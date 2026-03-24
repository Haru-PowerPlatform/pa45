"""
PA45 講座後 全自動公開スクリプト
------------------------------------------------------------
PPTXを受け取り、以下を自動実行する:
  1. PPTXの各スライドをPNG画像に変換（win32com / LibreOffice）
  2. WPメディアにスライド画像をアップロード
  3. OGPアイキャッチ（オレンジテーマ）を生成してアップロード
  4. スライド画像を埋め込んだブログ記事を作成（下書き or 公開）
  5. アイキャッチ・パーマリンク設定
  6. pa45サイト活動データ (activities JSON) を更新
  7. PPTXをGitHubリポジトリにコピー
  8. git commit & push → GitHub Pages 自動デプロイ

使い方:
  python scripts/pa45-publish.py \
    --pptx  "outputs/pa45/P002_PA45_変数を操作しよう_20260402.pptx" \
    --vol   2 \
    --title-ja "変数を操作しよう" \
    --title-en "Set variable" \
    --date  "2026-04-02" \
    [--publish]         # 即公開（省略時は下書き）
    [--post-id 1234]    # 既存投稿更新時

※ スライドをPNGに変換するには PowerPoint か LibreOffice が必要です。
------------------------------------------------------------
"""

import argparse
import base64
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
import urllib.error

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent

ACTIVITIES_DIR   = ROOT_DIR / "data" / "activities"
ACTIVITIES_INDEX = ROOT_DIR / "data" / "meta" / "activities-index.json"
ASSETS_PPTX_DIR  = ROOT_DIR / "assets" / "pa45"   # サイトに公開するPPTX格納先


# ── 環境変数 ──────────────────────────────────────────────────────────
def load_env():
    env = {}
    with open(ROOT_DIR / ".env", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip()
    return env


# ── WordPress リクエスト ───────────────────────────────────────────────
def wp_request(env, method, endpoint, data=None, binary=None, content_type="application/json"):
    url   = f"{env['WP_URL']}/wp-json/wp/v2/{endpoint}"
    creds = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}", "Content-Type": content_type}
    body  = json.dumps(data).encode("utf-8") if data is not None else binary
    req   = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode()}")
        sys.exit(1)


# ── Step 1: PPTXをPNGに変換 ───────────────────────────────────────────
def step_convert_slides(pptx_path: Path, out_dir: Path) -> list[Path]:
    """PPTXの各スライドをPNGに変換。win32com → LibreOffice の順で試みる。"""
    print("Step 1: PPTXをスライド画像に変換...")
    out_dir.mkdir(parents=True, exist_ok=True)

    # まず既存のPNGをチェック
    existing = sorted(out_dir.glob("slide_*.png"))
    if existing:
        print(f"  既存の画像が見つかりました: {len(existing)}枚")
        return existing

    # --- 方法A: win32com (Windows + PowerPoint必須) ---
    try:
        import win32com.client
        import re as _re
        pptx_abs = str(pptx_path.resolve())
        out_abs  = str(out_dir.resolve())

        ppt = win32com.client.Dispatch("PowerPoint.Application")
        ppt.Visible = True
        presentation = ppt.Presentations.Open(pptx_abs, ReadOnly=True)
        presentation.Export(out_abs, "PNG", 1920, 1080)
        presentation.Close()
        ppt.Quit()
        print("  win32com (PowerPoint) でPNG変換完了")

        # PowerPointは「スライド1.PNG」などのファイル名で出力する
        # 大文字小文字を区別せず一意ファイルを収集
        seen = set()
        raw_pngs = []
        for f in out_dir.iterdir():
            if f.suffix.lower() == ".png" and f.name not in seen:
                seen.add(f.name)
                raw_pngs.append(f)

        # 数値順でソート（スライド1, 2, ..., 16）
        def _slide_num(p):
            m = _re.search(r"(\d+)", p.stem)
            return int(m.group(1)) if m else 999

        raw_pngs.sort(key=_slide_num)

        # slide_001.png 形式にリネーム
        slides = []
        for i, f in enumerate(raw_pngs, 1):
            new_name = out_dir / f"slide_{i:03d}.png"
            f.rename(new_name)
            slides.append(new_name)
        print(f"  {len(slides)}枚のスライド画像を生成")
        return slides

    except ImportError:
        print("  win32com なし → LibreOffice を試みます...")
    except Exception as e:
        print(f"  win32com エラー: {e} → LibreOffice を試みます...")

    # --- 方法B: LibreOffice headless ---
    try:
        soffice = _find_soffice()
        # LibreOffice は直接PNG出力できないため PDF → PNG
        pdf_path = out_dir / "slides.pdf"
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf",
             "--outdir", str(out_dir), str(pptx_path)],
            check=True, capture_output=True,
        )
        # PDFのファイル名（LibreOfficeはPPTX名.pdfを出力）
        pdf_out = out_dir / (pptx_path.stem + ".pdf")
        if pdf_out.exists():
            pdf_out.rename(pdf_path)

        # pdf → png (pdftoppm or Pillow)
        try:
            result = subprocess.run(
                ["pdftoppm", "-png", "-r", "150", str(pdf_path), str(out_dir / "slide")],
                check=True, capture_output=True,
            )
            slides = sorted(out_dir.glob("slide-*.png"))
            # rename to slide_001.png
            renamed = []
            for i, f in enumerate(slides, 1):
                new_name = out_dir / f"slide_{i:03d}.png"
                f.rename(new_name)
                renamed.append(new_name)
            print(f"  LibreOffice + pdftoppm でPNG変換完了: {len(renamed)}枚")
            return renamed
        except FileNotFoundError:
            print("[ERROR] pdftoppm が見つかりません。Poppler をインストールしてください。")
            print("  代替: python -m pa45_publish_manual でスライド画像を手動指定できます。")
            sys.exit(1)

    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"[ERROR] スライドPNG変換失敗: {e}")
        print("  PowerPoint (win32com) または LibreOffice が必要です。")
        print("  スライド画像を手動で用意する場合:")
        print(f"    {out_dir}/slide_001.png, slide_002.png, ... という名前で配置してください。")
        print(f"  その後再実行してください。")
        sys.exit(1)


def _find_soffice():
    candidates = [
        "C:/Program Files/LibreOffice/program/soffice.exe",
        "C:/Program Files (x86)/LibreOffice/program/soffice.exe",
        "soffice",
    ]
    for c in candidates:
        if Path(c).exists() or c == "soffice":
            return c
    raise FileNotFoundError("LibreOffice (soffice) が見つかりません")


# ── Step 2: WPにスライド画像をアップロード ────────────────────────────
def step_upload_slides(env, slide_pngs: list[Path]) -> list[dict]:
    """スライドPNGをWPメディアにアップロード。[{id, url}, ...] を返す。"""
    print(f"Step 2: スライド画像をWordPressにアップロード ({len(slide_pngs)}枚)...")
    creds = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    results = []

    for i, png in enumerate(slide_pngs, 1):
        fname = f"pa45-slide-{int(time.time())}-{i:03d}.png"
        with open(png, "rb") as f:
            binary = f.read()
        req = Request(
            f"{env['WP_URL']}/wp-json/wp/v2/media",
            data=binary,
            headers={
                "Authorization": f"Basic {creds}",
                "Content-Type": "image/png",
                "Content-Disposition": f"attachment; filename={fname}",
            },
            method="POST",
        )
        with urlopen(req) as resp:
            r = json.loads(resp.read().decode("utf-8"))
        results.append({"id": r["id"], "url": r["source_url"]})
        print(f"  [{i:02d}/{len(slide_pngs)}] ID={r['id']} url={r['source_url']}")
        time.sleep(0.3)  # WP API レート制限対策

    return results


# ── Step 3: OGPアイキャッチ生成・アップロード ─────────────────────────
def step_generate_ogp(vol: int, title_ja: str, date: str) -> Path:
    """オレンジテーマのOGPを生成。"""
    print("Step 3: OGPアイキャッチ生成...")
    ogp_title = f"PA45 第{vol}回\n{title_ja}"
    png_path = SCRIPT_DIR / "ogp-output.png"
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "make-ogp.py"),
         "--title", ogp_title,
         "--label", "PA45 開催レポート",
         "--sub",   "Power Automate 45",
         "--theme", "orange",
         "--out",   "scripts/ogp-output.png"],
        cwd=str(ROOT_DIR), capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"[ERROR] OGP生成失敗:\n{result.stderr}")
        sys.exit(1)
    print("  OGP生成OK")
    return png_path


def step_upload_ogp(env, png_path: Path) -> int:
    """OGP画像をWPメディアにアップロード。media_id を返す。"""
    fname = f"pa45-ogp-{int(time.time())}.png"
    creds = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    with open(png_path, "rb") as f:
        binary = f.read()
    req = Request(
        f"{env['WP_URL']}/wp-json/wp/v2/media",
        data=binary,
        headers={
            "Authorization": f"Basic {creds}",
            "Content-Type": "image/png",
            "Content-Disposition": f"attachment; filename={fname}",
        },
        method="POST",
    )
    with urlopen(req) as resp:
        r = json.loads(resp.read().decode("utf-8"))
    print(f"  OGP メディアID: {r['id']}")
    return r["id"]


# ── Step 4: ブログ本文を生成 ──────────────────────────────────────────
def build_blog_body(vol: int, title_ja: str, title_en: str, date: str,
                    slide_media: list[dict]) -> str:
    """スライド画像を埋め込んだブログ本文HTMLを生成する。"""

    lines = []

    # 導入
    lines.append(f"""<p>こんにちは、Haru です。</p>
<p>PA45 第{vol}回「{title_ja}」を開催しました。</p>
<p>今回は <strong>{title_en}</strong> について、45分でハンズオン形式で学びました。</p>
<p>&nbsp;</p>""")

    # スライドギャラリー
    lines.append(f"<h2>第{vol}回 スライド資料</h2>")
    lines.append("<p>当日使用したスライドを全枚掲載します。</p>")
    lines.append("<p>&nbsp;</p>")

    for i, media in enumerate(slide_media, 1):
        lines.append(
            f'<figure class="wp-block-image size-large">'
            f'<img src="{media["url"]}" alt="PA45 第{vol}回 スライド{i}" '
            f'class="wp-image-{media["id"]}" loading="lazy" />'
            f'<figcaption>スライド {i}</figcaption>'
            f'</figure>'
        )
        lines.append("<p>&nbsp;</p>")

    # 締め
    lines.append(f"""<p>&nbsp;</p>
<h2>参加してくださった方へ</h2>
<p>今日も参加いただきありがとうございました！</p>
<p>「できた！」という体験が、次の一歩につながります。</p>
<p>感想や質問は <strong>#PA45</strong> でポストしてください。</p>
<p>&nbsp;</p>
<p>次回もお楽しみに！</p>""")

    return "\n".join(lines)


# ── Step 5: WP投稿作成・更新 ──────────────────────────────────────────
def step_create_post(env, title: str, body: str, post_id=None, publish=False) -> int:
    status = "publish" if publish else "draft"
    label  = "公開" if publish else "下書き"
    print(f"Step 5: WordPress {label}作成...")
    payload = {"title": title, "content": body, "status": status}
    if post_id:
        wp_request(env, "POST", f"posts/{post_id}", data=payload)
        print(f"  既存投稿 #{post_id} を{label}に更新")
        return post_id
    else:
        result  = wp_request(env, "POST", "posts", data=payload)
        post_id = result["id"]
        print(f"  新規投稿 #{post_id} を{label}で作成")
        return post_id


def step_set_featured(env, post_id: int, media_id: int):
    print(f"Step 6: アイキャッチ設定...")
    wp_request(env, "POST", f"posts/{post_id}", data={"featured_media": media_id})
    print("  設定OK")


def step_set_slug(env, post_id: int, slug: str):
    if not slug:
        return
    print(f"Step 7: パーマリンク設定... ({slug})")
    wp_request(env, "POST", f"posts/{post_id}", data={"slug": slug})
    print("  設定OK")


# ── Step 8: PPTXをリポジトリにコピー ─────────────────────────────────
def step_copy_pptx(pptx_path: Path, vol: int) -> Path:
    """PPTXをリポジトリの assets/pa45/ にコピーする。"""
    print("Step 8: PPTXをリポジトリにコピー...")
    ASSETS_PPTX_DIR.mkdir(parents=True, exist_ok=True)
    dest = ASSETS_PPTX_DIR / pptx_path.name
    import shutil
    shutil.copy2(pptx_path, dest)
    print(f"  コピー → {dest}")
    return dest


# ── Step 9: pa45サイト活動データ更新 ─────────────────────────────────
def step_update_site(act_id: str, vol: int, title_ja: str, title_en: str,
                     date: str, slug: str, pptx_dest: Path, env: dict,
                     post_id: int, publish: bool):
    print("Step 9: pa45サイトの活動データを更新...")

    blog_url  = f"{env['WP_URL']}/{slug}/" if slug else ""
    pptx_url  = f"https://isamu-kato.github.io/pa45/assets/pa45/{pptx_dest.name}" if pptx_dest else ""

    activity = {
        "id":      act_id,
        "type":    "PA45",
        "title":   f"PA45 第{vol}回：{title_ja}",
        "date":    date,
        "public":  publish,
        "summary": f"Power Automate 45 第{vol}回。テーマ：{title_en}（{title_ja}）",
        "tags":    ["PA45", "Power Automate", "ハンズオン"],
        "evidence": {
            "blog":  blog_url,
            "slide": pptx_url,
        },
    }

    out_path = ACTIVITIES_DIR / f"{act_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(activity, f, ensure_ascii=False, indent=2)
    print(f"  活動JSON: {out_path.name}")

    rel_path = f"data/activities/{act_id}.json"
    if ACTIVITIES_INDEX.exists():
        with open(ACTIVITIES_INDEX, encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = []

    if rel_path not in index:
        index.insert(0, rel_path)
        with open(ACTIVITIES_INDEX, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        print(f"  index更新: {rel_path} を追加")
    else:
        print(f"  index: 既に登録済み（更新）")
        # 上書きしたので再write
        with open(ACTIVITIES_INDEX, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

    # git commit & push
    print("Step 10: GitHubにプッシュ...")

    def git(cmd):
        result = subprocess.run(
            ["git"] + cmd, cwd=str(ROOT_DIR),
            capture_output=True, text=True,
        )
        return result.stdout.strip(), result.returncode

    files_to_add = [str(out_path), str(ACTIVITIES_INDEX)]
    if pptx_dest and pptx_dest.exists():
        files_to_add.append(str(pptx_dest))

    git(["add"] + files_to_add)
    msg = f"Add PA45 Vol{vol}: {title_ja}"
    stdout, code = git(["commit", "-m", msg,
                        "--author", "Claude Sonnet 4.6 <noreply@anthropic.com>"])
    if code != 0:
        print(f"  コミットスキップ（変更なし or エラー）")
    else:
        print(f"  コミット: {msg}")
        git(["push", "origin", "main"])
        print("  GitHubプッシュ完了 → GitHub Pages 自動デプロイ開始")


# ── メイン ────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="PA45 講座後 全自動公開")
    p.add_argument("--pptx",      required=True, help="PPTXファイルパス")
    p.add_argument("--vol",       required=True, type=int, help="回数")
    p.add_argument("--title-ja",  required=True, help="日本語テーマ")
    p.add_argument("--title-en",  default="",    help="英語タイトル")
    p.add_argument("--date",      required=True, help="開催日 YYYY-MM-DD")
    p.add_argument("--slug",      default="",    help="パーマリンク（省略時は自動生成）")
    p.add_argument("--post-id",   default=None,  type=int, help="既存投稿ID")
    p.add_argument("--publish",   action="store_true", help="即公開")
    p.add_argument("--slides-dir", default="",   help="既存スライドPNGのディレクトリ（変換スキップ）")
    args = p.parse_args()

    pptx_path = Path(args.pptx)
    if not pptx_path.exists():
        print(f"[ERROR] PPTXファイルが見つかりません: {pptx_path}")
        sys.exit(1)

    env = load_env()

    # スライド画像ディレクトリ
    slides_dir = Path(args.slides_dir) if args.slides_dir else \
        SCRIPT_DIR / "pa45-slides" / f"vol{args.vol:03d}"

    # スラッグ自動生成
    slug = args.slug
    if not slug:
        import re
        safe = re.sub(r"[^\w-]", "", args.title_en.lower().replace(" ", "-"))
        slug = f"pa45-vol{args.vol}-{safe}" if safe else f"pa45-vol{args.vol}"

    act_id = f"{args.date}-pa45-vol{args.vol}"
    title  = f"【PA45 第{args.vol}回】{args.title_ja}（{args.title_en}）"

    print(f"\nPA45 第{args.vol}回 公開フロー開始")
    print(f"  テーマ: {args.title_ja} / {args.title_en}")
    print(f"  日付:   {args.date}")
    print(f"  slug:   {slug}")
    print(f"  状態:   {'公開' if args.publish else '下書き'}")
    print()

    # Step 1: PNG変換
    slide_pngs = step_convert_slides(pptx_path, slides_dir)

    # Step 2: スライド画像アップロード
    slide_media = step_upload_slides(env, slide_pngs)

    # Step 3: OGP生成
    ogp_png = step_generate_ogp(args.vol, args.title_ja, args.date)

    # Step 3b: OGPアップロード
    ogp_media_id = step_upload_ogp(env, ogp_png)

    # Step 4: 本文生成
    body = build_blog_body(
        args.vol, args.title_ja, args.title_en or args.title_ja,
        args.date, slide_media
    )

    # Step 5: WP投稿
    post_id = step_create_post(env, title, body, args.post_id, args.publish)

    # Step 6: アイキャッチ
    step_set_featured(env, post_id, ogp_media_id)

    # Step 7: スラッグ
    step_set_slug(env, post_id, slug)

    # Step 8: PPTXをリポジトリにコピー
    pptx_dest = step_copy_pptx(pptx_path, args.vol)

    # Step 9-10: サイト更新 + git push
    step_update_site(
        act_id, args.vol, args.title_ja, args.title_en,
        args.date, slug, pptx_dest, env, post_id, args.publish
    )

    print()
    print("=" * 60)
    print(f"[完了] 投稿ID    : {post_id}")
    print(f"[完了] OGP ID   : {ogp_media_id}")
    print(f"[完了] スライド  : {len(slide_media)}枚")
    print(f"[完了] 管理画面  : {env['WP_URL']}/wp-admin/post.php?post={post_id}&action=edit")
    print(f"[完了] ブログURL : {env['WP_URL']}/{slug}/")
    print(f"[完了] 活動ID   : {act_id}")
    print(f"[完了] ステータス: {'公開済み' if args.publish else '下書き（管理画面から公開してください）'}")
    print("=" * 60)


if __name__ == "__main__":
    main()

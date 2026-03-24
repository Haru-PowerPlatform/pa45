"""
PA45 ブログ全自動投稿スクリプト
------------------------------------------------------------
使い方:
  python scripts/new-post.py \
    --title    "記事タイトル" \
    --body     "本文HTML" \
    --label    "pill上段" \
    --sub      "pill下段" \
    --theme    blue \
    --ogp      "アイキャッチ用タイトル\n2行目" \
    --slug     "english-url-slug" \
    --act-type blog \
    --act-date 2026-03-19 \
    --act-id   "2026-03-19-ippo-tv-ep25" \
    --event-url "https://connpass.com/..." \
    [--post-id 1234]   # 既存下書き更新時
    [--publish]        # 即公開（省略時は下書き）

--act-type の選択肢:
  blog      : ブログ記事（青 / 緑テーマ向け）
  PA45      : PA45開催レポート（オレンジ）
  Event     : 登壇・イベント（赤）
  X         : X投稿（黒）
  Community : コミュニティ活動

※ サイト更新（GitHub Pages）は常に実行されます。
------------------------------------------------------------
"""

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path
from urllib.request import urlopen, Request
import urllib.error
import base64

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent

ACTIVITIES_DIR   = ROOT_DIR / "data" / "activities"
ACTIVITIES_INDEX = ROOT_DIR / "data" / "meta" / "activities-index.json"


# ── 環境変数 ──────────────────────────────────────────────────────────────
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


# ── WordPress リクエスト ───────────────────────────────────────────────────
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


# ── Step 1: WordPress 下書き作成／更新 ────────────────────────────────────
def step_create_post(env, title, body, post_id=None, publish=False):
    status = "publish" if publish else "draft"
    label  = "公開" if publish else "下書き"
    print(f"▶ Step 1: WordPress {label}作成...")
    payload = {"title": title, "content": body, "status": status}
    if post_id:
        wp_request(env, "POST", f"posts/{post_id}", data=payload)
        print(f"  既存投稿 #{post_id} を{label}に更新しました")
    else:
        result  = wp_request(env, "POST", "posts", data=payload)
        post_id = result["id"]
        print(f"  新規投稿 #{post_id} を{label}で作成しました")
    return post_id


# ── Step 2: アイキャッチ画像生成 ──────────────────────────────────────────
def step_generate_ogp(title_lines, label, sub, theme="blue"):
    print("▶ Step 2: アイキャッチ画像を生成...")
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "make-ogp.py"),
         "--title", title_lines, "--label", label,
         "--sub", sub, "--theme", theme, "--out", "scripts/ogp-output.png"],
        cwd=str(ROOT_DIR), capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"[ERROR] 画像生成失敗:\n{result.stderr}")
        sys.exit(1)
    print("  画像生成OK")


# ── Step 3: WP メディアアップロード ───────────────────────────────────────
def step_upload_media(env, png_path):
    print("▶ Step 3: 画像をWordPressにアップロード...")
    fname = f"ogp-{int(time.time())}.png"
    with open(png_path, "rb") as f:
        binary = f.read()
    creds = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    req = Request(f"{env['WP_URL']}/wp-json/wp/v2/media", data=binary,
        headers={"Authorization": f"Basic {creds}", "Content-Type": "image/png",
                 "Content-Disposition": f"attachment; filename={fname}"}, method="POST")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    media_id = result["id"]
    print(f"  メディアID: {media_id}")
    return media_id


# ── Step 4: アイキャッチ設定 ──────────────────────────────────────────────
def step_set_featured(env, post_id, media_id):
    print("▶ Step 4: アイキャッチを設定...")
    wp_request(env, "POST", f"posts/{post_id}", data={"featured_media": media_id})
    print("  設定OK")


# ── Step 5: パーマリンク設定 ──────────────────────────────────────────────
def step_set_slug(env, post_id, slug):
    if not slug:
        return
    print(f"▶ Step 5: パーマリンクを設定... ({slug})")
    wp_request(env, "POST", f"posts/{post_id}", data={"slug": slug})
    print("  設定OK")


# ── Step 6: pa45サイト（活動データ）更新 ──────────────────────────────────
def step_update_site(act_id, act_type, act_date, title, summary,
                     slug, env, event_url=""):
    print("▶ Step 6: pa45サイトの活動データを更新...")

    blog_url = f"{env['WP_URL']}/{slug}/" if slug else ""

    activity = {
        "id":      act_id,
        "type":    act_type,
        "title":   title,
        "date":    act_date,
        "public":  True,
        "summary": summary,
        "tags":    [],
        "evidence": {
            "blog":  blog_url,
            "event": event_url,
        },
    }

    # JSON ファイル書き出し
    out_path = ACTIVITIES_DIR / f"{act_id}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(activity, f, ensure_ascii=False, indent=2)
    print(f"  活動JSON: {out_path.name}")

    # activities-index.json 更新
    rel_path = f"data/activities/{act_id}.json"
    if ACTIVITIES_INDEX.exists():
        with open(ACTIVITIES_INDEX, encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = []

    if rel_path not in index:
        # 日付順（新しい順）に挿入
        index.insert(0, rel_path)
        with open(ACTIVITIES_INDEX, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
        print(f"  index更新: {rel_path} を追加")
    else:
        print(f"  index: 既に登録済み")

    # Git commit & push
    print("▶ Step 7: GitHubにプッシュ...")
    def git(cmd):
        result = subprocess.run(
            ["git"] + cmd, cwd=str(ROOT_DIR),
            capture_output=True, text=True,
        )
        return result.stdout.strip(), result.returncode

    git(["add", str(out_path), str(ACTIVITIES_INDEX)])
    msg = f"Add activity: {act_id}"
    stdout, code = git(["commit", "-m", msg,
                        "--author", "Claude Sonnet 4.6 <noreply@anthropic.com>"])
    if code != 0:
        print(f"  コミットスキップ（変更なし or エラー）")
    else:
        print(f"  コミット: {msg}")
        git(["push", "origin", "main"])
        print("  GitHubプッシュ完了 → GitHub Pages 自動デプロイ開始")


# ── メイン ────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="PA45 ブログ全自動投稿 + サイト更新")
    p.add_argument("--title",     required=True,  help="記事タイトル")
    p.add_argument("--body",      default="",     help="本文（HTML可）")
    p.add_argument("--label",     required=True,  help="アイキャッチ pill 上段")
    p.add_argument("--sub",       required=True,  help="アイキャッチ pill 下段")
    p.add_argument("--theme",     default="blue",
                   choices=["blue","orange","green","red","yellow"])
    p.add_argument("--ogp",       default="",     help="アイキャッチ用タイトル（\\nで改行）")
    p.add_argument("--slug",      default="",     help="英語パーマリンク")
    p.add_argument("--post-id",   default=None,   type=int)
    # サイト更新用
    p.add_argument("--act-type",  default="blog", help="活動タイプ: blog/PA45/Event/X/Community")
    p.add_argument("--act-date",  default=str(date.today()), help="活動日 YYYY-MM-DD")
    p.add_argument("--act-id",    default="",     help="活動ID（省略時は日付+slugから自動生成）")
    p.add_argument("--act-summary", default="",   help="活動サマリー1文")
    p.add_argument("--event-url", default="",     help="connpassなどのイベントURL")
    p.add_argument("--publish",   action="store_true", help="即公開（省略時は下書き）")
    args = p.parse_args()

    env      = load_env()
    png_path = ROOT_DIR / "scripts" / "ogp-output.png"
    ogp_title = args.ogp if args.ogp else args.title

    # 活動ID の自動生成
    act_id = args.act_id
    if not act_id:
        slug_part = re.sub(r"[^a-z0-9-]", "", args.slug.lower())[:30] if args.slug else "post"
        act_id = f"{args.act_date}-{slug_part}"

    # ── 実行 ──────────────────────────────────────────────────────────────
    post_id  = step_create_post(env, args.title, args.body, args.post_id, args.publish)
    step_generate_ogp(ogp_title, args.label, args.sub, args.theme)
    media_id = step_upload_media(env, png_path)
    step_set_featured(env, post_id, media_id)
    step_set_slug(env, post_id, args.slug)

    # サイト更新は常に実行
    summary = args.act_summary or args.title
    step_update_site(act_id, args.act_type, args.act_date,
                     args.title, summary, args.slug, env, args.event_url)

    print()
    print("=" * 55)
    print(f"[完了] 投稿ID    : {post_id}")
    print(f"[完了] メディアID: {media_id}")
    print(f"[完了] 管理画面  : {env['WP_URL']}/wp-admin/post.php?post={post_id}&action=edit")
    if args.slug:
        print(f"[完了] ブログURL : {env['WP_URL']}/{args.slug}/")
    print(f"[完了] 活動ID    : {act_id}")
    if args.publish:
        print(f"[完了] ステータス: 公開済み ✓")
    else:
        print(f"[完了] ステータス: 下書き（管理画面から公開してください）")
    print("=" * 55)


if __name__ == "__main__":
    main()

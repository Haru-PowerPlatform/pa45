"""
PA45 ブログ全自動投稿スクリプト
使い方:
  python scripts/new-post.py \
    --title  "記事タイトル" \
    --body   "本文（★マーカーを入れたいならここに書く）" \
    --label  "pill上段" \
    --sub    "pill下段" \
    --slug   "english-url-slug" \
    [--post-id 1234]   # 既存下書きを更新する場合

引数なしで呼び出した場合はヘルプを表示。
"""

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import urllib.error
import base64

# ── パス設定 ──────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR   = SCRIPT_DIR.parent


def load_env():
    env = {}
    env_path = ROOT_DIR / ".env"
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip()
    return env


def wp_request(env, method, endpoint, data=None, binary=None, content_type="application/json"):
    url = f"{env['WP_URL']}/wp-json/wp/v2/{endpoint}"
    creds = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    headers = {
        "Authorization": f"Basic {creds}",
        "Content-Type": content_type,
    }
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
    if binary is not None:
        body = binary
    req = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode()}")
        sys.exit(1)


# ── Step 1: WordPress 下書き作成／更新 ──────────────────────────────────
def step_create_post(env, title, body, post_id=None):
    print("▶ Step 1: WordPress 下書き作成...")
    payload = {
        "title":   title,
        "content": body,
        "status":  "draft",
    }
    if post_id:
        result = wp_request(env, "POST", f"posts/{post_id}", data=payload)
        print(f"  既存投稿 #{post_id} を更新しました")
    else:
        result = wp_request(env, "POST", "posts", data=payload)
        post_id = result["id"]
        print(f"  新規投稿 #{post_id} を作成しました")
    return post_id


# ── Step 2: アイキャッチ画像生成 ────────────────────────────────────────
def step_generate_ogp(title_lines, label, sub):
    print("▶ Step 2: アイキャッチ画像を生成...")
    import subprocess
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT_DIR / "make-ogp.py"),
            "--title", title_lines,
            "--label", label,
            "--sub",   sub,
            "--out",   "scripts/ogp-output.png",
        ],
        cwd=str(ROOT_DIR),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"[ERROR] 画像生成失敗:\n{result.stderr}")
        sys.exit(1)
    print("  画像生成OK")


# ── Step 3: WP メディアアップロード ─────────────────────────────────────
def step_upload_media(env, png_path):
    print("▶ Step 3: 画像をWordPressにアップロード...")
    fname = f"ogp-{int(time.time())}.png"
    with open(png_path, "rb") as f:
        binary = f.read()

    url  = f"{env['WP_URL']}/wp-json/wp/v2/media"
    creds = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    headers = {
        "Authorization":       f"Basic {creds}",
        "Content-Type":        "image/png",
        "Content-Disposition": f"attachment; filename={fname}",
    }
    req = Request(url, data=binary, headers=headers, method="POST")
    with urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    media_id = result["id"]
    print(f"  メディアID: {media_id}")
    return media_id


# ── Step 4: アイキャッチ設定 ────────────────────────────────────────────
def step_set_featured(env, post_id, media_id):
    print("▶ Step 4: アイキャッチを設定...")
    wp_request(env, "POST", f"posts/{post_id}", data={"featured_media": media_id})
    print("  設定OK")


# ── Step 5: パーマリンク（スラッグ）設定 ────────────────────────────────
def step_set_slug(env, post_id, slug):
    if not slug:
        return
    print(f"▶ Step 5: パーマリンクを設定... ({slug})")
    wp_request(env, "POST", f"posts/{post_id}", data={"slug": slug})
    print("  設定OK")


# ── メイン ───────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(description="PA45 ブログ全自動投稿")
    p.add_argument("--title",   required=True,  help="記事タイトル")
    p.add_argument("--body",    default="",     help="本文（HTML可）")
    p.add_argument("--label",   required=True,  help="アイキャッチ pill 上段")
    p.add_argument("--sub",     required=True,  help="アイキャッチ pill 下段")
    p.add_argument("--ogp",     default="",     help="アイキャッチ用タイトル（省略時は--titleを使用）")
    p.add_argument("--slug",    default="",     help="英語パーマリンク")
    p.add_argument("--post-id", default=None,   type=int, help="既存投稿IDを更新する場合")
    args = p.parse_args()

    env     = load_env()
    png_path = ROOT_DIR / "scripts" / "ogp-output.png"

    # アイキャッチ用タイトル（改行で3行まで）
    ogp_title = args.ogp if args.ogp else args.title

    post_id  = step_create_post(env, args.title, args.body, args.post_id)
    step_generate_ogp(ogp_title, args.label, args.sub)
    media_id = step_upload_media(env, png_path)
    step_set_featured(env, post_id, media_id)
    step_set_slug(env, post_id, args.slug)

    print()
    print("=" * 50)
    print(f"[完了] 投稿ID    : {post_id}")
    print(f"[完了] メディアID: {media_id}")
    print(f"[完了] 管理画面  : {env['WP_URL']}/wp-admin/post.php?post={post_id}&action=edit")
    if args.slug:
        print(f"[完了] URL       : {env['WP_URL']}/{args.slug}/")
    print("=" * 50)


if __name__ == "__main__":
    main()

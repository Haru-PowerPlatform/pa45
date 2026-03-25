"""
WordPress記事をQiitaにクロスポストするスクリプト

使い方:
  python scripts/cross-post-qiita.py --list        # 対象記事一覧表示
  python scripts/cross-post-qiita.py --dry-run     # 変換内容確認（投稿しない）
  python scripts/cross-post-qiita.py --all         # 全記事をQiitaに下書き投稿
  python scripts/cross-post-qiita.py --vol 5       # 特定のVol番号だけ
"""

import sys, io, json, re, base64, argparse
from pathlib import Path
from urllib.request import urlopen, Request
import urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent

def load_env():
    env = {}
    with open(ROOT / ".env", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env

ENV = load_env()

# ── WordPress API ─────────────────────────────────────────────────────────────

def wp_get(endpoint):
    url = f"{ENV['WP_URL']}/wp-json/wp/v2/{endpoint}"
    creds = base64.b64encode(f"{ENV['WP_USER']}:{ENV['WP_PASS']}".encode()).decode()
    req = Request(url, headers={"Authorization": f"Basic {creds}"})
    with urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def wp_publish(post_id):
    """WP記事を公開状態にする"""
    url = f"{ENV['WP_URL']}/wp-json/wp/v2/posts/{post_id}"
    creds = base64.b64encode(f"{ENV['WP_USER']}:{ENV['WP_PASS']}".encode()).decode()
    data = json.dumps({"status": "publish"}).encode("utf-8")
    req = Request(url, data=data, headers={
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json"
    }, method="POST")
    with urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def get_wp_posts():
    """X投稿スライド記事（下書き含む）を取得"""
    posts = []
    page = 1
    while True:
        batch = wp_get(f"posts?per_page=100&page={page}&status=draft,publish&_fields=id,title,content,link,slug,status")
        if not batch:
            break
        posts.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    # 【Vol.N】形式のタイトルを持つ記事だけ絞り込む
    result = []
    for p in posts:
        title = p["title"]["rendered"]
        m = re.search(r"【Vol\.(\d+)】", title)
        if m:
            p["vol"] = int(m.group(1))
            result.append(p)
    return sorted(result, key=lambda x: x["vol"])

# ── HTML → Markdown 変換 ──────────────────────────────────────────────────────

def html_to_markdown(html):
    """WordPress HTMLをQiita向けMarkdownに変換"""
    # Gutenbergブロックコメント除去
    text = re.sub(r'<!-- /?wp:[^>]* -->', '', html)

    # コードブロック（先に処理）
    text = re.sub(
        r'<pre[^>]*><code[^>]*>(.*?)</code></pre>',
        lambda m: '\n```\n' + _unescape(m.group(1)) + '\n```\n',
        text, flags=re.DOTALL
    )
    text = re.sub(r'<code>(.*?)</code>', r'`\1`', text, flags=re.DOTALL)

    # 見出し
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', text, flags=re.DOTALL)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', text, flags=re.DOTALL)

    # 強調
    text = re.sub(r'<strong>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)

    # リスト
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', text, flags=re.DOTALL)
    text = re.sub(r'</?[uo]l[^>]*>', '', text)

    # 段落・改行
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text)

    # 吹き出しブロック → 引用に変換
    text = re.sub(
        r'<div class="speech-balloon">(.*?)</div>',
        lambda m: '\n> ' + _strip_tags(m.group(1)).strip() + '\n',
        text, flags=re.DOTALL
    )

    # spanタグ（色強調など）→ テキストのみ残す
    text = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', text, flags=re.DOTALL)

    # nbsp
    text = text.replace('&nbsp;', ' ')

    # 残りのHTMLタグを除去
    text = _strip_tags(text)

    # HTMLエンティティ
    text = _unescape(text)

    # 連続空行を最大2行に
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

def _strip_tags(html):
    return re.sub(r'<[^>]+>', '', html)

def _unescape(text):
    return (text
        .replace('&amp;', '&')
        .replace('&lt;', '<')
        .replace('&gt;', '>')
        .replace('&quot;', '"')
        .replace('&#039;', "'")
        .replace('&nbsp;', ' ')
    )

# ── Qiita API ─────────────────────────────────────────────────────────────────

QIITA_TAGS = [
    {"name": "PowerAutomate"},
    {"name": "PowerPlatform"},
    {"name": "Microsoft365"},
    {"name": "初心者向け"},
]

def qiita_post(title, body, is_draft=True):
    url = "https://qiita.com/api/v2/items"
    data = json.dumps({
        "title": title,
        "body": body,
        "tags": QIITA_TAGS,
        "private": is_draft,
    }).encode("utf-8")
    req = Request(url, data=data, headers={
        "Authorization": f"Bearer {ENV['QIITA_TOKEN']}",
        "Content-Type": "application/json",
    }, method="POST")
    with urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def build_qiita_body(wp_url, markdown_content):
    header = f":::note info\n元記事：{wp_url}\n:::\n\n"
    return header + markdown_content

# ── 投稿済み管理 ──────────────────────────────────────────────────────────────

QIITA_POSTS_PATH = ROOT / "data" / "meta" / "qiita-posts.json"

def load_posted():
    if not QIITA_POSTS_PATH.exists():
        return []
    with open(QIITA_POSTS_PATH, encoding="utf-8") as f:
        return json.load(f).get("posted", [])

def save_posted(posted):
    with open(QIITA_POSTS_PATH, "w", encoding="utf-8") as f:
        json.dump({"posted": posted}, f, ensure_ascii=False, indent=2)

# ── メイン処理 ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true", help="対象記事一覧表示")
    parser.add_argument("--dry-run", action="store_true", help="変換内容確認のみ（投稿しない）")
    parser.add_argument("--all", action="store_true", help="全記事をQiitaに下書き投稿")
    parser.add_argument("--next", action="store_true", help="次の未投稿記事を1件投稿")
    parser.add_argument("--publish-wp", action="store_true", help="WP記事を公開してからQiitaに投稿")
    parser.add_argument("--vol", type=int, help="特定のVol番号")
    args = parser.parse_args()

    print("WordPressから記事を取得中...")
    posts = get_wp_posts()
    print(f"{len(posts)}件取得")

    if args.vol:
        posts = [p for p in posts if p["vol"] == args.vol]
        if not posts:
            print(f"Vol.{args.vol} が見つかりません")
            return

    posted = load_posted()
    posted_vols = {p["vol"] for p in posted}

    if args.list:
        for p in posts:
            status = p.get("status", "?")
            done = "✅" if p["vol"] in posted_vols else "⬜"
            print(f"  {done} Vol.{p['vol']:2d}  [{status:7s}]  ID:{p['id']}  {p['title']['rendered']}")
        print(f"\n投稿済み: {len(posted_vols)}/{len(posts)}件")
        return

    # --next: 次の未投稿を1件だけ投稿
    if args.next:
        remaining = [p for p in posts if p["vol"] not in posted_vols]
        if not remaining:
            print("全件投稿済みです")
            return
        posts = [remaining[0]]

    for p in posts:
        vol = p["vol"]
        title = _strip_tags(p["title"]["rendered"])
        wp_url = p["link"]

        # --next のとき投稿済みはスキップ
        if args.next and vol in posted_vols:
            continue

        # WP公開
        if args.publish_wp and p.get("status") != "publish":
            print(f"  Vol.{vol:2d} WP公開中...", end=" ")
            result = wp_publish(p["id"])
            wp_url = result["link"]
            print(f"完了 → {wp_url}")

        # Markdown変換
        html_content = p["content"]["rendered"]
        md = html_to_markdown(html_content)
        body = build_qiita_body(wp_url, md)

        if args.dry_run:
            print(f"\n{'='*60}")
            print(f"Vol.{vol}  {title}")
            print(f"元記事URL: {wp_url}")
            print(f"{'─'*40}")
            print(body[:500] + "..." if len(body) > 500 else body)
            continue

        if args.all or args.vol or args.next:
            print(f"  Vol.{vol:2d} Qiita投稿中...", end=" ")
            try:
                result = qiita_post(title, body, is_draft=True)
                qiita_url = result["url"]
                print(f"完了 → {qiita_url}")
                # 投稿済みに追記
                from datetime import date
                posted.append({"vol": vol, "qiita_url": qiita_url, "date": str(date.today())})
                save_posted(posted)
                posted_vols.add(vol)
            except urllib.error.HTTPError as e:
                print(f"エラー: {e.code} {e.read().decode()}")

    if not (args.list or args.dry_run or args.all or args.vol or args.next):
        print("オプションを指定してください。--help で確認")

if __name__ == "__main__":
    main()

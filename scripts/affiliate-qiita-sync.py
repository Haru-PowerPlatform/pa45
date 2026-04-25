"""affiliate 3サイト → 各専用Qiitaアカウントへ記事をクロスポスト。
PA45のQiitaアカウントとは完全分離。

env vars:
  WP_BIZENGLISHAI_USER / WP_BIZENGLISHAI_PASS / QIITA_TOKEN_BIZENGLISHAI
  WP_AIGYOMU_USER     / WP_AIGYOMU_PASS     / QIITA_TOKEN_AIGYOMU
  (side-invest は Qiita 対象外＝note で配信)

Trigger:
  python scripts/affiliate-qiita-sync.py --site biz-english-ai --limit 1
  python scripts/affiliate-qiita-sync.py --site ai-gyomu       --limit 1

State (どの記事を投稿したか) は data/affiliate-qiita-state.json に記録。
重複投稿防止。
"""
import os, sys, io, json, re, base64, argparse, time
from pathlib import Path
from urllib.request import urlopen, Request
import urllib.error

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
STATE = ROOT / "data" / "affiliate-qiita-state.json"
STATE.parent.mkdir(exist_ok=True)

SITES = {
    "biz-english-ai": {
        "wp_url":   "https://biz-english-ai.com",
        "user_env": "WP_BIZENGLISHAI_USER",
        "pass_env": "WP_BIZENGLISHAI_PASS",
        "qiita_token_env": "QIITA_TOKEN_BIZENGLISHAI",
        "default_tags": [{"name": "英語学習"}, {"name": "AI"}, {"name": "ブログ"}],
    },
    "ai-gyomu": {
        "wp_url":   "https://ai-gyomu.jp",
        "user_env": "WP_AIGYOMU_USER",
        "pass_env": "WP_AIGYOMU_PASS",
        "qiita_token_env": "QIITA_TOKEN_AIGYOMU",
        "default_tags": [{"name": "SaaS"}, {"name": "業務効率化"}, {"name": "個人事業主"}],
    },
}

def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"posted": {}}

def save_state(s):
    STATE.write_text(json.dumps(s, indent=2, ensure_ascii=False), encoding="utf-8")

def http_json(url, method="GET", headers=None, data=None, timeout=30):
    headers = dict(headers or {})
    body = json.dumps(data).encode() if data else None
    if body:
        headers.setdefault("Content-Type", "application/json")
    req = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")

def fetch_wp_posts(site_cfg, user, pw, limit=20):
    auth = base64.b64encode(f"{user}:{pw}".encode()).decode()
    url = f"{site_cfg['wp_url']}/wp-json/wp/v2/posts?status=publish&per_page={limit}&orderby=date&order=desc&_fields=id,title,link,content,date,excerpt"
    status, js = http_json(url, headers={"Authorization": f"Basic {auth}"})
    if status != 200:
        print(f"  WP fetch error {status}", file=sys.stderr)
        return []
    return js or []

def html_to_md(html_str):
    """Minimal HTML→Markdown for Qiita."""
    s = html_str
    # Strip our balloon divs entirely (they're inline-styled and don't render in Qiita)
    s = re.sub(r'<!-- char-convo-(?:start|inline\d+)-start -->.*?<!-- char-convo-(?:start|inline\d+)-end -->', '', s, flags=re.S)
    s = re.sub(r'<div style="display:flex.*?</div>\s*</div>', '', s, flags=re.S)
    # h tags
    for n in (1,2,3,4):
        s = re.sub(rf'<h{n}[^>]*>(.*?)</h{n}>', lambda m: '\n' + ('#' * n) + ' ' + re.sub(r'<[^>]+>','',m.group(1)) + '\n', s, flags=re.S)
    # ul/li
    s = re.sub(r'<ul[^>]*>', '\n', s)
    s = re.sub(r'</ul>', '\n', s)
    s = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: '- ' + re.sub(r'<[^>]+>','',m.group(1)).strip() + '\n', s, flags=re.S)
    # a
    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>',
               lambda m: f'[{re.sub(r"<[^>]+>","",m.group(2))}]({m.group(1)})', s, flags=re.S)
    # strong/b
    s = re.sub(r'<(?:strong|b)[^>]*>(.*?)</(?:strong|b)>', r'**\1**', s, flags=re.S)
    # img
    s = re.sub(r'<img[^>]*src="([^"]+)"[^>]*/?>', r'![](\1)', s)
    # br/p
    s = re.sub(r'<br\s*/?>', '\n', s)
    s = re.sub(r'</p>', '\n\n', s)
    s = re.sub(r'<p[^>]*>', '', s)
    # remaining tags
    s = re.sub(r'<[^>]+>', '', s)
    # entities
    s = s.replace('&nbsp;',' ').replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')
    # normalize blanks
    s = re.sub(r'\n{3,}', '\n\n', s).strip()
    return s

def post_to_qiita(token, title, body, tags, draft=True):
    payload = {
        "title": title,
        "body": body,
        "tags": tags,
        "private": draft,  # private=true → 限定公開（下書き相当）
        "tweet": False,
    }
    status, js = http_json("https://qiita.com/api/v2/items",
                           method="POST",
                           headers={"Authorization": f"Bearer {token}"},
                           data=payload)
    return status, js

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True, choices=list(SITES.keys()))
    ap.add_argument("--limit", type=int, default=1)
    ap.add_argument("--draft", action="store_true", default=True)
    ap.add_argument("--public", action="store_true", help="即公開（デフォルトは限定公開＝下書き）")
    args = ap.parse_args()

    site_cfg = SITES[args.site]
    user = os.environ.get(site_cfg["user_env"])
    pw   = os.environ.get(site_cfg["pass_env"])
    qtok = os.environ.get(site_cfg["qiita_token_env"])
    if not all([user, pw, qtok]):
        print(f"missing env: {site_cfg['user_env']}/{site_cfg['pass_env']}/{site_cfg['qiita_token_env']}",
              file=sys.stderr)
        sys.exit(1)

    state = load_state()
    posted_map = state["posted"].setdefault(args.site, {})

    posts = fetch_wp_posts(site_cfg, user, pw, limit=20)
    candidates = [p for p in posts if str(p["id"]) not in posted_map]
    if not candidates:
        print("no new posts to cross-post")
        return
    print(f"found {len(candidates)} unposted, will post up to {args.limit}")

    pub = not args.draft if args.public else False
    posted = 0
    for p in candidates[:args.limit]:
        title = re.sub(r'<[^>]+>', '', p["title"]["rendered"])
        original_url = p["link"]
        intro = (
            f"> 元記事: [{title}]({original_url})\n"
            f"> このQiita版は要約版です。全文・最新情報は元記事をご覧ください。\n\n---\n\n"
        )
        body_md = intro + html_to_md(p["content"]["rendered"])
        if len(body_md) > 200000:
            body_md = body_md[:200000] + "\n\n…（続きは元記事へ）"
        status, resp = post_to_qiita(qtok, title, body_md, site_cfg["default_tags"], draft=not pub)
        if status in (200, 201):
            url = resp.get("url") if isinstance(resp, dict) else ""
            posted_map[str(p["id"])] = {"url": url, "ts": int(time.time())}
            print(f"  posted: {title[:50]} -> {url}")
            posted += 1
            time.sleep(2)
        else:
            print(f"  ERROR {status}: {str(resp)[:200]}")
            break

    save_state(state)
    print(f"posted total: {posted}")

if __name__ == "__main__":
    main()

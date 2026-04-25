"""3アフィリサイトの記事 modified_date を月1で軽微更新（鮮度シグナル付与）。
CONTENT は変更せず modifiedGmt のみ更新する。
GitHub Actions の月次cronから呼ばれる。"""
import os, sys, base64, json, time
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
import urllib.error

SITES = [
    {
        "label": "biz-english-ai",
        "wp":   "https://biz-english-ai.com",
        "user_env": "WP_BIZENGLISHAI_USER",
        "pass_env": "WP_BIZENGLISHAI_PASS",
    },
    {
        "label": "ai-gyomu",
        "wp":   "https://ai-gyomu.jp",
        "user_env": "WP_AIGYOMU_USER",
        "pass_env": "WP_AIGYOMU_PASS",
    },
    {
        "label": "side-invest",
        "wp":   "https://side-invest.com",
        "user_env": "WP_SIDEINVEST_USER",
        "pass_env": "WP_SIDEINVEST_PASS",
    },
]

def http(method, url, headers=None, data=None, timeout=30):
    body = json.dumps(data).encode() if data else None
    h = dict(headers or {})
    if body: h.setdefault("Content-Type", "application/json")
    req = Request(url, data=body, headers=h, method=method)
    try:
        with urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode("utf-8") or "null")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")

def refresh_site(s):
    user = os.environ.get(s["user_env"]); pw = os.environ.get(s["pass_env"])
    if not user or not pw:
        print(f"[skip] {s['label']}: creds missing")
        return 0
    auth = "Basic " + base64.b64encode(f"{user}:{pw}".encode()).decode()
    headers = {"Authorization": auth}
    print(f"[{s['label']}] fetching posts")

    posts = []
    page = 1
    while True:
        st, js = http("GET", f"{s['wp']}/wp-json/wp/v2/posts?status=publish&per_page=50&page={page}&_fields=id,modified_gmt", headers=headers)
        if st != 200 or not js: break
        posts.extend(js)
        if len(js) < 50: break
        page += 1
        if page > 6: break

    # Pick the 8 oldest-modified posts (refresh-signal target)
    posts.sort(key=lambda p: p.get("modified_gmt") or "")
    targets = posts[:8]
    now_gmt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    updated = 0
    for p in targets:
        # Update modified_gmt to now (no content change)
        st, _ = http("POST", f"{s['wp']}/wp-json/wp/v2/posts/{p['id']}",
                     headers=headers,
                     data={"modified_gmt": now_gmt})
        if st in (200, 201):
            updated += 1
            print(f"  refreshed id={p['id']}")
            time.sleep(0.4)
    print(f"[{s['label']}] refreshed {updated}/{len(targets)}")
    return updated

def main():
    total = 0
    for s in SITES:
        total += refresh_site(s)
    print(f"\nTOTAL refreshed: {total}")

if __name__ == "__main__":
    main()

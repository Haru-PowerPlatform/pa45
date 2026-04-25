"""GSC API → 3サイトの100位以内記事を取得して dashboard sites/index.html を更新。
GitHub Actions から日次実行される想定。

env:
  GSC_TOKEN_JSON: gsc_token.json の中身（OAuth2 user credentials）
"""
import os, json, re, sys
from datetime import date, timedelta
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[2]
DASH = ROOT / "sites" / "index.html"

SITES = [
    "https://biz-english-ai.com/",
    "https://ai-gyomu.jp/",
    "https://side-invest.com/",
]

def get_creds():
    raw = os.environ.get("GSC_TOKEN_JSON")
    if not raw:
        sys.exit("GSC_TOKEN_JSON env var missing")
    info = json.loads(raw)
    return Credentials.from_authorized_user_info(info)

def fetch_gsc(svc, site, start, end):
    body = {
        "startDate": start.isoformat(),
        "endDate":   end.isoformat(),
        "dimensions": ["query", "page"],
        "rowLimit": 50,
        "orderBy": [{"field": "impressions", "descending": True}],
    }
    try:
        r = svc.searchanalytics().query(siteUrl=site, body=body).execute()
        return r.get("rows", [])
    except Exception as e:
        print(f"  {site}: ERROR {str(e)[:120]}")
        return []

def main():
    creds = get_creds()
    svc = build("searchconsole", "v1", credentials=creds, cache_discovery=False)
    end = date.today() - timedelta(days=2)
    start = end - timedelta(days=28)
    period = f"{start} 〜 {end}"

    pages = {}
    for site in SITES:
        print(f"fetch {site}")
        rows = fetch_gsc(svc, site, start, end)
        for row in rows:
            pos = row.get("position", 0)
            if pos > 100: continue
            url = row["keys"][1]
            e = pages.setdefault(url, {"site": site, "url": url, "best_pos": 999, "imp": 0, "clicks": 0, "queries": []})
            e["best_pos"] = min(e["best_pos"], pos)
            e["imp"] += row.get("impressions", 0)
            e["clicks"] += row.get("clicks", 0)
            e["queries"].append((row["keys"][0], row.get("impressions", 0), pos))
    ranked = sorted(pages.values(), key=lambda x: (x["best_pos"], -x["imp"]))
    print(f"total ranked pages: {len(ranked)}")

    if ranked:
        rows_html = ""
        for r in ranked[:30]:
            top_q = sorted(r["queries"], key=lambda q: -q[1])[0]
            host = r["site"].replace("https://", "").rstrip("/")
            slug = r["url"].replace(r["site"], "/")[:60]
            rows_html += (
                f'<tr><td class="rk-pos">{r["best_pos"]:.1f}</td>'
                f'<td><a href="{r["url"]}" target="_blank" rel="noopener" style="color:#2563eb;text-decoration:none;">{slug}</a>'
                f'<div class="rk-host">{host}</div></td>'
                f'<td class="rk-q">{top_q[0]}</td>'
                f'<td class="rk-imp">{r["imp"]}</td>'
                f'<td class="rk-clk">{r["clicks"]}</td></tr>'
            )
        body = (
            f'<div class="rank-card">'
            f'<p class="rk-period">期間: {period}　／　100位以内に到達した記事を上位順で表示</p>'
            f'<table class="rk-table"><thead><tr>'
            f'<th>順位</th><th>記事</th><th>主要検索語</th><th>表示</th><th>クリック</th>'
            f'</tr></thead><tbody>{rows_html}</tbody></table></div>'
        )
    else:
        body = (
            '<div class="rank-card"><p class="rk-empty">'
            f'⏳ GSCデータ蓄積待ち（期間: {period}）<br>'
            'まだ検索流入が計測されていません。次回更新時に自動反映されます。'
            '</p></div>'
        )

    section = '<h2>🔍 検索ランクin記事（Top 100位以内）</h2>\n' + body + '\n'

    html = DASH.read_text(encoding='utf-8')
    rank_pat = re.compile(r'<h2>🔍 検索ランクin記事.*?</div>\n', flags=re.S)
    if rank_pat.search(html):
        new_html = rank_pat.sub(section, html, count=1)
    else:
        new_html = html.replace('</header>\n', '</header>\n\n' + section + '\n', 1)

    if new_html == html:
        print("no changes")
    else:
        DASH.write_text(new_html, encoding='utf-8')
        print(f"updated {DASH}")

if __name__ == "__main__":
    main()

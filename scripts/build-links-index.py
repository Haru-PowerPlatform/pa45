#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
slides/links.html（全回の資料リンク集＝目次ハブ）を台帳から冪等生成する。

- 正データ＝ data/config/links-index.json（[{vol,title,desc,date}] の配列）
- 台帳が無ければ、現行 slides/links.html の grid を解析して初回ブートストラップする
  （＝いまの見た目/文言を保ったまま台帳化）。
- grid・「第1回〜第N回」・footer「全N回の目次」だけを差し替える。周辺のCSS/検索JSは不変。
- 新しい回は週次タスクが links-index.json に1行追加 → 本スクリプトで再生成。

使い方:
  python scripts/build-links-index.py            # 再生成（台帳が無ければブートストラップ）
  python scripts/build-links-index.py --check     # 差分が出るか確認（書き込まない）
"""
import re, os, json, sys, html

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE   = os.path.join(ROOT, "slides", "links.html")
LEDGER = os.path.join(ROOT, "data", "config", "links-index.json")

GRID_RE = re.compile(r'(<div class="grid" id="grid">\n).*?(\n  </div>\n\n  <p class="empty")', re.S)
CARD_RE = re.compile(
    r'<a class="card( latest)?" href="vol-\d+/links\.html">\s*'
    r'<div class="no"><span class="lbl">第</span><span class="num">(\d+)</span></div>\s*'
    r'<div class="body">\s*'
    r'<p class="t">(.*?)</p>\s*'
    r'<p class="d"><span>(.*?)</span><span class="date">(.*?)</span></p>',
    re.S)


def bootstrap_ledger(page_html):
    rows = []
    for m in CARD_RE.finditer(page_html):
        _latest, num, title, desc, date = m.groups()
        title = re.sub(r'\s*<span class="badge-new">最新</span>\s*', '', title).strip()
        rows.append({"vol": int(num), "title": html.unescape(title).strip(),
                     "desc": html.unescape(desc).strip(), "date": date.strip()})
    rows.sort(key=lambda r: r["vol"], reverse=True)
    return rows


def render_card(row, is_latest):
    cls = "card latest" if is_latest else "card"
    badge = ' <span class="badge-new">最新</span>' if is_latest else ""
    v = row["vol"]
    esc = lambda s: html.escape(s, quote=False)
    return (
        f'    <a class="{cls}" href="vol-{v:02d}/links.html">\n'
        f'      <div class="no"><span class="lbl">第</span><span class="num">{v}</span></div>\n'
        f'      <div class="body">\n'
        f'        <p class="t">{esc(row["title"])}{badge}</p>\n'
        f'        <p class="d"><span>{esc(row["desc"])}</span>'
        f'<span class="date">{esc(row["date"])}</span></p>\n'
        f'      </div>\n'
        f'      <span class="go">開く →</span>\n'
        f'    </a>'
    )


def main():
    check = "--check" in sys.argv
    page = open(PAGE, encoding="utf-8").read()

    if os.path.exists(LEDGER):
        rows = json.load(open(LEDGER, encoding="utf-8"))
    else:
        rows = bootstrap_ledger(page)
        os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
        json.dump(rows, open(LEDGER, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"[bootstrap] {LEDGER} を現行HTMLから作成（{len(rows)}件）")

    rows = sorted(rows, key=lambda r: r["vol"], reverse=True)
    if not rows:
        print("[skip] 台帳が空"); return
    maxvol = rows[0]["vol"]
    cards = "\n\n".join(render_card(r, r["vol"] == maxvol) for r in rows)

    new = GRID_RE.sub(lambda m: m.group(1) + "\n" + cards + "\n" + m.group(2), page)
    new = re.sub(r'第1回〜第\d+回', f'第1回〜第{maxvol}回', new)
    new = re.sub(r'全\d+回の目次', f'全{maxvol}回の目次', new)

    if new == page:
        print("[ok] 差分なし（最新）"); return
    if check:
        print("[check] 差分あり（未書き込み）"); return
    open(PAGE, "w", encoding="utf-8").write(new)
    print(f"[ok] slides/links.html を再生成（全{maxvol}回・{len(rows)}カード）")


if __name__ == "__main__":
    main()

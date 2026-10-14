"""ホーム（index.html）の「次回」2か所と「過去回の資料」直近3回を data/config/upcoming-event.json から冪等に書き換える。

対象:
  - ヒーロー下の「次回」タイトル＋ボタン（<!-- NEXT_EVENT_HERO:START/END -->）
  - 「次回講座（PA45）」カード（<!-- NEXT_EVENT_CARD:START/END -->）
  - 過去回の資料 直近3回＋「すべての回を見る」ボタン（<!-- BACKNUMBER:START/END -->、links-index.json から）

upcoming-event.json を次回へ進めれば、夜間ジョブでホームも追従する。
使い方: python scripts/sync-home-next-event.py
"""
import json
import re
import subprocess
import sys
from datetime import date
from html import escape as html_escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
UPCOMING = ROOT / "data" / "config" / "upcoming-event.json"
LINKS_INDEX = ROOT / "data" / "config" / "links-index.json"


def tracked(path: str) -> bool:
    r = subprocess.run(["git", "ls-files", "--error-unmatch", path], cwd=ROOT,
                       capture_output=True)
    return r.returncode == 0


def hero_block(ev: dict) -> str:
    vol = ev["vol"]
    lines = [
        '<!-- NEXT_EVENT_HERO:START -->',
        f'          <div class="hero-next-title">{ev["date_label"]}{ev["time"]} ── {ev["title"]}</div>',
        '          <div class="hero-next-actions">',
        f'            <a href="{ev["connpass_url"]}" target="_blank" rel="noopener" class="btn-small">connpass で参加登録する →</a>',
    ]
    if tracked(f"slides/vol-{vol}/index.html"):
        lines.append(
            f'            <a href="https://haru-powerplatform.github.io/pa45/slides/vol-{vol}/" target="_blank" rel="noopener" class="btn-small btn-small-ghost">📄 第{vol}回の解説スライドを開く →</a>')
    lines += ['          </div>', '          <!-- NEXT_EVENT_HERO:END -->']
    return "\n".join(lines)


def card_block(ev: dict) -> str:
    vol = ev["vol"]
    prev = vol - 1
    y, m, d = (int(x) for x in ev["date_iso"].split("-"))
    btns = []
    if tracked(f"slides/vol-{prev}/index.html"):
        btns.append(f'      <a href="slides/vol-{prev}/" target="_blank" rel="noopener" style="font-size:12px;font-weight:600;background:var(--c-blue-bg);color:var(--c-blue-text);padding:7px 14px;border-radius:8px;">📄 前回（第{prev}回）のスライド</a>')
    if tracked(f"slides/vol-{prev}/links.html"):
        btns.append(f'      <a href="slides/vol-{prev}/links.html" target="_blank" rel="noopener" style="font-size:12px;font-weight:600;border:1px solid rgba(42,125,212,.35);color:var(--c-blue-mid);padding:7px 14px;border-radius:8px;">📎 資料リンク集</a>')
    lines = [
        '<!-- NEXT_EVENT_CARD:START -->',
        f'    <a href="{ev["connpass_url"]}" target="_blank" rel="noopener" class="card event-card" style="display:flex;">',
        '      <div class="event-date-box">',
        f'        <div class="event-day">{d}</div>',
        f'        <div class="event-mon">{m}月</div>',
        '      </div>',
        '      <div class="event-info">',
        f'        <div class="event-title">{ev["title"]}</div>',
        f'        <div class="event-meta">{y}年{m}月{d}日（{ev["weekday"]}）{ev["time_range"]} · オンライン · 無料</div>',
        '      </div>',
        '      <span class="event-badge">受付中</span>',
        '      <span style="font-size:18px;color:var(--c-hint);margin-left:4px;">›</span>',
        '    </a>',
    ]
    if btns:
        lines += ['    <div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;">', *btns, '    </div>']
    lines.append('    <!-- NEXT_EVENT_CARD:END -->')
    return "\n".join(lines)


def backnumber_block(ev: dict) -> str:
    """開催済みの直近3回カード＋「すべての回を見る」大ボタン（台帳 links-index.json から）。"""
    rows = json.loads(LINKS_INDEX.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    past = sorted((r for r in rows if r["date"] < today and r["vol"] < ev["vol"]),
                  key=lambda r: r["vol"], reverse=True)
    lines = ['<!-- BACKNUMBER:START -->',
             '    <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;" class="backnumber-grid">']
    for r in past[:3]:
        v = r["vol"]
        slide = ""
        if tracked(f"slides/vol-{v}/index.html"):
            slide = (f'          <a href="slides/vol-{v}/" target="_blank" rel="noopener" style="flex:1;text-align:center;font-size:12px;font-weight:600;background:var(--c-blue-bg);color:var(--c-blue-text);padding:7px 4px;border-radius:8px;">📄 スライド</a>\n')
        if tracked(f"slides/vol-{v}/links.html"):
            slide += (f'          <a href="slides/vol-{v}/links.html" target="_blank" rel="noopener" style="flex:1;text-align:center;font-size:12px;font-weight:600;border:1px solid rgba(42,125,212,.35);color:var(--c-blue-mid);padding:7px 4px;border-radius:8px;">📎 資料</a>\n')
        lines += [
            '',
            '      <div class="card" style="padding:16px;display:flex;flex-direction:column;gap:6px;">',
            f'        <span style="align-self:flex-start;font-size:11px;font-weight:700;color:#fff;background:var(--c-blue-mid);padding:2px 9px;border-radius:20px;">Vol.{v}</span>',
            f'        <div style="font-size:13px;font-weight:700;line-height:1.5;">{html_escape(r["title"])}</div>',
            f'        <div style="font-size:11px;color:var(--c-hint);">{r["date"]}</div>',
            '        <div style="display:flex;gap:8px;margin-top:auto;padding-top:8px;">',
            slide.rstrip("\n"),
            '        </div>',
            '      </div>',
        ]
    n = len(past)
    lines += [
        '',
        '    </div>',
        '    <a href="sessions/#archive" class="all-sessions-cta">',
        f'      <span>📚 第1回〜第{past[0]["vol"] if past else 1}回 すべての回を見る<small>全{n}回ぶんの解説スライド・サンプルフロー・録画</small></span>',
        '      <span class="arrow">→</span>',
        '    </a>',
        '    <!-- BACKNUMBER:END -->',
    ]
    return "\n".join(lines)


def replace(html: str, name: str, block: str) -> str:
    pat = re.compile(rf"<!-- {name}:START -->.*?<!-- {name}:END -->", re.S)
    if not pat.search(html):
        sys.exit(f"index.html に {name} のマーカーが無い")
    return pat.sub(lambda _: block, html, count=1)


def main():
    ev = json.loads(UPCOMING.read_text(encoding="utf-8"))
    raw = INDEX.read_bytes()
    crlf = b"\r\n" in raw
    html = raw.decode("utf-8").replace("\r\n", "\n")
    new = replace(html, "NEXT_EVENT_HERO", hero_block(ev))
    new = replace(new, "NEXT_EVENT_CARD", card_block(ev))
    new = replace(new, "BACKNUMBER", backnumber_block(ev))
    if new == html:
        print(f"ホーム次回欄: 変更なし（第{ev['vol']}回）")
        return
    if crlf:
        new = new.replace("\n", "\r\n")
    INDEX.write_bytes(new.encode("utf-8"))
    print(f"ホーム次回欄: 第{ev['vol']}回 に更新")


if __name__ == "__main__":
    main()

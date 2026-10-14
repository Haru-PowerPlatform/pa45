"""ホーム（index.html）の「次回」2か所と「過去回の資料」直近3回を
data/config/upcoming-event.json / data/config/links-index.json から冪等に書き換える。

対象:
  - ヒーロー下の「次回」タイトル＋ボタン（<!-- NEXT_EVENT_HERO:START/END -->）
  - 「次回講座（PA45）」カード（<!-- NEXT_EVENT_CARD:START/END -->）
  - 過去回の資料 直近3回＋「すべての回を見る」ボタン（<!-- BACKNUMBER:START/END -->）
  - ヒーローの実績（開催回数・累計参加者・平均理解度）を data/insights.json から

upcoming-event.json を次回へ進めればホームも追従する。
空（{}）・開催日が過ぎている・キーが欠けている場合も落ちずに「準備中」表示にする。
夜間ジョブ（nightly-site-refresh.ps1）と GitHub Actions（post-event-auto.yml）から呼ばれる。
使い方: python scripts/sync-home-next-event.py
"""
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape as html_escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
UPCOMING = ROOT / "data" / "config" / "upcoming-event.json"
LINKS_INDEX = ROOT / "data" / "config" / "links-index.json"
INSIGHTS = ROOT / "data" / "insights.json"
CONNPASS_GROUP = "https://powerautomate-create.connpass.com/"
WEEKDAYS = "月火水木金土日"


def today_jst() -> date:
    # GitHub Actions は UTC で動くので JST に寄せる
    return datetime.now(timezone(timedelta(hours=9))).date()


def tracked(path: str) -> bool:
    r = subprocess.run(["git", "ls-files", "--error-unmatch", path], cwd=ROOT,
                       capture_output=True)
    return r.returncode == 0


def load_upcoming() -> dict | None:
    """表示に使える次回イベントを返す。無い・終わっている場合は None。"""
    try:
        ev = json.loads(UPCOMING.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None
    if not ev.get("vol"):
        return None
    d = None
    try:
        d = date.fromisoformat(str(ev.get("date_iso", "")))
    except ValueError:
        pass
    if d and d < today_jst():
        return None  # 開催日を過ぎた回は「次回」に出さない
    vol = ev["vol"]
    url = ev.get("connpass_url") or (
        f"{CONNPASS_GROUP}event/{ev['event_id']}/" if ev.get("event_id") else CONNPASS_GROUP)
    time = ev.get("time", "20:15")
    out = {
        "vol": vol,
        "date": d,
        "url": url,
        "time": time,
        "time_range": ev.get("time_range", f"{time}〜21:00"),
        "title": ev.get("title") or f"PA45 第{vol}回：{ev.get('theme', '')}".rstrip("："),
    }
    if d:
        out["date_label"] = ev.get("date_label") or f"{d.month}月{d.day}日（{WEEKDAYS[d.weekday()]}）"
        out["weekday"] = ev.get("weekday") or WEEKDAYS[d.weekday()]
    else:
        out["date_label"] = (ev.get("date_label") or ev.get("date") or "日程調整中") + " "
    return out


def past_sessions(ev: dict | None) -> list:
    rows = json.loads(LINKS_INDEX.read_text(encoding="utf-8"))
    today = today_jst().isoformat()
    return sorted((r for r in rows
                   if r.get("date", "9999") <= today and (ev is None or r["vol"] < ev["vol"])),
                  key=lambda r: r["vol"], reverse=True)


def hero_block(ev: dict | None) -> str:
    lines = ['<!-- NEXT_EVENT_HERO:START -->']
    if ev:
        vol = ev["vol"]
        lines += [
            f'          <div class="hero-next-title">{ev["date_label"]}{ev["time"]} ── {html_escape(ev["title"])}</div>',
            '          <div class="hero-next-actions">',
            f'            <a href="{ev["url"]}" target="_blank" rel="noopener" class="btn-small">connpass で参加登録する →</a>',
        ]
        if tracked(f"slides/vol-{vol}/index.html"):
            lines.append(
                f'            <a href="https://haru-powerplatform.github.io/pa45/slides/vol-{vol}/" target="_blank" rel="noopener" class="btn-small btn-small-ghost">📄 第{vol}回の解説スライドを開く →</a>')
    else:
        lines += [
            '          <div class="hero-next-title">次回の日程は準備中です（毎週木曜 20:15〜開催）</div>',
            '          <div class="hero-next-actions">',
            f'            <a href="{CONNPASS_GROUP}" target="_blank" rel="noopener" class="btn-small">connpass グループをフォローする →</a>',
        ]
    lines += ['          </div>', '          <!-- NEXT_EVENT_HERO:END -->']
    return "\n".join(lines)


def card_block(ev: dict | None, past: list) -> str:
    lines = ['<!-- NEXT_EVENT_CARD:START -->']
    if ev:
        d = ev["date"]
        day, mon = (str(d.day), f"{d.month}月") if d else ("─", "調整中")
        when = f"{d.year}年{d.month}月{d.day}日（{ev['weekday']}）" if d else "日程調整中 "
        lines += [
            f'    <a href="{ev["url"]}" target="_blank" rel="noopener" class="card event-card" style="display:flex;">',
            '      <div class="event-date-box">',
            f'        <div class="event-day">{day}</div>',
            f'        <div class="event-mon">{mon}</div>',
            '      </div>',
            '      <div class="event-info">',
            f'        <div class="event-title">{html_escape(ev["title"])}</div>',
            f'        <div class="event-meta">{when}{ev["time_range"]} · オンライン · 無料</div>',
            '      </div>',
            '      <span class="event-badge">受付中</span>',
        ]
    else:
        lines += [
            f'    <a href="{CONNPASS_GROUP}" target="_blank" rel="noopener" class="card event-card" style="display:flex;">',
            '      <div class="event-date-box">',
            '        <div class="event-day">木</div>',
            '        <div class="event-mon">毎週</div>',
            '      </div>',
            '      <div class="event-info">',
            '        <div class="event-title">次回の日程は準備中です</div>',
            '        <div class="event-meta">毎週木曜 20:15〜21:00 · オンライン · 無料 · connpass で告知します</div>',
            '      </div>',
            '      <span class="event-badge">準備中</span>',
        ]
    lines += [
        '      <span style="font-size:18px;color:var(--c-hint);margin-left:4px;">›</span>',
        '    </a>',
    ]
    btns = []
    if past:
        prev = past[0]["vol"]
        if tracked(f"slides/vol-{prev}/index.html"):
            btns.append(f'      <a href="slides/vol-{prev}/" target="_blank" rel="noopener" style="font-size:12px;font-weight:600;background:var(--c-blue-bg);color:var(--c-blue-text);padding:7px 14px;border-radius:8px;">📄 前回（第{prev}回）のスライド</a>')
        if tracked(f"slides/vol-{prev}/links.html"):
            btns.append(f'      <a href="slides/vol-{prev}/links.html" target="_blank" rel="noopener" style="font-size:12px;font-weight:600;border:1px solid rgba(42,125,212,.35);color:var(--c-blue-mid);padding:7px 14px;border-radius:8px;">📎 資料リンク集</a>')
    if btns:
        lines += ['    <div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;">', *btns, '    </div>']
    lines.append('    <!-- NEXT_EVENT_CARD:END -->')
    return "\n".join(lines)


def backnumber_block(past: list) -> str:
    """開催済みの直近3回カード＋「すべての回を見る」大ボタン。"""
    lines = ['<!-- BACKNUMBER:START -->',
             '    <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;" class="backnumber-grid">']
    for r in past[:3]:
        v = r["vol"]
        btns = []
        if tracked(f"slides/vol-{v}/index.html"):
            btns.append(f'          <a href="slides/vol-{v}/" target="_blank" rel="noopener" style="flex:1;text-align:center;font-size:12px;font-weight:600;background:var(--c-blue-bg);color:var(--c-blue-text);padding:7px 4px;border-radius:8px;">📄 スライド</a>')
        if tracked(f"slides/vol-{v}/links.html"):
            btns.append(f'          <a href="slides/vol-{v}/links.html" target="_blank" rel="noopener" style="flex:1;text-align:center;font-size:12px;font-weight:600;border:1px solid rgba(42,125,212,.35);color:var(--c-blue-mid);padding:7px 4px;border-radius:8px;">📎 資料</a>')
        lines += [
            '',
            '      <div class="card" style="padding:16px;display:flex;flex-direction:column;gap:6px;">',
            f'        <span style="align-self:flex-start;font-size:11px;font-weight:700;color:#fff;background:var(--c-blue-mid);padding:2px 9px;border-radius:20px;">Vol.{v}</span>',
            f'        <div style="font-size:13px;font-weight:700;line-height:1.5;">{html_escape(r["title"])}</div>',
            f'        <div style="font-size:11px;color:var(--c-hint);">{r["date"]}</div>',
            '        <div style="display:flex;gap:8px;margin-top:auto;padding-top:8px;">',
            *btns,
            '        </div>',
            '      </div>',
        ]
    last = past[0]["vol"] if past else 1
    lines += [
        '',
        '    </div>',
        '    <a href="sessions/#archive" class="all-sessions-cta">',
        f'      <span>📚 第1回〜第{last}回 すべての回を見る<small>全{len(past)}回ぶんの解説スライド・サンプルフロー・録画</small></span>',
        '      <span class="arrow">→</span>',
        '    </a>',
        '    <!-- BACKNUMBER:END -->',
    ]
    return "\n".join(lines)


def sync_hero_stats(html: str) -> str:
    """ヒーローの実績3つを insights.json の集計に合わせる（手書きのまま古くなるのを防ぐ）。"""
    try:
        s = json.loads(INSIGHTS.read_text(encoding="utf-8"))["summary"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return html
    vals = {"PA45開催": f"{s['sessions']}回", "累計参加者": f"{s['participants_total']}名+",
            "平均理解度": f"{round(s['understanding_avg'])}%"}
    for label, v in vals.items():
        html = re.sub(rf'(<div class="hero-stat-n">)[^<]*(</div>\s*<div class="hero-stat-l">{label}</div>)',
                      lambda m: m.group(1) + v + m.group(2), html, count=1)
    return html


def replace(html: str, name: str, block: str) -> str:
    pat = re.compile(rf"<!-- {name}:START -->.*?<!-- {name}:END -->", re.S)
    if not pat.search(html):
        sys.exit(f"index.html に {name} のマーカーが無い")
    return pat.sub(lambda _: block, html, count=1)


def main():
    ev = load_upcoming()
    past = past_sessions(ev)
    raw = INDEX.read_bytes()
    crlf = b"\r\n" in raw
    html = raw.decode("utf-8").replace("\r\n", "\n")
    new = replace(html, "NEXT_EVENT_HERO", hero_block(ev))
    new = replace(new, "NEXT_EVENT_CARD", card_block(ev, past))
    new = replace(new, "BACKNUMBER", backnumber_block(past))
    new = sync_hero_stats(new)
    label = f"第{ev['vol']}回" if ev else "準備中"
    if new == html:
        print(f"ホーム次回欄: 変更なし（{label}）")
        return
    if crlf:
        new = new.replace("\n", "\r\n")
    INDEX.write_bytes(new.encode("utf-8"))
    print(f"ホーム次回欄: {label} に更新")


if __name__ == "__main__":
    main()

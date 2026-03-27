"""
PA45 毎日のTODOメール生成 & 送信スクリプト

使い方:
  python scripts/daily-todo.py            # コンソール表示のみ
  python scripts/daily-todo.py --send     # Gmailで送信
  python scripts/daily-todo.py --preview  # HTMLプレビューをブラウザで表示

環境変数:
  EMAIL_FROM      送信元Gmailアドレス
  EMAIL_PASSWORD  Gmailアプリパスワード
  EMAIL_TO        受信先メールアドレス
"""

import sys, io, json, os, re, argparse
from pathlib import Path
from datetime import date, datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
ACTIVITIES_DIR = ROOT / "data" / "activities"
INDEX_PATH     = ROOT / "data" / "meta" / "activities-index.json"
UPCOMING_PATH  = ROOT / "data" / "meta" / "upcoming-events.json"
SURVEYS_DIR    = ROOT / "data" / "surveys"

# ──────────────────────────────────────────────────────────────
# データ読み込み
# ──────────────────────────────────────────────────────────────

def load_activities():
    if not INDEX_PATH.exists():
        return []
    paths = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    acts = []
    for p in paths:
        fp = ROOT / p
        if fp.exists():
            acts.append(json.loads(fp.read_text(encoding="utf-8")))
    return acts

def load_upcoming():
    if not UPCOMING_PATH.exists():
        return []
    return json.loads(UPCOMING_PATH.read_text(encoding="utf-8"))

def load_survey(vol: int):
    for name in [f"vol-{vol}.json", f"vol-{vol:02d}.json"]:
        fp = SURVEYS_DIR / name
        if fp.exists():
            return json.loads(fp.read_text(encoding="utf-8"))
    return None

# ──────────────────────────────────────────────────────────────
# TODO生成
# ──────────────────────────────────────────────────────────────

def build_todo():
    today      = date.today()
    weekday_jp = ["月", "火", "水", "木", "金", "土", "日"][today.weekday()]
    activities = load_activities()
    upcoming   = load_upcoming()

    todos_urgent = []   # 🔥 今日必ずやること
    todos_soon   = []   # 📅 期限あり（PA45関連）
    todos_backlog= []   # ⚠️ 積み残し
    todos_weekly = []   # 💡 今週中に

    # ── Xスライド（毎日） ───────────────────────────────────────
    x_acts = [a for a in activities if a.get("type") == "X"]
    vols = []
    for a in x_acts:
        m = re.search(r"Vol\.(\d+)", a.get("title", ""))
        if m:
            vols.append(int(m.group(1)))
    next_x_vol = max(vols) + 1 if vols else 1
    todos_urgent.append(f"Xスライド Vol.{next_x_vol} を作成して投稿する")

    # ── 次回PA45イベント ─────────────────────────────────────────
    next_event = None
    for ev in upcoming:
        try:
            ev_date = datetime.strptime(ev["date"], "%Y-%m-%d").date()
        except Exception:
            continue
        days_left = (ev_date - today).days
        if days_left < 0:
            continue
        next_event = {**ev, "days_left": days_left, "ev_date": ev_date}
        break

    if next_event:
        d = next_event["days_left"]
        vol = next_event.get("vol", "?")
        theme = next_event.get("theme", "")
        ev_date_str = next_event["ev_date"].strftime("%m/%d")
        connpass_url = next_event.get("connpass_url", "")

        if d == 0:
            todos_urgent += [
                f"【本日PA45 第{vol}回！】Teams会議を開始する",
                "画面共有・Power Automate環境を確認する",
                "参加者数をメモしておく（後でJSONに使う）",
            ]
        elif d == 1:
            todos_urgent += [
                f"スライド最終確認（明日 第{vol}回：{theme}）",
                "Teams会議URLの動作確認",
                f"X告知投稿をする → connpass: {connpass_url}",
            ]
        elif d <= 3:
            todos_soon += [
                f"第{vol}回 スライド仕上げ（{ev_date_str}まで あと{d}日）",
                f"Teams URL確認・connpass告知文を確認",
            ]
        elif d <= 7:
            todos_soon += [
                f"第{vol}回「{theme}」スライド作成中？（{ev_date_str} あと{d}日）",
                f"connpassイベントページを公開済みか確認",
            ]
        else:
            todos_weekly.append(f"第{vol}回「{theme}」の準備を始める（{ev_date_str} あと{d}日）")

    # ── 開催済みの積み残し確認 ────────────────────────────────────
    pa45_acts = sorted(
        [a for a in activities if a.get("type") == "PA45"],
        key=lambda x: x.get("date", "")
    )
    for a in pa45_acts:
        vol_label = a.get("title", "").replace("PA45 第", "").split("回")[0]
        ev = a.get("evidence", {})
        if not ev.get("blog"):
            todos_backlog.append(f"第{vol_label}回：ブログ記事を書いて公開する")
        if not ev.get("youtube"):
            todos_backlog.append(f"第{vol_label}回：YouTube動画をアップロード・公開する")
        if not ev.get("slide"):
            todos_backlog.append(f"第{vol_label}回：スライドをGitHub Pagesに公開する")

    # ── 今週中タスク ─────────────────────────────────────────────
    # WordPress下書きが多い場合
    todos_weekly.append("WordPress下書きから1本、内容を整えて公開する")

    # 月曜なら週次ダイジェスト
    if today.weekday() == 0:
        todos_urgent.insert(0, "週次ダイジェストを確認する → python scripts/weekly-digest.py")

    return {
        "today": today,
        "weekday_jp": weekday_jp,
        "next_event": next_event,
        "todos_urgent": todos_urgent,
        "todos_soon": todos_soon,
        "todos_backlog": todos_backlog,
        "todos_weekly": todos_weekly,
        "stats": {
            "pa45_count": len(pa45_acts),
            "total_participants": sum(a.get("participants", 0) for a in pa45_acts),
            "activity_count": len(activities),
        }
    }

# ──────────────────────────────────────────────────────────────
# テキスト形式
# ──────────────────────────────────────────────────────────────

def render_text(data):
    lines = []
    today_str = data["today"].strftime(f"%Y-%m-%d（{data['weekday_jp']}）")
    lines.append(f"📋 PA45 本日のTODO  {today_str}")
    lines.append("=" * 52)

    def section(icon, title, items):
        if not items:
            return
        lines.append(f"\n{icon} {title}")
        for item in items:
            lines.append(f"  □ {item}")

    section("🔥", "今日やること（最優先）", data["todos_urgent"])
    section("📅", "期限あり（今週）",        data["todos_soon"])
    section("⚠️ ", "積み残し",                data["todos_backlog"])
    section("💡", "今週中に",                data["todos_weekly"])

    lines.append("\n" + "─" * 52)
    s = data["stats"]
    ne = data["next_event"]
    lines.append(f"📊 PA45: {s['pa45_count']}回開催 / 累計{s['total_participants']}名参加")
    if ne:
        lines.append(f"📅 次回: 第{ne.get('vol')}回「{ne.get('theme')}」"
                     f"{ne['ev_date'].strftime('%m/%d')} あと{ne['days_left']}日")
    lines.append("=" * 52)
    return "\n".join(lines)

# ──────────────────────────────────────────────────────────────
# HTML形式（メール用）
# ──────────────────────────────────────────────────────────────

def render_html(data):
    today_str = data["today"].strftime(f"%Y年%m月%d日（{data['weekday_jp']}）")

    def section_html(icon, title, items, color):
        if not items:
            return ""
        rows = "".join(
            f'<tr><td style="padding:4px 0 4px 8px;font-size:15px;color:#333;">'
            f'☐ {item}</td></tr>'
            for item in items
        )
        return f"""
<div style="margin:16px 0;">
  <div style="background:{color};border-radius:8px 8px 0 0;padding:8px 14px;">
    <strong style="font-size:14px;color:#fff;">{icon} {title}</strong>
  </div>
  <table style="width:100%;border-collapse:collapse;background:#fafafa;
                border:1px solid #e0e0e0;border-top:none;border-radius:0 0 8px 8px;">
    {rows}
  </table>
</div>"""

    s = data["stats"]
    ne = data["next_event"]
    next_event_html = ""
    if ne:
        next_event_html = (
            f'<span style="font-size:13px;color:#555;">📅 次回 第{ne.get("vol")}回'
            f'「{ne.get("theme")}」{ne["ev_date"].strftime("%m/%d")} あと{ne["days_left"]}日</span>'
        )

    body = f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8">
<title>PA45 TODO</title></head>
<body style="font-family:'Hiragino Sans',Meiryo,sans-serif;max-width:600px;
             margin:0 auto;padding:20px;background:#f5f5f5;">

<div style="background:#1a1a2e;border-radius:12px;padding:16px 20px;margin-bottom:20px;">
  <h1 style="margin:0;font-size:20px;color:#fff;">📋 PA45 本日のTODO</h1>
  <p style="margin:4px 0 0;font-size:14px;color:#aaa;">{today_str}</p>
</div>

{section_html("🔥", "今日やること（最優先）", data["todos_urgent"], "#c0392b")}
{section_html("📅", "期限あり・今週", data["todos_soon"], "#2980b9")}
{section_html("⚠️", "積み残し", data["todos_backlog"], "#e67e22")}
{section_html("💡", "今週中に", data["todos_weekly"], "#27ae60")}

<div style="margin-top:20px;padding:12px 16px;background:#fff;
            border-radius:8px;border:1px solid #e0e0e0;font-size:13px;color:#555;">
  📊 PA45: <strong>{s['pa45_count']}回</strong>開催 /
  累計 <strong>{s['total_participants']}名</strong>参加 /
  活動記録 <strong>{s['activity_count']}件</strong><br>
  {next_event_html}
</div>

<p style="margin-top:16px;font-size:11px;color:#999;text-align:center;">
  このメールは daily-todo.py により自動生成されました
</p>
</body></html>"""
    return body

# ──────────────────────────────────────────────────────────────
# Gmail で送信
# ──────────────────────────────────────────────────────────────

def send_gmail(html_body, subject):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    email_from = os.environ.get("EMAIL_FROM", "")
    email_pass = os.environ.get("EMAIL_PASSWORD", "")
    email_to   = os.environ.get("EMAIL_TO", email_from)

    if not all([email_from, email_pass]):
        raise ValueError("EMAIL_FROM / EMAIL_PASSWORD が未設定です")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = email_from
    msg["To"]      = email_to
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_from, email_pass)
        smtp.send_message(msg)

    print(f"✅ Gmail送信完了 → {email_to}（件名: {subject}）")

# ──────────────────────────────────────────────────────────────
# メイン
# ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--send",    action="store_true", help="Outlook下書きを作成する")
    parser.add_argument("--preview", action="store_true", help="HTMLをブラウザで確認する")
    args = parser.parse_args()

    data    = build_todo()
    today   = data["today"]
    subject = f"【PA45 TODO】{today.strftime('%m/%d')}（{data['weekday_jp']}）のやること"

    # 常にコンソール表示
    print(render_text(data))

    if args.preview:
        import tempfile, webbrowser
        with tempfile.NamedTemporaryFile("w", suffix=".html",
                                         encoding="utf-8", delete=False) as f:
            f.write(render_html(data))
            webbrowser.open(f"file://{f.name}")
        print("ブラウザでプレビューを開きました")

    if args.send:
        html = render_html(data)
        send_gmail(html, subject)

if __name__ == "__main__":
    main()

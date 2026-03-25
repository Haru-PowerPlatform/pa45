"""
PA45 ステータスレポート生成スクリプト

使い方:
  python scripts/status.py          # ターミナルに表示
  python scripts/status.py --email  # メール本文として出力（GitHub Actionsから使用）

GitHub Actions から daily-status.yml 経由で毎朝メール送信されます。
"""

import sys
import io
import json
import re
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import date, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
ACTIVITIES_DIR = ROOT / "data" / "activities"
INDEX_PATH = ROOT / "data" / "meta" / "activities-index.json"
UPCOMING_PATH = ROOT / "data" / "meta" / "upcoming-events.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ja,en;q=0.9",
}


def days_until(date_str):
    d = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (d - date.today()).days


def check_url(url):
    """URLにアクセスできるか確認。True=OK, False=NG"""
    try:
        req = urllib.request.Request(url, headers=HEADERS, method="HEAD")
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.status < 400
    except Exception:
        return False


def load_activities():
    if not INDEX_PATH.exists():
        return []
    with open(INDEX_PATH, encoding="utf-8") as f:
        paths = json.load(f)
    activities = []
    for p in paths:
        fp = ROOT / p
        if fp.exists():
            with open(fp, encoding="utf-8") as f:
                activities.append(json.load(f))
    return activities


def load_upcoming():
    if not UPCOMING_PATH.exists():
        return []
    with open(UPCOMING_PATH, encoding="utf-8") as f:
        return json.load(f)


def build_report():
    today = date.today()
    activities = load_activities()
    upcoming = load_upcoming()

    lines = []
    lines.append("=" * 50)
    lines.append(f"  PA45 ステータスレポート  {today}")
    lines.append("=" * 50)

    # ── 次回イベント ────────────────────────────────────────────────────────
    lines.append("")
    lines.append("📅 次回イベント")

    if not upcoming:
        lines.append("  （upcoming-events.json に登録なし）")
    else:
        for ev in upcoming:
            days = days_until(ev["date"])
            if days < 0:
                continue
            lines.append(f"  第{ev['vol']}回：{ev['theme']}")
            lines.append(f"  開催日：{ev['date']}（あと {days} 日）")
            lines.append(f"  connpass：{ev.get('connpass_url', '未登録')}")

            # スライドURL確認
            slide_url = f"https://haru-powerplatform.github.io/pa45/assets/pa45/P{ev['vol']:03d}_PA45_{ev['theme']}_{ev['date'].replace('-', '')}.pptx"
            slide_ok = check_url(slide_url)
            lines.append(f"  {'✅' if slide_ok else '⬜'} スライド{'公開済み' if slide_ok else '未公開'}")

            # 対応するblog下書き確認（WordPressは直接確認できないのでactivitiesのblog URLをチェック）
            act = next((a for a in activities if a.get("connpass_event_id") == int(ev["event_id"])), None)
            blog_url = act.get("evidence", {}).get("blog", "") if act else ""
            if blog_url:
                lines.append(f"  ✅ ブログ公開済み：{blog_url}")
            else:
                lines.append(f"  ⬜ ブログ未公開")

    # ── 過去回サマリー ──────────────────────────────────────────────────────
    lines.append("")
    lines.append("📊 過去回サマリー")

    pa45_acts = sorted(
        [a for a in activities if a.get("type") == "PA45"],
        key=lambda x: x.get("date", "")
    )

    if not pa45_acts:
        lines.append("  （記録なし）")
    else:
        for a in pa45_acts:
            vol = a.get("title", "").replace("PA45 第", "").split("回")[0]
            participants = a.get("participants", "?")
            blog = "✅ブログあり" if a.get("evidence", {}).get("blog") else "⬜ブログなし"
            slide = "✅スライドあり" if a.get("evidence", {}).get("slide") else "⬜スライドなし"
            lines.append(f"  第{vol}回  参加者:{participants}人  {blog}  {slide}")

    # ── 次に作るべき X投稿 Vol ──────────────────────────────────────────────
    lines.append("")
    lines.append("📣 次のX投稿スライド")

    x_acts = [a for a in activities if a.get("type") == "X"]
    if x_acts:
        # Vol番号を title から抽出（例: "Vol.12：Power Automate..." → 12）
        vols = []
        for a in x_acts:
            title = a.get("title", "")
            m = re.search(r"Vol\.(\d+)", title)
            if m:
                vols.append(int(m.group(1)))
        if vols:
            next_vol = max(vols) + 1
            lines.append(f"  現在の最新：Vol.{max(vols)}")
            lines.append(f"  👉 次に作る：Vol.{next_vol}")
        else:
            lines.append("  （Vol番号を取得できませんでした）")
    else:
        lines.append("  X投稿の活動が登録されていません")

    # ── 全活動件数 ──────────────────────────────────────────────────────────
    lines.append("")
    lines.append(f"📁 登録済み活動数：{len(activities)} 件")

    # ── 未完了タスク ────────────────────────────────────────────────────────
    lines.append("")
    lines.append("⚠️  要対応")

    issues = []
    for a in pa45_acts:
        ev_id = a.get("connpass_event_id")
        if not a.get("evidence", {}).get("blog"):
            issues.append(f"  ⬜ 第{a['title'].replace('PA45 第','').split('回')[0]}回：ブログ未公開")
        if not a.get("evidence", {}).get("slide"):
            issues.append(f"  ⬜ 第{a['title'].replace('PA45 第','').split('回')[0]}回：スライドなし")
        if a.get("participants", 0) == 0:
            issues.append(f"  ⬜ 第{a['title'].replace('PA45 第','').split('回')[0]}回：参加者数未確定")
        if not a.get("evidence", {}).get("youtube"):
            issues.append(f"  ⬜ 第{a['title'].replace('PA45 第','').split('回')[0]}回：YouTube動画未アップロード（編集→アップロード→公開）")

    if issues:
        lines.extend(issues)
    else:
        lines.append("  なし 🎉")

    lines.append("")
    lines.append("=" * 50)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", action="store_true", help="メール送信モード（GitHub Actions用）")
    args = parser.parse_args()

    report = build_report()

    if args.email:
        # GitHub Actions からメール送信用に環境変数経由で出力
        import os
        import smtplib
        from email.mime.text import MIMEText

        email_to = os.environ.get("EMAIL_TO", "")
        email_from = os.environ.get("EMAIL_FROM", "")
        email_pass = os.environ.get("EMAIL_PASSWORD", "")

        if not all([email_to, email_from, email_pass]):
            print("環境変数 EMAIL_TO / EMAIL_FROM / EMAIL_PASSWORD が未設定です")
            print(report)
            sys.exit(1)

        msg = MIMEText(report, "plain", "utf-8")
        msg["Subject"] = f"PA45 ステータスレポート {date.today()}"
        msg["From"] = email_from
        msg["To"] = email_to

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_from, email_pass)
            smtp.send_message(msg)

        print("メール送信完了")
    else:
        print(report)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PA45 当日リマインダー X 投稿スクリプト
GitHub Actions から 12:15 JST (03:15 UTC) に自動実行。

今日の日付が data/pa45-sessions.json に登録されていれば投稿。
なければ何もしない。

使い方:
  python scripts/x-pa45-reminder.py
  python scripts/x-pa45-reminder.py --dry-run   # 投稿せず本文だけ表示
"""

import sys, io, os, json, argparse, requests
from datetime import date
from pathlib import Path
from requests_oauthlib import OAuth1

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT          = Path(__file__).parent.parent
SESSIONS_PATH = ROOT / "data" / "pa45-sessions.json"


def get_auth():
    return OAuth1(
        os.environ["X_API_KEY"],
        os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_SECRET"],
    )


def load_today_session():
    """今日の日付に一致するセッションを返す。なければ None。"""
    data = json.loads(SESSIONS_PATH.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    for session in data["sessions"]:
        if session["date"] == today:
            return session
    return None


def build_tweet(session: dict) -> str:
    vol   = session["vol"]
    time  = session["time"]
    theme = session["theme"]
    desc  = session["description"]
    pts   = session.get("points", [])
    url   = session.get("connpass_url", "")

    # ✅ ポイント行
    point_lines = "\n".join(f"✅ {p}" for p in pts)

    tweet = f"""【今日{time}〜｜PA45 Vol.{vol}】

Power Automate初心者向け45分ハンズオン🚀
今日は「{theme}」。

{point_lines}

を組み合わせて
👉 {desc}

途中参加OK／知識ゼロ歓迎🙆‍♂️"""

    if url:
        tweet += f"\n🔗 {url}"

    tweet += "\n\n#PowerAutomate #ローコード #PA45"
    return tweet


def post_tweet(text: str):
    url  = "https://api.twitter.com/2/tweets"
    auth = get_auth()
    resp = requests.post(url, auth=auth, json={"text": text})
    resp.raise_for_status()
    return resp.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="投稿せず本文だけ表示")
    args = parser.parse_args()

    session = load_today_session()
    if session is None:
        print(f"今日（{date.today()}）はPA45の開催日ではありません。スキップ。")
        sys.exit(0)

    text = build_tweet(session)

    print(f"─── PA45 Vol.{session['vol']} リマインダー ───")
    print(f"開催日時: {session['date']} {session['time']}")
    print(f"テーマ: {session['theme']}")
    print(f"文字数: {len(text)}")
    print("本文:")
    print(text)
    print("──────────────────────────────")

    if args.dry_run:
        print("（dry-run: 実際には投稿しません）")
        sys.exit(0)

    result = post_tweet(text)
    tweet_id = result.get("data", {}).get("id", "unknown")
    print(f"✅ 投稿完了 tweet_id={tweet_id}")


if __name__ == "__main__":
    main()

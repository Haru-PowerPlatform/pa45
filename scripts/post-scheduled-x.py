#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スケジュールX投稿スクリプト
GitHub Actions cron から呼び出す。
  - 昼スロット (noon):    JST 12:15 = UTC 03:15
  - 夕スロット (evening): JST 17:30 = UTC 08:30

使い方:
  python scripts/post-scheduled-x.py --slot noon
  python scripts/post-scheduled-x.py --slot evening
"""

import sys, io, os, json, argparse, requests
from datetime import date, datetime
from pathlib import Path
from requests_oauthlib import OAuth1

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
SCHEDULE_PATH = ROOT / "data" / "x-posts-schedule.json"
LOG_PATH      = ROOT / "data" / "x-posts-log.json"

# ── X API v2 認証 ─────────────────────────────────────────────────────────────
def get_auth():
    return OAuth1(
        os.environ["X_API_KEY"],
        os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_TOKEN_SECRET"],
    )

# ── 投稿ログ ──────────────────────────────────────────────────────────────────
def load_log():
    if LOG_PATH.exists():
        return json.loads(LOG_PATH.read_text(encoding="utf-8"))
    return {"posted": []}

def save_log(log):
    LOG_PATH.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")

def already_posted(log, index, slot):
    key = f"{index}:{slot}"
    return key in log.get("posted", [])

def mark_posted(log, index, slot, tweet_id):
    key = f"{index}:{slot}"
    log.setdefault("posted", []).append(key)
    log.setdefault("history", []).append({
        "index": index,
        "slot": slot,
        "tweet_id": tweet_id,
        "posted_at": datetime.utcnow().isoformat() + "Z"
    })

# ── 本日の投稿を選ぶ ───────────────────────────────────────────────────────────
def pick_post(slot: str):
    data = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))
    posts = data["posts"]
    start = date.fromisoformat(data["start_date"])
    today = date.today()

    day_index = (today - start).days
    if day_index < 0:
        print(f"まだ開始日前です（start={start}, today={today}）")
        return None, None

    # posts はペアで並んでいる（noon/evening 交互）
    # post_index = day_index * 2 + (0 if noon, 1 if evening)
    slot_offset = 0 if slot == "noon" else 1
    post_index  = day_index * 2 + slot_offset

    if post_index >= len(posts):
        # リストを使い切ったらループ
        post_index = post_index % len(posts)
        print(f"⚠️ スケジュールをループしています（index={post_index}）")

    post = posts[post_index]
    return post, post_index

# ── ツイート投稿 ──────────────────────────────────────────────────────────────
def post_tweet(text: str):
    url  = "https://api.twitter.com/2/tweets"
    auth = get_auth()
    resp = requests.post(url, auth=auth, json={"text": text})
    resp.raise_for_status()
    return resp.json()

# ── 本文を組み立てる ──────────────────────────────────────────────────────────
def build_text(post: dict) -> str:
    parts = [post["body"].strip()]
    if post.get("hashtags"):
        parts.append("\n" + post["hashtags"])
    if post.get("url"):
        parts.append(post["url"])
    return "\n".join(parts)

# ── メイン ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slot", choices=["noon", "evening"], required=True)
    parser.add_argument("--dry-run", action="store_true", help="投稿せず本文だけ表示")
    args = parser.parse_args()

    post, index = pick_post(args.slot)
    if post is None:
        sys.exit(0)

    text = build_text(post)
    print(f"─── 本日の投稿（{args.slot}）───")
    print(f"テーマ: {post['theme']}")
    print(f"文字数: {len(post['body'])}字")
    print("本文:")
    print(text)
    print("─────────────────────────────")

    if args.dry_run:
        print("（dry-run: 実際には投稿しません）")
        sys.exit(0)

    log = load_log()
    if already_posted(log, index, args.slot):
        print(f"✅ 既に投稿済み（index={index}, slot={args.slot}）—— スキップ")
        sys.exit(0)

    result = post_tweet(text)
    tweet_id = result.get("data", {}).get("id", "unknown")
    print(f"✅ 投稿完了 tweet_id={tweet_id}")

    mark_posted(log, index, args.slot, tweet_id)
    save_log(log)

if __name__ == "__main__":
    main()

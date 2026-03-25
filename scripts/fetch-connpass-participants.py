"""
connpass イベントの参加者数を取得するスクリプト

使い方:
  python scripts/fetch-connpass-participants.py <event_id>
  python scripts/fetch-connpass-participants.py <event_id> --url https://powerautomate-create.connpass.com/event/386395/

event_id のみ指定した場合は、以下の順で試みます:
  1. https://powerautomate-create.connpass.com/event/<id>/
  2. https://connpass.com/event/<id>/
"""

import sys
import io
import re
import urllib.request
import urllib.error
import json
import argparse

# Windows コンソールの文字化け対策
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "ja,en;q=0.9",
}


def fetch_html(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8"), resp.geturl()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, None
        raise


def parse_participants(html):
    # <span class="amount"><span>26</span>人 のパターン（実際のHTML構造）
    match = re.search(r'class="amount"[^>]*>\s*<span[^>]*>\s*(\d+)\s*</span>', html)
    if match:
        return int(match.group(1))

    # フォールバック: "参加者数" の近くにある数字
    match = re.search(r'参加者数[^\d]*(\d+)', html)
    if match:
        return int(match.group(1))

    # さらにフォールバック: accepted カウント（JSON-LD等）
    match = re.search(r'"accepted"\s*:\s*(\d+)', html)
    if match:
        return int(match.group(1))

    return None


def get_participants(event_id, url=None):
    urls_to_try = []
    if url:
        urls_to_try.append(url)
    else:
        urls_to_try = [
            f"https://powerautomate-create.connpass.com/event/{event_id}/",
            f"https://connpass.com/event/{event_id}/",
        ]

    for u in urls_to_try:
        html, final_url = fetch_html(u)
        if html is None:
            continue
        count = parse_participants(html)
        if count is not None:
            return count, final_url

    return None, None


def main():
    parser = argparse.ArgumentParser(description="connpass参加者数取得")
    parser.add_argument("event_id", help="connpassイベントID")
    parser.add_argument("--url", help="イベントURL（省略時は自動判定）", default=None)
    parser.add_argument("--json", action="store_true", help="JSON形式で出力")
    args = parser.parse_args()

    count, url = get_participants(args.event_id, args.url)

    if args.json:
        print(json.dumps({"event_id": args.event_id, "participants": count, "url": url}, ensure_ascii=False))
    elif count is not None:
        print(f"参加者数: {count}人  ({url})")
    else:
        print(f"取得できませんでした（event_id={args.event_id}）", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

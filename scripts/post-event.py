"""
PA45 開催後の自動処理スクリプト

使い方:
  python scripts/post-event.py --vol 4 --event-id 388691 --date 2026-04-02 --theme "Apply to each"

処理内容:
  1. connpassから参加者数を自動取得
  2. data/activities/YYYY-MM-DD-pa45-volN.json を作成/更新
  3. data/meta/activities-index.json を更新
"""

import sys
import io
import re
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
ACTIVITIES_DIR = ROOT / "data" / "activities"
INDEX_PATH = ROOT / "data" / "meta" / "activities-index.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "ja,en;q=0.9",
}


def fetch_participants(event_id):
    urls = [
        f"https://powerautomate-create.connpass.com/event/{event_id}/",
        f"https://connpass.com/event/{event_id}/",
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("utf-8")
                final_url = resp.geturl()
            m = re.search(r'class="amount"[^>]*>\s*<span[^>]*>\s*(\d+)\s*</span>', html)
            if not m:
                m = re.search(r'参加者数[^\d]*(\d+)', html)
            if m:
                return int(m.group(1)), final_url
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
            raise
    return None, None


def update_index(activity_path_str):
    if INDEX_PATH.exists():
        with open(INDEX_PATH, encoding="utf-8") as f:
            index = json.load(f)
    else:
        index = []

    if activity_path_str not in index:
        index.append(activity_path_str)
        index.sort()

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"  index 更新: {INDEX_PATH.name}")


def main():
    parser = argparse.ArgumentParser(description="PA45 開催後処理")
    parser.add_argument("--vol", required=True, type=int, help="回数（例: 4）")
    parser.add_argument("--event-id", required=True, help="connpassイベントID")
    parser.add_argument("--date", required=True, help="開催日 YYYY-MM-DD")
    parser.add_argument("--theme", required=True, help="テーマ名（例: Apply to each）")
    parser.add_argument("--blog", default="", help="ブログ記事URL（省略可）")
    parser.add_argument("--slide", default="", help="スライドURL（省略可）")
    parser.add_argument("--participants", type=int, default=None, help="参加者数（省略時はconnpassから自動取得）")
    args = parser.parse_args()

    print(f"\n=== PA45 第{args.vol}回 開催後処理 ===\n")

    # 1. 参加者数取得
    if args.participants is not None:
        participants = args.participants
        connpass_url = f"https://powerautomate-create.connpass.com/event/{args.event_id}/"
        print(f"  参加者数: {participants}人（手動指定）")
    else:
        print(f"  connpassから参加者数を取得中... (event_id={args.event_id})")
        participants, connpass_url = fetch_participants(args.event_id)
        if participants is None:
            print("  ⚠ 参加者数を取得できませんでした。--participants で手動指定してください。")
            sys.exit(1)
        print(f"  参加者数: {participants}人  ({connpass_url})")

    # 2. スライドURL（省略時はパターンから生成）
    slide_url = args.slide
    if not slide_url:
        vol_str = f"{args.vol:03d}"
        slide_url = f"https://haru-powerplatform.github.io/pa45/assets/pa45/P{vol_str}_PA45_{args.theme}_{args.date.replace('-', '')}.pptx"
        print(f"  スライドURL（自動生成）: {slide_url}")

    # 3. activities JSON 作成
    activity_id = f"{args.date}-pa45-vol{args.vol}"
    filename = f"{activity_id}.json"
    filepath = ACTIVITIES_DIR / filename

    evidence = {"connpass": connpass_url or ""}
    if args.blog:
        evidence["blog"] = args.blog
    if slide_url:
        evidence["slide"] = slide_url

    activity = {
        "id": activity_id,
        "type": "PA45",
        "title": f"PA45 第{args.vol}回：{args.theme}",
        "date": args.date,
        "public": True,
        "summary": f"Power Automate 45 第{args.vol}回。テーマ：{args.theme}",
        "tags": ["PA45", "Power Automate", "ハンズオン"],
        "connpass_event_id": int(args.event_id),
        "participants": participants,
        "evidence": evidence,
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(activity, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"  activity JSON 作成: {filename}")

    # 4. index 更新
    update_index(f"data/activities/{filename}")

    print(f"\n完了！次のステップ:")
    print(f"  git add data/activities/{filename} data/meta/activities-index.json")
    print(f"  git commit -m 'feat: add PA45 Vol.{args.vol} activity'")
    print(f"  git push && gh pr create ...")
    if not args.blog:
        print(f"\n  ※ ブログを書いたら --blog URL を指定して再実行するか、JSONに追記してください")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PA45 当日リマインダー X 投稿スクリプト
GitHub Actions から毎週木曜 12:15 JST (03:15 UTC) に自動実行。

1. connpass API で今日開催の PA45 イベントを検索
2. イベントなし → スキップ（開催なし週は何もしない）
3. イベントあり → OGP画像を取得
4. Claude API（画像認識）でテーマ・内容を自動抽出
5. X に投稿（connpass URL 付き）

使い方:
  python scripts/x-pa45-reminder.py
  python scripts/x-pa45-reminder.py --dry-run   # 投稿せず本文だけ表示
"""

import sys, io, os, json, argparse, base64, re, requests
from datetime import date
from pathlib import Path
from requests_oauthlib import OAuth1

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


# ──────────────────────────────────────────────
# 1. connpass API で今日の PA45 イベントを取得
# ──────────────────────────────────────────────
def find_today_event() -> dict | None:
    today = date.today()
    ymd = today.strftime("%Y%m%d")
    url = f"https://connpass.com/api/v1/event/?keyword=PA45&ymd={ymd}&count=10"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    events = resp.json().get("events", [])

    # PA45 に関係するイベントだけ絞り込む
    for ev in events:
        title = ev.get("title", "")
        if "PA45" in title or "Power Automate 45" in title:
            print(f"✅ 今日のイベント発見: {title}")
            print(f"   URL: {ev['event_url']}")
            return ev

    print(f"今日（{today}）は PA45 の開催日ではありません。スキップ。")
    return None


# ──────────────────────────────────────────────
# 2. connpass イベントページから OGP 画像 URL を取得
# ──────────────────────────────────────────────
def get_ogp_image_url(event_url: str) -> str | None:
    from html.parser import HTMLParser

    class OGPParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.ogp_image = None

        def handle_starttag(self, tag, attrs):
            if tag == "meta":
                attrs_dict = dict(attrs)
                if attrs_dict.get("property") == "og:image":
                    self.ogp_image = attrs_dict.get("content")

    headers = {"User-Agent": "Mozilla/5.0 (compatible; PA45Bot/1.0)"}
    resp = requests.get(event_url, headers=headers, timeout=15)
    parser = OGPParser()
    parser.feed(resp.text)
    return parser.ogp_image


# ──────────────────────────────────────────────
# 3. 画像を base64 に変換
# ──────────────────────────────────────────────
def download_image(image_url: str) -> tuple[str, str]:
    """(base64_data, media_type) を返す"""
    resp = requests.get(image_url, timeout=15)
    resp.raise_for_status()

    content_type = resp.headers.get("Content-Type", "")
    if "jpeg" in content_type or "jpg" in content_type:
        media_type = "image/jpeg"
    elif "png" in content_type:
        media_type = "image/png"
    elif "webp" in content_type:
        media_type = "image/webp"
    elif "gif" in content_type:
        media_type = "image/gif"
    else:
        # URL から推定
        lower = image_url.lower()
        if ".png" in lower:
            media_type = "image/png"
        elif ".webp" in lower:
            media_type = "image/webp"
        else:
            media_type = "image/jpeg"

    data = base64.standard_b64encode(resp.content).decode("utf-8")
    return data, media_type


# ──────────────────────────────────────────────
# 4. Claude API で画像からイベント情報を抽出
# ──────────────────────────────────────────────
def analyze_image_with_claude(img_data: str, media_type: str) -> dict:
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = """このPA45（Power Automate 45分ハンズオン）のイベント告知画像を読み取り、
以下のJSON形式で情報を返してください。JSONのみ返してください。

{
  "vol": 回数（整数。例: 5）,
  "theme": "今回のメインテーマ（15文字以内）",
  "time": "開始時刻（例: 20:15）",
  "points": ["学ぶこと1", "学ぶこと2", "学ぶこと3"],
  "description": "今日作るフローや今日やることの一言説明（30文字以内）"
}

・読み取れない項目は null を入れてください。
・points は画像内のキーワードや「今日やること」から3つ抽出してください。
・JSONのみ返してください（説明文は不要）。"""

    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=600,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": img_data,
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }]
    )

    raw = message.content[0].text.strip()
    # コードブロックを除去
    raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    return json.loads(raw)


# ──────────────────────────────────────────────
# 5. ツイート本文を組み立てる
# ──────────────────────────────────────────────
def build_tweet(info: dict, event: dict) -> str:
    vol   = info.get("vol") or "?"
    time  = info.get("time") or "20:15"
    theme = info.get("theme") or event.get("title", "")
    pts   = info.get("points") or []
    desc  = info.get("description") or ""
    url   = event.get("event_url", "")

    point_lines = "\n".join(f"✅ {p}" for p in pts) if pts else ""

    tweet = f"【今日{time}〜｜PA45 Vol.{vol}】\n\n"
    tweet += "Power Automate初心者向け45分ハンズオン🚀\n"
    tweet += f"今日は「{theme}」。\n"

    if point_lines:
        tweet += f"\n{point_lines}\n"

    if desc:
        tweet += f"\nを組み合わせて\n👉 {desc}\n"

    tweet += "\n途中参加OK／知識ゼロ歓迎🙆‍♂️"

    if url:
        tweet += f"\n🔗 {url}"

    tweet += "\n\n#PowerAutomate #ローコード #PA45"
    return tweet


# ──────────────────────────────────────────────
# 6. X に投稿
# ──────────────────────────────────────────────
def post_tweet(text: str):
    auth = OAuth1(
        os.environ["X_API_KEY"],
        os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_SECRET"],
    )
    resp = requests.post(
        "https://api.twitter.com/2/tweets",
        auth=auth,
        json={"text": text},
        timeout=15
    )
    resp.raise_for_status()
    return resp.json()


# ──────────────────────────────────────────────
# メイン
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="投稿せず本文だけ表示")
    args = parser.parse_args()

    # 1. 今日の PA45 イベントを確認
    event = find_today_event()
    if event is None:
        sys.exit(0)

    # 2. OGP 画像を取得
    event_url = event["event_url"]
    ogp_url = get_ogp_image_url(event_url)
    if ogp_url is None:
        print("⚠️ OGP画像が取得できませんでした。イベント情報で代替します。")
        info = {
            "vol": None,
            "theme": event.get("title", ""),
            "time": "20:15",
            "points": [],
            "description": event.get("catch", "")[:30] if event.get("catch") else ""
        }
    else:
        print(f"🖼  OGP画像: {ogp_url}")
        # 3. 画像をダウンロード
        img_data, media_type = download_image(ogp_url)
        print(f"   media_type: {media_type}")
        # 4. Claude API で解析
        print("🤖 Claude API で画像を解析中...")
        info = analyze_image_with_claude(img_data, media_type)
        print(f"   解析結果: {json.dumps(info, ensure_ascii=False)}")

    # 5. 投稿文を生成
    tweet = build_tweet(info, event)

    print("\n─── 投稿内容 ───────────────────────────")
    print(tweet)
    print(f"─── 文字数: {len(tweet)} ───────────────────")

    if args.dry_run:
        print("\n（dry-run: 実際には投稿しません）")
        sys.exit(0)

    # 6. 投稿
    result = post_tweet(tweet)
    tweet_id = result.get("data", {}).get("id", "unknown")
    print(f"\n✅ X投稿完了！ tweet_id={tweet_id}")
    print(f"   https://x.com/isamu_Automate/status/{tweet_id}")


if __name__ == "__main__":
    main()

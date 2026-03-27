"""
PA45 connpass イベント説明文ジェネレーター

使い方:
  python scripts/new-connpass-event.py --vol 5 --date 2026-04-10 --theme "Apply to each"

出力:
  connpassの「イベント説明」欄と「参加者への情報」欄に貼り付けるテキストを生成します。
  前回のイベントをテンプレートとして使用し、回数・日付・テーマだけ変更します。
"""

import argparse
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── テンプレート ─────────────────────────────────────────────────────────────
# 「参加者への情報」欄（Teams URLは毎回同じ）
PARTICIPANTS_INFO_TEMPLATE = """\
【📹 録画・YouTube公開について】
第4回より、講座の録画をそのままYouTubeで公開しています。
Teams の表示名（参加者名）が画面に映る場合があります。
お名前を映したくない方は、以下の手順で「匿名参加」してください。

▼ Teamsで匿名参加する方法
1. Teams会議URLをブラウザ（Chrome / Edge など）で開く
2. 「このブラウザで続ける」を選択（アプリを使わない）
3. 名前入力欄に任意の名前（例：「匿名」「PA45参加者」など）を入力
4. 「今すぐ参加」をクリック

※ Teamsアプリで参加する場合は、プロフィールの表示名が映ります。
　 事前に表示名を変更するか、ブラウザ参加をご利用ください。

---

【Teams会議URL】
https://teams.microsoft.com/l/meetup-join/19%3ameeting_OWY5NTlmZjMtMWRmYy00NDk5LTg4YmUtZjRlMGI3ZGFiYWNk%40thread.v2/0?context=%7b%22Tid%22%3a%22ad7b0428-b3ae-4132-a47d-d9eda8cbab9a%22%2c%22Oid%22%3a%22d7ac68af-2e74-43e5-ac56-0aad7e9148a7%22%7d

上記URLから参加してください。
当日は画面共有しながら進めます。カメラ・マイクはオフで大丈夫です。

【ハンズオン資料】
当日の朝までにconnpassのお知らせ欄に掲載します。

【Power Automate環境について】
Microsoft 365のアカウントが必要です。
無料試用版でも参加できます。
"""

# 「イベント説明」欄テンプレート
EVENT_DESCRIPTION_TEMPLATE = """\
## PA45（Power Automate 45分）とは

Power Automateを45分で学ぶハンズオン勉強会です。
未経験者・初心者の方を対象に、毎回1つのアクション・機能に絞って手を動かします。

---

## 第{vol}回のテーマ：{theme}

今回は「{theme}」を取り上げます。

実際に手を動かしながら、{theme}の基本を45分で習得しましょう。

---

## こんな方におすすめ

- Power Automateを使い始めたばかりの方
- {theme}をちゃんと理解したい方
- 毎回1テーマを着実に積み上げていきたい方

---

## 開催概要

- 日時：{date_ja}
- 形式：オンライン（Microsoft Teams）
- 所要時間：約45分
- 参加費：無料

---

## 注意事項

- Power Automate が使えるMicrosoft 365アカウントをご用意ください
- 接続テストは不要です。当日Teams URLからそのままご参加ください
- 途中参加・途中退出OK

## 📹 録画・YouTube公開について

本講座は録画してYouTubeで公開しています。
**Teamsの表示名（参加者名）が画面に映る場合があります。**
お名前を映したくない方は「匿名参加」をご利用ください。

▼ 匿名参加の方法（ブラウザ推奨）
1. Teams会議URLをブラウザ（Chrome / Edgeなど）で開く
2. 「このブラウザで続ける」を選択（アプリは使わない）
3. 名前入力欄に任意の名前（例：「匿名」「PA45参加者」）を入力
4. 「今すぐ参加」をクリック

※ Teamsアプリで参加する場合、プロフィールの表示名が映ります。
　 事前に表示名を変更するか、上記のブラウザ参加をお使いください。

---

主催：はる（Power Automate コミュニティ PowerAutomate-create）
"""


def to_ja_date(date_str):
    """YYYY-MM-DD → YYYY年MM月DD日（曜日）"""
    from datetime import datetime
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]
    d = datetime.strptime(date_str, "%Y-%m-%d")
    return f"{d.year}年{d.month}月{d.day}日（{weekdays[d.weekday()]}）"


def main():
    parser = argparse.ArgumentParser(description="PA45 connpassイベント説明文ジェネレーター")
    parser.add_argument("--vol", required=True, type=int, help="回数（例: 5）")
    parser.add_argument("--date", required=True, help="開催日 YYYY-MM-DD")
    parser.add_argument("--theme", required=True, help="テーマ名（例: Apply to each）")
    args = parser.parse_args()

    date_ja = to_ja_date(args.date)

    description = EVENT_DESCRIPTION_TEMPLATE.format(
        vol=args.vol,
        theme=args.theme,
        date_ja=date_ja,
    )

    print("=" * 60)
    print(f"  PA45 第{args.vol}回：{args.theme}  ({args.date})")
    print("=" * 60)

    print("\n【 イベント説明 】コピーしてconnpassに貼り付け")
    print("-" * 60)
    print(description)

    print("\n【 参加者への情報 】コピーしてconnpassに貼り付け")
    print("-" * 60)
    print(PARTICIPANTS_INFO_TEMPLATE)


if __name__ == "__main__":
    main()

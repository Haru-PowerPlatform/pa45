"""
PA45 開催前チェックリスト

使い方:
  python scripts/pre-event-checklist.py --vol 5 --date 2026-04-10 --event-id 390000 --theme "Apply to each"

開催日までの日数に応じて、やることリストを表示します。
"""

import argparse
import sys
import io
from datetime import date, datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


def days_until(date_str):
    event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    return (event_date - date.today()).days


def main():
    parser = argparse.ArgumentParser(description="PA45 開催前チェックリスト")
    parser.add_argument("--vol", required=True, type=int)
    parser.add_argument("--date", required=True, help="開催日 YYYY-MM-DD")
    parser.add_argument("--event-id", required=True, help="connpassイベントID")
    parser.add_argument("--theme", required=True, help="テーマ名")
    args = parser.parse_args()

    days = days_until(args.date)
    connpass_url = f"https://powerautomate-create.connpass.com/event/{args.event_id}/"

    print()
    print("=" * 60)
    print(f"  PA45 第{args.vol}回：{args.theme}")
    print(f"  開催日: {args.date}  （あと {days} 日）")
    print("=" * 60)

    print("\n📋 チェックリスト\n")

    # ── 1週間以上前 ──────────────────────────────────────────────────────────
    section_1 = [
        ("connpassイベントを作成・公開済みか", connpass_url),
        ("イベントタイトル・説明文を記入済みか", None),
        ("参加者への情報（TeamsURL）を記入済みか", None),
        ("アイキャッチ画像をアップロード済みか", None),
    ]

    # ── 3日前〜前日 ──────────────────────────────────────────────────────────
    section_2 = [
        ("スライドを作成・最終確認済みか", None),
        ("スライドをGitHub Pagesにアップロード済みか",
         f"https://haru-powerplatform.github.io/pa45/assets/pa45/"),
        ("connpassのお知らせ欄にスライドURLを掲載済みか", connpass_url),
        ("Teams会議URLの動作確認をしたか", None),
        ("X（開催告知）を投稿したか", None),
    ]

    # ── 当日 ─────────────────────────────────────────────────────────────────
    section_3 = [
        ("Teams会議を開始済みか", None),
        ("画面共有の準備ができているか", None),
        ("Power Automateの環境が開いているか", None),
        ("参加者数をメモしておく（開催後のJSONに使う）", None),
    ]

    # ── X投稿文（告知・レポート） ─────────────────────────────────────────
    x_pre = (
        f"【開催告知】\n"
        f"PA45 第{args.vol}回「{args.theme}」を開催します🎉\n"
        f"📅 {args.date}\n"
        f"🔗 {connpass_url}\n"
        f"#PowerAutomate #PA45 #ハンズオン"
    )
    x_post = (
        f"【開催レポート】\n"
        f"PA45 第{args.vol}回「{args.theme}」が終わりました！\n"
        f"参加者XX人、ありがとうございました🙏\n"
        f"スライド：（URLを入れる）\n"
        f"#PowerAutomate #PA45 #ハンズオン"
    )

    # ── 開催後 ───────────────────────────────────────────────────────────────
    section_4 = [
        ("参加者数を確認する（connpassの参加者数）",
         f"python scripts/fetch-connpass-participants.py {args.event_id}"),
        ("activities JSONを作成する",
         f"python scripts/post-event.py --vol {args.vol} --event-id {args.event_id} --date {args.date} --theme \"{args.theme}\""),
        ("ブログ下書きを生成する",
         f"python scripts/new-blog-draft.py --vol {args.vol} --date {args.date} --theme \"{args.theme}\""),
        ("ブログを公開し、URLを取得して post-event.py を --blog オプション付きで再実行", None),
        ("X（開催後レポート）を投稿する", None),
    ]

    print_x = True

    def print_section(title, items, active=True):
        mark = "✅" if active else "⬜"
        print(f"  {'【' + title + '】'}")
        for label, hint in items:
            print(f"    {mark} {label}")
            if hint:
                print(f"         → {hint}")
        print()

    if days > 7:
        print_section("1週間以上前にやること", section_1)
        print_section("3日前〜前日にやること", section_2, active=False)
        print_section("当日にやること", section_3, active=False)
        print_section("開催後にやること", section_4, active=False)
    elif days > 0:
        print_section("1週間以上前にやること（済んでいれば✅）", section_1)
        print_section("3日前〜前日にやること", section_2)
        print_section("当日にやること", section_3, active=False)
        print_section("開催後にやること", section_4, active=False)
    elif days == 0:
        print_section("1週間以上前・前日まで（済んでいれば✅）", section_1 + section_2)
        print_section("当日にやること ← 今日！", section_3)
        print_section("開催後にやること", section_4, active=False)
    else:
        print_section("開催前（済んでいれば✅）", section_1 + section_2 + section_3)
        print_section("開催後にやること ← 今日！", section_4)

    # ── X投稿文 ──────────────────────────────────────────────────────────────
    print("=" * 60)
    print("\n📣 X投稿文（コピペ用）\n")
    for line in x_pre.splitlines():
        print(f"  {line}")
    print()
    for line in x_post.splitlines():
        print(f"  {line}")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()

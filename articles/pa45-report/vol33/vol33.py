# -*- coding: utf-8 -*-
"""PA45 第33回（2026-10-29）レポート。元ネタ＝slides/vol-33/handson.html・data/surveys/vol-33.json。
python vol33.py / python vol33.py --push
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _report_kit import build  # noqa: E402

CFG = dict(
    vol=33,
    slide=4,
    here=pathlib.Path(__file__).resolve().parent,
    slug="pa45-vol33-internal-name-list",
    title="【Power Automate入門】SharePointリストの内部名を、フローに調べてもらう｜PA45 第33回",
    excerpt="SharePoint リストの日本語の列は、内部名が _x72b6__x614b_ のような記号の並びになります。第33回では、リスト名を入れて押すと、表示名と内部名の表がメールで届くフローを、「SharePoint に HTTP 要求を送信します」で作ります。",
    eye=("列の内部名は", "<b>フロー</b>に調べてもらう", "表示名と内部名の表がメールで届く"),
    lead=[
        "フローの中で、リストの列名が _x72b6__x614b_ のような記号で出てくることがあります。",
        "文字化けではなく、日本語の列名は内部名が記号の並びになります。",
        '第33回では、<span class="hl-marker">リスト名を入れて押すと、表示名と内部名の表がメールで届く</span>フローを作ります。',
    ],
    sections=[
        dict(h2="今回のテーマ：決まったアクションに無い頼みごとを送る", body=[
            ("p", ["列の表示名と内部名の一覧は、SharePoint がリストごとに持っています。",
                   "ただ、それを取り出す決まったアクションはありません。"]),
            ("p", ["そこで「SharePoint に HTTP 要求を送信します」で、列の一覧をくださいという頼みごとを自分で書いて送ります。",
                   "ブラウザが Web ページを開くのと同じ、頼んで返事をもらうしくみです。使うアクションはすべて標準で、プレミアムのライセンスは要りません。"]),
        ]),
        dict(h2="ハンズオン：手動トリガーと4アクション", body=[
            ("p", ["準備として、練習用のリスト「備品の貸し出し」を作り、借りた人・状態の2列を日本語のまま足して4行入れます。",
                   "日本語の列名の内部名がどうなるかを、あとでフローに調べてもらうためです。"]),
            ("step", 1, "リスト名を入れて押すトリガー",
             "インスタント クラウド フローで<b>「フローを手動でトリガーする」</b>を選び、テキストの入力「リスト名」を足します。どのリストでも同じフローで調べられるように、リスト名は押すたびに入れる形にしました。"),
            ("step", 2, "列の一覧を読みに行く",
             "SharePoint の<b>「SharePoint に HTTP 要求を送信します」</b>で、方法は GET（読むだけ）、URI はリスト名を挟んで下の形にします。詳細パラメーターの「すべて表示」でヘッダーを出し、Accept に application/json;odata=nometadata を入れます。"),
            ("code", "_api/web/lists/getbytitle('リスト名')/fields?$filter=Hidden eq false and ReadOnlyField eq false&$select=Title,InternalName"),
            ("shot", "real-t2-http", "方法・URI・ヘッダーを入れた「SharePoint に HTTP 要求を送信します」"),
            ("step", 3, "表示名と内部名だけにする",
             "データ操作の<b>「選択」</b>で、元に返事の value、マップに 表示名＝item()?['Title']、内部名＝item()?['InternalName'] を入れます。item() は、いま見ている1件を指します。"),
            ("shot", "real-t3-select", "「選択」のマップに、表示名と内部名の2行を入れた"),
            ("step", 4, "表にして、自分あてにメールで送る",
             "<b>「HTML テーブルの作成」</b>で選択の出力を表にし、Office 365 Outlook の<b>「メールの送信 (V2)」</b>の本文に入れます。JSON のままメールに貼ると記号だらけで読めないので、表に変えてから送ります。"),
            ("shot", "real-t6-mail", "届いたメール。表示名と内部名が2列で並ぶ"),
        ]),
        dict(h2="URI とヘッダーの読み方", body=[
            ("p", ["_api/web/lists/getbytitle('リスト名') は、このサイトのこの名前のリスト、/fields はその列の一覧です。",
                   "$filter で隠し列と読み取り専用の列（作成者・登録日時など）を除き、$select で表示名と内部名だけ返してもらいます。"]),
            ("p", ["Accept のヘッダーは、返事の形の希望です。application/json は JSON という形で、odata=nometadata は付属情報なしで、という意味です。",
                   "入れ忘れると返事が value の無い形で届き、選択で The 'from' property value … is of type 'Null' のエラーで止まります（2026-10-26 のリハーサルで実際に起きました）。"]),
            ("p", ["届いた内部名は、フィルター クエリでそのまま使えます。",
                   "状態の列なら _x72b6__x614b_ eq '貸出中' と書くと、貸出中の行だけを取り出せます。表示名の 状態 で書くと、列名のエラーで止まります。"]),
        ]),
        dict(h2="先に確認しておくこと", body=[
            ("p", ["検索欄に HTTP と打つと、緑の SharePoint のアイコンのものと、地球のアイコンの「HTTP」が並びます。",
                   "地球のアイコンのほうはプレミアムなので、この回では使いません。"]),
            ("p", ["「SharePoint に HTTP 要求を送信します」は、書き換えや削除の要求も送れるアクションです。",
                   "この回で使うのは、読むだけの GET だけにしています。"]),
            ("p", ["アンケートの理解度は 73.3% で、リストを使ったことがない参加者には後半が難しかった、という声がありました。",
                   "HTTP 要求と JSON を1回で扱う回だったので、手順書と録画で同じ順番を追えるようにしてあります。"]),
        ]),
    ],
    points=[
        "日本語の列名は、内部名が _x72b6__x614b_ のような記号の並びになる。フィルター クエリで使うのは内部名。",
        "決まったアクションに無い頼みごとは「SharePoint に HTTP 要求を送信します」で送れる。この回では読むだけの GET に限った。",
        "ヘッダーの Accept を入れ忘れると、返事が value の無い形で届いて選択で止まる。",
    ],
    next="第34回は、SharePoint リストのステータスが変わったときだけ Teams に届く通知を作ります。",
)

if __name__ == "__main__":
    build(CFG)

# -*- coding: utf-8 -*-
"""PA45 第31回（2026-10-15）レポート。元ネタ＝slides/vol-31/handson.html・data/surveys/vol-31.json。
python vol31.py / python vol31.py --push
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _report_kit import build  # noqa: E402

CFG = dict(
    vol=31,
    slide=4,
    here=pathlib.Path(__file__).resolve().parent,
    slug="pa45-vol31-sharepoint-file-to-pdf",
    title="【Power Automate入門】SharePointのファイルを選んで1クリックでPDFにして送る｜PA45 第31回",
    excerpt="SharePoint のファイルの「…」から押すと、送り先とひとことを聞かれ、そのファイルが PDF になってメールで届く。第31回では、PDF への変換が OneDrive の機能であることを踏まえて、一度 OneDrive にコピーしてから変換する形で作ります。",
    eye=("選んだファイルを", "1クリックで<b>PDF</b>に", "変換は OneDrive の機能を使う"),
    lead=[
        "Word のファイルを開いて、PDF で保存して、メールに添付して送る。",
        "1件ごとに画面を3つ行き来する作業です。",
        '第31回では、<span class="hl-marker">SharePoint のファイルの「…」から押すだけで、PDF になってメールで届く</span>ところまで作ります。',
    ],
    sections=[
        dict(h2="今回のテーマ：入口がファイルになった「選んで1クリック」", body=[
            ("p", ["第30回は Teams のメッセージから To Do へ入れる形でした。",
                   "今回は同じ選んで1クリックの形で、入口が SharePoint のファイルになります。"]),
            ("p", ["押した人が選ぶのは、送るファイルと送り先です。",
                   "PDF にする・添付して送る、のところをフローに任せます。"]),
        ]),
        dict(h2="ハンズオン：6ブロックで作る", body=[
            ("shot", "real-flow-all", "完成したフロー。トリガーからメールの送信まで、6ブロックが縦に並ぶ"),
            ("step", 1, "ファイルの「…」から押せるトリガーを置く",
             "インスタント クラウド フローで SharePoint の<b>「選択したファイルの場合」</b>を選び、サイトとライブラリ（ドキュメント）を指定します。「＋ 入力を追加する」で、送り先の「メール」と、ひとことの「テキスト」を足します。"),
            ("shot", "real-s1-trigger", "トリガーに、入力「メール」と「入力（テキスト）」の2つを足した"),
            ("step", 2, "選んだファイルの名前と中身を取り出す",
             "トリガーが渡すのはファイルの ID だけです。<b>「ファイルのプロパティの取得」</b>で名前と識別子を取り、その識別子で<b>「ファイル コンテンツの取得」</b>から中身を取り出します。"),
            ("step", 3, "OneDrive に置いて、PDF に変換する",
             "OneDrive for Business の<b>「ファイルの作成」</b>で /PA45一時 に同じ名前で置き、<b>「ファイルの変換」</b>でターゲットの種類を PDF にします。"),
            ("shot", "real-s3-convert", "「ファイルの変換」。ファイルは「ファイルの作成」の ID、種類は PDF"),
            ("step", 4, "PDF をメールに添付して送る",
             "Office 365 Outlook の<b>「メールの送信 (V2)」</b>で、宛先にトリガーのメール、件名に拡張子なしの名前、本文にひとことを入れます。「すべて表示」で添付ファイルを出し、名前とコンテンツは「ファイルの変換」のものを選びます。"),
            ("shot", "real-s4-attach-pick", "添付の名前とコンテンツは「ファイルの変換」のほうから選ぶ"),
        ]),
        dict(h2="PDF への変換は OneDrive の機能", body=[
            ("p", ["「ファイルの変換」は OneDrive for Business のアクションで、つないだアカウントの OneDrive にあるファイルしか扱えません。",
                   "そのため SharePoint のファイルを、一度自分の OneDrive にコピーしてから変換しています。"]),
            ("p", ["OneDrive for Business の「ファイルの変換」は Standard のコネクタです。",
                   "Word Online (Business) の「Word 文書を PDF に変換する」は Premium（有償）なので、今回は OneDrive のほうを使いました。"]),
        ]),
        dict(h2="先に確認しておくこと", body=[
            ("p", ["SharePoint のファイルの「…」→「統合」→「フロー」に出るのは、既定の環境で作ったフローだけです。",
                   "作り始める前に、画面右上の環境を確かめます。"]),
            ("p", ["アンケートには、メールは届いたが PDF が添付されていなかった、という声がありました。",
                   "添付のコンテンツに「ファイルの作成」の下の項目（変換前の Word）を選ぶと、PDF ではないものが渡ります。選ぶのは「ファイルの変換」の「ファイル コンテンツ」です。"]),
            ("p", ["署名・パスワード・IRM（情報保護）の付いた Word は変換できません。",
                   "OneDrive の /PA45一時 には変換前のコピーが残るので、気になるときは最後に「ファイルの削除」を足します。"]),
            ("shot", "real-t5-mail", "届いたメール。件名がファイル名で、PDF が添付されている"),
        ]),
    ],
    points=[
        "「選択したファイルの場合」のトリガーは、既定の環境に作ると SharePoint のファイルの「…」に出る。",
        "トリガーが渡すのはファイルの ID だけ。名前はプロパティの取得、中身はコンテンツの取得で取り出す。",
        "PDF への変換は OneDrive の「ファイルの変換」（Standard）。一度 OneDrive にコピーしてから変換する。",
    ],
    next="第32回は、置くだけで月別フォルダに片付くファイル整理を作ります。",
)

if __name__ == "__main__":
    build(CFG)

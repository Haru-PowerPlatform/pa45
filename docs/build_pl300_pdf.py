# -*- coding: utf-8 -*-
"""PL-300 ミスポイント復習用PDFを生成する"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
)

# 日本語フォント登録（Windowsの游ゴシック）
pdfmetrics.registerFont(TTFont("YuGothic", "C:/Windows/Fonts/YuGothR.ttc"))
pdfmetrics.registerFont(TTFont("YuGothicB", "C:/Windows/Fonts/YuGothB.ttc"))

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "Title", parent=styles["Title"],
    fontName="YuGothicB", fontSize=22, leading=28, alignment=1,
    textColor=colors.HexColor("#1e3a8a"), spaceAfter=10,
)
subtitle_style = ParagraphStyle(
    "Subtitle", parent=styles["Normal"],
    fontName="YuGothic", fontSize=11, leading=16, alignment=1,
    textColor=colors.HexColor("#475569"), spaceAfter=20,
)
h1_style = ParagraphStyle(
    "H1", parent=styles["Heading1"],
    fontName="YuGothicB", fontSize=18, leading=24,
    textColor=colors.HexColor("#1e3a8a"), spaceBefore=14, spaceAfter=10,
    borderPadding=4,
)
h2_style = ParagraphStyle(
    "H2", parent=styles["Heading2"],
    fontName="YuGothicB", fontSize=13, leading=18,
    textColor=colors.HexColor("#7c3aed"), spaceBefore=10, spaceAfter=4,
)
body_style = ParagraphStyle(
    "Body", parent=styles["Normal"],
    fontName="YuGothic", fontSize=10, leading=15, spaceAfter=4,
)
small_style = ParagraphStyle(
    "Small", parent=styles["Normal"],
    fontName="YuGothic", fontSize=9, leading=13, spaceAfter=3,
)
rule_style = ParagraphStyle(
    "Rule", parent=styles["Normal"],
    fontName="YuGothicB", fontSize=10, leading=15,
    textColor=colors.HexColor("#b91c1c"), spaceAfter=4,
)

# ================ ミスデータ ================
# 番号, テーマ, 誤答→正解, 鉄則
TOP_WEAKNESS = [
    ("ALL vs ALLSELECTED", "🚨 5回ミス", [
        "「選択した」「表示中」「選択範囲」「絞り込んだ中で」 → <b>ALLSELECTED</b>",
        "「全国」「全体」「総〇〇」「全製品」 → <b>ALL</b>",
        "「地域全体に占めるシェア」の罠：「選択した地域の中での全体」なので <b>ALLSELECTED</b>",
    ]),
    ("データフロー vs 共有データセット", "🚨 4回ミス", [
        "「変換ロジック」「Power Query」「クレンジング」「ETL」 → <b>データフロー</b>",
        "「完成済みモデル」「メジャー共有」 → <b>共有データセット</b>",
        "「再利用」という単語だけで共有データセットを選ばない。<b>何を再利用するか</b>を確認。",
    ]),
    ("RLS 実装手順", "🟠 3回ミス", [
        "ロール定義（DAX） → <b>Power BI Desktop</b>",
        "ユーザー割り当て → <b>Power BI Service</b>（発行後）",
        "RLS テスト → Desktop の「ロールとして表示」",
    ]),
    ("複数日付列のリレーション", "🟠 3回ミス", [
        "1つのDateテーブル + 非アクティブリレーション + <b>USERELATIONSHIP</b>",
        "OrderDate, ShipDate, DueDate それぞれ別の集計が必要",
        "CALCULATE 内でのみ使用可。例: <font name='Courier'>CALCULATE(SUM(...), USERELATIONSHIP(Sales[ShipDate], Date[Date]))</font>",
    ]),
]

MISTAKES_BY_AREA = {
    "領域① データの準備（Power Query）": [
        ("Append（追加）", "同構造のテーブルを縦に結合（SQLのUNION相当）。月次CSV12個を1つに → Append"),
        ("Merge（マージ）", "別テーブルをキーで横結合（SQLのJOIN相当）"),
        ("列のマージ", "同一テーブル内の複数列を1列に結合（姓+名→氏名）。クエリのマージとは別物"),
        ("ピボット / ピボット解除", "値を列ヘッダーに昇格＝ピボット／列見出しを行に＝ピボット解除"),
        ("タグ列の分割", "「;」区切りタグ → 列の分割で<b>「行」</b>に展開（列に分割は罠）"),
        ("条件付き列", "GUIで if-then-else を構築。M知識不要"),
        ("例から列を作成", "複雑な文字列加工をAIに推論させる。2〜3個の正解例で自動生成"),
        ("インデックス列", "行番号・連番付与。0開始/1開始/カスタム"),
        ("下方向へフィル（Fill Down）", "結合セル取り込み時、空白を直前の値で埋める"),
        ("グループ化", "明細不要・集計値だけで取り込み。1000万行→数千行に圧縮"),
        ("上位N行の削除", "先頭の不要メタデータをスキップ→1行目をヘッダーに昇格"),
        ("値の置換", "表記ゆれを統一（Complete/done/完了済み → 完了）"),
        ("エラーの置換", "型変換エラーセルをnullに（データ保持）。エラーの削除は行ごと消失"),
        ("列で並べ替え（Sort by Column）", "テキスト列を別の数値列の順で並べる。モデルレベル設定で全ビジュアル一貫"),
        ("From Folder", "フォルダー内の同構造CSVを自動結合。新規ファイルも自動取り込み"),
        ("クエリの折りたたみ確認", "ステップ右クリック→「ネイティブクエリの表示」が有効ならフォールディング成功"),
        ("プライバシーレベル", "Formula.Firewall エラー対策。Private/Organizational/Publicの3段階"),
        ("増分更新", "直近N日のみ更新、過去履歴保持。RangeStart/RangeEndパラメーターが必須"),
        ("データプロファイリング3機能", "列の品質（空白/エラー）／列の分布（ユニーク数）／列のプロファイル（統計）"),
        ("データ型最適化", "整数 > 固定小数点 > 10進数 > テキスト（VertiPaq圧縮効率順）"),
        ("ライブ接続", "完成済みモデル（Power BIデータセット/SSAS）に直結。データ複製なし"),
    ],
    "領域② データのモデル化（DAX）": [
        ("計算列 vs メジャー", "スライサー・軸・フィルター → 計算列／カード・KPI・集計 → メジャー"),
        ("ALL vs ALLSELECTED", "選択した範囲＝ALLSELECTED／全体＝ALL（最重要弱点）"),
        ("ALL(列名)", "1列だけフィルター解除（他は残す）。REMOVEFILTERS()は全部解除でやりすぎ"),
        ("SUMX", "行ごとに掛け算・割り算してから合計。SUM×SUMは値が爆発"),
        ("CALCULATE + 時間関数", "前年同月＝SAMEPERIODLASTYEAR／累計＝TOTALYTD／N期間シフト＝DATEADD"),
        ("DATEADD", "日付をN期間シフト。<font name='Courier'>DATEADD(日付列, -3, MONTH)</font>。第1引数は必ず日付列"),
        ("DATEDIFF", "2日付の差。<font name='Courier'>DATEDIFF(開始, 終了, 単位)</font>。引数順注意（古い→新しい）"),
        ("USERELATIONSHIP", "複数日付列の非アクティブリレーションを一時的に有効化"),
        ("RELATED vs RELATEDTABLE", "多→1＝RELATED（1行）／1→多＝RELATEDTABLE（テーブル）"),
        ("DIVIDE", "ゼロ除算回避。第3引数なし＝BLANK、指定＝代替値"),
        ("IFERROR", "DAXのエラー処理。try…otherwise は M言語（混同注意）"),
        ("COALESCE", "左から最初の非空白値を返す。優先順位付き表示の定番"),
        ("HASONEVALUE", "単一選択か判定（True/False）。値も欲しいときは SELECTEDVALUE"),
        ("SELECTEDVALUE", "単一選択時の値、それ以外は代替値"),
        ("DISTINCTCOUNT", "ユニーク値の数。COUNTROWSは重複込みで罠"),
        ("RANKX", "順位付け。<font name='Courier'>RANKX(ALL(Product), [売上])</font>。ALLが無いと常に1"),
        ("SWITCH(TRUE(), ...)", "複数閾値の条件分岐。ネストIFより読みやすい"),
        ("VAR + RETURN", "中間値を変数化。可読性・パフォーマンス向上"),
        ("計算テーブル", "派生テーブルをDAXで作成。モデリングタブ→新しいテーブル"),
        ("CALENDARAUTO / CALENDAR", "日付テーブルをDAXで作成"),
        ("計算グループ", "メジャー×計算パターンの爆発を防ぐ。Tabular Editorで作成"),
        ("クロスフィルター方向", "スタースキーマ標準＝ディメンション→ファクトの単方向"),
        ("動的RLS", "<font name='Courier'>[列] = USERPRINCIPALNAME()</font>。USERNAMEは罠"),
        ("AVERAGEとBLANK", "AVERAGEはBLANK自動除外。NOT ISBLANKは冗長"),
        ("暗黙 vs 明示メジャー", "ベストプラクティスは明示メジャー（再利用・統一・修正の一元反映）"),
        ("Dualモード", "Composite モデルの共通ディメンション用。Import/DQ両方と結合可"),
    ],
    "領域③ 視覚化と分析": [
        ("ドリルダウン", "同じグラフで階層を掘る（年→月→日）"),
        ("ドリルスルー", "別ページに飛んでフィルター引き継ぐ"),
        ("ブックマーク + ボタン + 選択ペイン", "同じページ内でビューを切り替える3点セット"),
        ("ページナビゲーター", "ボタン動作でページ間遷移。追加・削除を自動反映"),
        ("相互作用を編集", "同じページ内のビジュアル間制御。フィルター/強調表示/なし"),
        ("同期スライサー", "ページ間でスライサー値を連動"),
        ("Top N フィルター", "1ビジュアルだけ上位N件表示（DAX不要）"),
        ("ビン化", "連続数値を等間隔グループに（10歳刻みなど）"),
        ("クラスター", "散布図で似た点を自動グループ化（AI）"),
        ("Q&A", "自然言語で質問→グラフ生成（能動）"),
        ("分解ツリー", "メジャーを階層的に分解＋AIが切り口提案"),
        ("主要なインフルエンサー", "ターゲットへの影響要因を分析（要因分析）"),
        ("スマートナラティブ", "データを文章で動的に説明（テキスト生成）"),
        ("クイックインサイト", "自動でインサイトを発見（数値ベース）"),
        ("分析ペイン", "定数線・予測・推移線・異常検出など。グラフに線を追加"),
        ("条件付き書式（フィールド値）", "複数列の複合条件はメジャーで色を返してフィールド値で適用"),
        ("カスタムビジュアル", "標準にない図（サンキー等）はAppSourceから入手"),
        ("ページ分割レポート", "帳票・請求書・印刷・改ページ専用（.rdl）"),
        ("ウォーターフォール", "期初→期末の+/−寄与度の可視化"),
        ("ファネル", "段階的な離脱・転換率（コンバージョン）"),
        ("ツリーマップ", "階層構造の面積比較"),
        ("リボンチャート", "順位の時系列変化"),
        ("KPIビジュアル", "実績/目標/推移を1つで表示"),
        ("スパークライン", "テーブル/マトリックスのセル内にミニ折れ線（推移）"),
        ("データバー", "セル内に値の大小を棒で表示（推移ではない）"),
        ("小さい複数（Small multiples）", "1ビジュアルをカテゴリで格子分割"),
        ("階層作成", "モデルビューで階層を作成→軸にドラッグでドリル動作"),
        ("レポートテーマ", "全体デザイン一括。JSONで保存・再利用"),
        ("カスタムツールチップ（レポートページ）", "ホバー時に専用ページを表示。複雑なビジュアル可"),
        ("代替テキスト（Alt Text）", "スクリーンリーダー対応・アクセシビリティ"),
        ("Mobile Layout", "スマホ用縦長レイアウト。表示タブ→携帯電話レイアウト"),
        ("What-If パラメーター", "スライダーで数値を変えてシミュレーション"),
        ("Goals / スコアカード", "複数KPI管理・担当者割当・ステータス追跡"),
        ("スライサーの検索", "多数項目から絞り込み。スライサー右上「…」→検索を有効化"),
    ],
    "領域④ デプロイと保守": [
        ("ワークスペースロール", "管理者 > メンバー > 共同作成者 > ビューアー"),
        ("Build vs Read 権限", "Read=閲覧のみ／Build=新規レポート作成可"),
        ("認定（Certified） vs プロモーション", "認定＝管理者承認制／プロモーション＝誰でも付与"),
        ("機密ラベル（Sensitivity Label）", "情報の機密度。エクスポート後も保護継続。MIP連携"),
        ("アプリの公開", "大人数・閲覧専用・パッケージ配布"),
        ("アプリの利用ユーザー追加", "アクセス許可で追加→「アプリの更新」で反映"),
        ("共有ボタン", "少人数・1レポートだけ共有"),
        ("テンプレート（PBIT）", "レイアウト＋モデル定義のみ・データなしで配布"),
        ("展開パイプライン", "開発・テスト・本番の3環境管理（Premium機能）"),
        ("所有者を引き継ぐ（Take over）", "退職者のデータセット所有権移譲"),
        ("ゲートウェイ判断", "オンプレミスのみ必要・クラウド同士は不要"),
        ("ゲートウェイ種類", "個人モード（自分専用）／標準モード（チーム共有）"),
        ("スケジュール更新の上限", "Pro=8回/日／Premium=48回/日（最短30分）"),
        ("更新失敗通知", "スケジュール更新設定に標準装備"),
        ("サブスクリプション", "定期メール配信（PDF/PPTX添付）"),
        ("データアラート", "KPI閾値超え通知（KPI/カード/ゲージのみ）"),
        ("OneDrive 自動同期", "OneDrive/SharePoint Online上のExcelは約1時間おきに自動同期"),
        ("リネージビュー", "依存関係・影響範囲の視覚化"),
        ("使用状況メトリクス", "誰が・いつ・何回見たか（利用分析）"),
        ("監査ログ", "誰が何をしたか（テナント全体・コンプライアンス）"),
        ("パフォーマンスアナライザー", "レポートの速度測定・ボトルネック特定"),
        ("ダッシュボード", "複数レポートのビジュアルを1画面に集約（Service専用）"),
        ("Webに公開", "ライセンスなし・社外公開（機密データ厳禁）"),
        ("ライブ接続 vs DirectQuery", "ライブ＝既存モデル／DQ＝生データソース"),
        ("Power Query パラメーター", "接続文字列・サーバー名を変数化（1箇所変更で全部切替）"),
        ("Power BI ライセンス", "Free＝My WS限定／Pro＝通常WS共同作業／Premium＝大組織"),
    ],
}

REFLEX_KEYWORDS = [
    ("DAX/集計", [
        ("行ごとに掛け算→合計", "SUMX"),
        ("列をそのまま合計", "SUM"),
        ("選択範囲内のシェア", "ALLSELECTED"),
        ("全体に対するシェア", "ALL"),
        ("1列だけフィルター解除", "ALL(列名)"),
        ("複数列にまたがる条件付き書式", "フィールド値"),
        ("ゼロ除算回避", "DIVIDE"),
        ("エラー時に代替値", "IFERROR"),
        ("最初の非空白値", "COALESCE"),
        ("単一選択判定（True/False）", "HASONEVALUE"),
        ("単一選択時の値取得", "SELECTEDVALUE"),
        ("ユニーク値の数", "DISTINCTCOUNT"),
        ("ランキング", "RANKX(ALL(...), 式)"),
        ("複数閾値の条件分岐", "SWITCH(TRUE(), ...)"),
        ("中間値の変数化", "VAR + RETURN"),
    ]),
    ("時間インテリジェンス", [
        ("前年同月（YoY）", "SAMEPERIODLASTYEAR"),
        ("年初からの累計（YTD）", "TOTALYTD"),
        ("N期間シフト（柔軟）", "DATEADD(日付列, -N, 単位)"),
        ("過去N期間ローリング", "DATESINPERIOD"),
        ("2日付の差（日数等）", "DATEDIFF(開始, 終了, 単位)"),
        ("タイムインテリジェンスが動かない", "「日付テーブルとしてマーク」未設定 or リレーション無効"),
    ]),
    ("Power Query", [
        ("同構造を縦結合", "Append（追加）"),
        ("キーで横結合", "Merge（マージ）"),
        ("姓+名を1列に", "列のマージ"),
        ("縦持ち→横持ち", "ピボット"),
        ("横持ち→縦持ち", "ピボット解除"),
        ("「;」区切りタグの展開", "列の分割→各行"),
        ("先頭メタデータをスキップ", "上位N行の削除"),
        ("結合セルの空白を埋める", "下方向へフィル"),
        ("行番号・連番", "インデックス列"),
        ("表記ゆれ統一", "値の置換"),
        ("if-then-else をGUIで", "条件付き列"),
        ("複雑な文字列加工", "例から列を作成"),
        ("複数CSVを自動取り込み", "From Folder"),
        ("Formula.Firewall エラー", "プライバシーレベル設定"),
        ("接続先を1箇所で切替", "Power Query パラメーター"),
    ]),
    ("視覚化", [
        ("階層を掘る（同じグラフ）", "ドリルダウン"),
        ("別ページへ詳細遷移", "ドリルスルー"),
        ("ビュー切替（同じページ）", "ブックマーク+ボタン+選択ペイン"),
        ("ページ間スライサー連動", "同期スライサー"),
        ("クロスフィルター制御", "相互作用を編集"),
        ("自然言語で質問", "Q&A"),
        ("階層的に分解", "分解ツリー"),
        ("要因分析", "主要なインフルエンサー"),
        ("データを文章で説明", "スマートナラティブ"),
        ("自動でインサイト発見", "クイックインサイト"),
        ("散布図で自動グループ化", "クラスター"),
        ("グラフに目標線・予測", "分析ペイン"),
        ("帳票・印刷・改ページ", "ページ分割レポート"),
        ("期初→期末の+/−", "ウォーターフォール"),
        ("段階的離脱", "ファネル"),
        ("セル内にミニ折れ線", "スパークライン"),
        ("セル内に棒で大小", "データバー"),
        ("複数地域を格子状に", "小さい複数"),
        ("スマホ用レイアウト", "携帯電話レイアウト"),
        ("What-If シミュレーション", "What-Ifパラメーター"),
        ("複数KPI担当者管理", "Goals / スコアカード"),
    ]),
    ("配布・運用", [
        ("少人数に1レポート", "共有ボタン"),
        ("大規模配布・パッケージ", "アプリ"),
        ("公式品質保証", "認定（Certified）"),
        ("情報の機密度", "機密ラベル"),
        ("テンプレート配布", "PBIT"),
        ("3環境管理", "展開パイプライン"),
        ("所有者退職", "Take over"),
        ("オンプレミス接続", "ゲートウェイ必要"),
        ("チームで共有ゲートウェイ", "標準モード"),
        ("OneDriveのExcel自動同期", "ゲートウェイ不要・約1時間おき"),
        ("依存関係", "リネージビュー"),
        ("閲覧回数分析", "使用状況メトリクス"),
        ("テナント全体の操作証跡", "監査ログ"),
        ("レポートが遅い", "パフォーマンスアナライザー"),
        ("複数レポートを1画面", "ダッシュボード"),
        ("通常ワークスペース閲覧", "Pro ライセンス"),
        ("既存PowerBIデータセット接続", "ライブ接続"),
        ("生DBに直結", "DirectQuery"),
    ]),
]


# ================ PDF構築 ================
def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("YuGothic", 8)
    canvas.setFillColor(colors.HexColor("#94a3b8"))
    canvas.drawCentredString(A4[0] / 2, 12 * mm, f"PL-300 ミスポイント復習 / Haru / Page {doc.page}")
    canvas.restoreState()


def add_bullets(story, items):
    for txt in items:
        story.append(Paragraph(f"• {txt}", body_style))


def main():
    out_path = r"C:\Users\isamu\Documents\pa45\docs\PL300_mistakes_review.pdf"
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=20 * mm, bottomMargin=20 * mm,
        title="PL-300 ミスポイント復習",
        author="Haru",
    )
    story = []

    # --- 表紙 ---
    story.append(Spacer(1, 60))
    story.append(Paragraph("PL-300 ミスポイント<br/>復習まとめ", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Microsoft Power BI Data Analyst Associate", subtitle_style))
    story.append(Spacer(1, 40))

    cover_table_data = [
        ["項目", "内容"],
        ["対象", "Haru (ism136)"],
        ["教材", "MS Learn 公式試験範囲ベース"],
        ["範囲", "ランダム総復習 ㉙ 〜 130（合計130問）"],
        ["弱点再テスト", "R1〜R26（既出ミスを問題変更して再出題）"],
        ["作成日", "2026-05-24"],
        ["ソース", "docs/pl300-mistakes.md (GitHub: Haru-PowerPlatform/pa45)"],
    ]
    cover_table = Table(cover_table_data, colWidths=[40 * mm, 110 * mm])
    cover_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "YuGothic"),
        ("FONTNAME", (0, 0), (-1, 0), "YuGothicB"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#eff6ff")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "<font color='#475569'>このPDFは試験直前の最終チェック用。<br/>"
        "問題文に頻出するキーワードと、即答すべき機能・関数を結びつけた<br/>"
        "「反射パターン集」として活用してください。</font>",
        ParagraphStyle("Cover", parent=body_style, alignment=1, fontSize=10),
    ))
    story.append(PageBreak())

    # --- 1. 最重要弱点 ---
    story.append(Paragraph("1. 最重要弱点（複数回ミス）", h1_style))
    story.append(Paragraph(
        "<font color='#475569'>同じテーマで複数回間違えた最優先項目です。試験前に必ず復習してください。</font>",
        body_style,
    ))
    story.append(Spacer(1, 8))

    for theme, badge, rules in TOP_WEAKNESS:
        block = []
        block.append(Paragraph(f"{theme}　<font color='#dc2626'>{badge}</font>", h2_style))
        for r in rules:
            block.append(Paragraph(f"• {r}", body_style))
        block.append(Spacer(1, 6))
        story.append(KeepTogether(block))

    story.append(PageBreak())

    # --- 2. 領域別ミスポイント ---
    story.append(Paragraph("2. 領域別ミスポイント一覧", h1_style))
    story.append(Paragraph(
        "<font color='#475569'>MS Learn 公式アウトラインの4領域に沿ったミスポイント。"
        "各テーマと一言鉄則を並べたチートシート。</font>",
        body_style,
    ))
    story.append(Spacer(1, 8))

    for area, items in MISTAKES_BY_AREA.items():
        story.append(Paragraph(area, h2_style))

        table_data = [["テーマ", "鉄則・反射ポイント"]]
        for theme, rule in items:
            table_data.append([
                Paragraph(theme, body_style),
                Paragraph(rule, small_style),
            ])
        t = Table(table_data, colWidths=[45 * mm, 125 * mm], repeatRows=1)
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "YuGothic"),
            ("FONTNAME", (0, 0), (-1, 0), "YuGothicB"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7c3aed")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(t)
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # --- 3. 反射キーワード集 ---
    story.append(Paragraph("3. 反射キーワード集（試験本番用）", h1_style))
    story.append(Paragraph(
        "<font color='#475569'>問題文のキーワード → 即答する機能・関数。<br/>"
        "試験中はこの表を頭の中で照らし合わせて反射的に答える。</font>",
        body_style,
    ))
    story.append(Spacer(1, 8))

    for category, pairs in REFLEX_KEYWORDS:
        story.append(Paragraph(category, h2_style))
        table_data = [["問題文のキーワード", "即答"]]
        for kw, ans in pairs:
            table_data.append([
                Paragraph(kw, small_style),
                Paragraph(f"<b>{ans}</b>", small_style),
            ])
        t = Table(table_data, colWidths=[100 * mm, 70 * mm], repeatRows=1)
        t.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "YuGothic"),
            ("FONTNAME", (0, 0), (-1, 0), "YuGothicB"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0891b2")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#ecfeff")]),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story.append(t)
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # --- 4. 試験当日チェックリスト ---
    story.append(Paragraph("4. 試験当日チェックリスト", h1_style))
    story.append(Spacer(1, 6))

    checklist = [
        ("⚠️ 最頻出の罠（必ず一呼吸おく）", [
            "「全体」と書いてあっても、文脈が<b>「選択範囲の中の全体」</b>なら → ALLSELECTED",
            "「再利用」と書いてあっても、再利用するのが<b>「変換ロジック」</b>なら → データフロー",
            "「PDF出力」と書いてあっても、<b>帳票・改ページ</b>要件があれば → ページ分割レポート",
            "「機密」と書いてあっても、<b>品質保証マーク</b>なら → 認定（Certified）",
            "「フィルターしたい」と書いてあっても、<b>行ごとに分類</b>するなら → 計算列（メジャー不可）",
        ]),
        ("✅ 場所判定（GUIで答える系）", [
            "ロール定義 → Desktop、ユーザー割当 → Service",
            "並べ替えはモデルレベル（列ツール → 列で並べ替え）",
            "テーマはJSON保存・再利用",
            "代替テキストはビジュアル書式 → 全般",
            "ピン留め → ダッシュボード（Service専用）",
            "ライブページのピン留めはServiceのみ",
        ]),
        ("✅ 接続モード判定", [
            "Power BIデータセット / SSAS → ライブ接続",
            "SQL Server等の生データソースに直接 → DirectQuery",
            "データを取り込む → インポート",
            "オンプレSQL / 社内ファイルサーバ → ゲートウェイ必要",
            "Azure SQL / SharePoint Online / OneDrive → ゲートウェイ不要",
        ]),
        ("✅ パフォーマンス改善の順番", [
            "1. 不要列・不要行を削除（Power Query上流）",
            "2. データ型最適化（整数 > 固定小数点 > 10進数 > テキスト）",
            "3. スタースキーマに整理",
            "4. メジャー最適化（VAR・SUMX）",
            "5. 最終手段：DirectQuery / Premium",
        ]),
    ]
    for ttl, items in checklist:
        block = [Paragraph(ttl, h2_style)]
        for it in items:
            block.append(Paragraph(f"• {it}", body_style))
        block.append(Spacer(1, 6))
        story.append(KeepTogether(block))

    story.append(Spacer(1, 20))
    story.append(Paragraph(
        "<font color='#475569'>—— 最後の最後まで、反射キーワードを頭で唱えてから答える。落ち着いて。<br/>"
        "迷ったら：『何の全体？』『何を再利用？』『どこに置きたい？』を自問する。</font>",
        ParagraphStyle("End", parent=body_style, alignment=1),
    ))

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(f"OK: {out_path}")


if __name__ == "__main__":
    main()

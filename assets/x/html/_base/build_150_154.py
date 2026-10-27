# -*- coding: utf-8 -*-
"""X技術Tips Vol.150〜154（2026-10-27 作り直し）の4枚組を生成する。python build_150_154.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x145lib import *

NEXT1 = "作り方は<b>2枚目</b>、実際に作ったフローの画面は<b>3・4枚目</b>"
X = SVGW('<path d="M6 6l12 12M18 6L6 18"/>', 3)
OK = SVGW('<path d="M5 12l5 5 9-10"/>', 3)


# ════════════════ Vol.150 Excel の一覧から宛名入りメールを1人ずつ（型A）
def v150():
    people = [("山田工業", "山田 太郎", "11月10日（月）"), ("佐藤商事", "佐藤 花子", "11月11日（火）"), ("鈴木設計", "鈴木 一郎", "11月12日（水）")]
    mails = "".join(f'<div class="mail new" style="padding:4px 9px"><div class="ms" style="font-size:15px">【{d}】面談のご案内（{c} {n} 様）</div>'
                    f'<div class="mb" style="font-size:14.5px">{c}<br>{n} 様　いつもお世話になっております。{d} の面談につきまして…</div></div>' for c, n, d in people)
    stage = f'''    <div class="col bad">
      <div class="ph"><span class="mk">{X}</span>BCC で全員に同じ文面</div>
      <div class="win outlook" style="flex:1"><div class="wh"><img src="{ICON['outlook']}" alt="">新しいメッセージ</div><div class="wb">
        <div class="fi"><span class="k">BCC</span>yamada@… ; sato@… ; suzuki@… ; takahashi@… ; tanaka@…</div>
        <div class="fi"><span class="k">件名</span>面談のご案内</div>
        <div style="border:1.5px solid #DCE3EE;border-radius:8px;padding:8px 10px;font-size:15.5px;font-weight:700;color:var(--navy);line-height:1.5;flex:1">
          関係各位<br>いつもお世話になっております。<br>面談の日時は、別途お送りした一覧をご確認ください。</div>
      </div></div>
      <div class="cap">宛名も日時も入らず、<b>入れ違いの返信</b>が来る</div>
      <img class="chara" src="{A}chara/chara_trouble.png" alt="" style="position:absolute;right:8px;bottom:50px;height:112px">
    </div>
    <div class="col good">
      <div class="ph"><span class="mk">{OK}</span>1人ずつ、宛名と日時入り</div>
      <div class="win outlook" style="flex:1"><div class="wh"><img src="{ICON['outlook']}" alt="">送信済みアイテム</div><div class="wb" style="gap:5px">{mails}</div></div>
      <div class="metric"><span class="ml">送る作業</span><span class="mv">5通×手作業</span><span class="ar">{SVGW(P_ARROW, 3)}</span><span class="mv to">ボタン1回</span><span class="ml">一覧はExcelのまま</span></div>
    </div>'''
    page("vol-150", "Vol.150-1", "Excelの一覧から宛名入りメール", "Excel の一覧から、<br><span class=\"hl\">1人ずつ宛名入りのメール</span>を送る",
         "smile", "送付先の Excel を1行ずつ読み、会社名・氏名・面談日を差し込んだメールを<b>1人に1通</b>送ります。<br>BCC の一斉送信をやめても、送る手間はボタン1回のままです",
         stage, next_bar(NEXT1))

    cols = [
        {"t": "Excel を表にしておく", "ex": '<table class="lt"><tr><th>氏名</th><th>会社名</th><th>メールアドレス</th><th>面談日</th></tr><tr><td>山田 太郎</td><td>山田工業</td><td>yamada@…</td><td>11月10日</td></tr><tr><td>佐藤 花子</td><td>佐藤商事</td><td>sato@…</td><td>11月11日</td></tr></table>',
         "acts": [("excel", "ホーム ＞ テーブルとして書式設定", [("テーブル名", "送付先", True), ("置き場所", "OneDrive の /PA45一時", False)], "見出しの行が、そのまま動的コンテンツの名前になる")],
         "cap": "見出しは<b>氏名・会社名・メールアドレス・面談日</b>"},
        {"t": "行を全部読む", "ex": '<div>送付先の5行が、上から順に取れる</div><div style="color:#64748B">見出しの名前で値を選べる</div>',
         "acts": [("pa", "フローを手動でトリガーする", [], "送りたいときに自分で押す"),
                  ("excel", "表内に存在する行を一覧表示", [("ファイル", "/PA45一時/面談のご案内_送付先.xlsx", True), ("テーブル", "送付先", False)], "")],
         "cap": "ファイルは<b>フォルダーのアイコン</b>から選ぶ"},
        {"t": "1行ごとに送る", "ex": '<div style="font-weight:900">【11月10日（月）】面談のご案内（山田工業 山田 太郎 様）</div><div>山田工業<br>山田 太郎 様</div>',
         "acts": [("ctrl", "それぞれに適用する", [], ""),
                  ("outlook", "メールの送信 (V2)", [("宛先", "メールアドレス", True), ("件名", "【面談日】面談のご案内（会社名 氏名 様）", True), ("本文", "会社名・氏名・面談日を差し込む", False)], "")],
         "cap": "最初は宛先を<b>自分</b>にして中身を確かめる"},
    ]
    page("vol-150b", "Vol.150-2", "作り方", "作り方は<span class=\"hl\">3ステップ</span>（表にする → 読む → 1行ずつ送る）",
         "laptop", "Excel を<b>テーブル</b>にしておくと、列の見出しがそのまま差し込みの名前になります。<br>メールの件名と本文に、会社名・氏名・面談日を選んで並べるだけです",
         howto_cols(cols), warn_bar(["行の一覧は既定で256行まで。それ以上はアクションの設定でページ処理を有効に", "Excel を開いて編集中だとロックで失敗することがある", "送る前に自分宛てで1回試す"]))

    steps = [("pa", "フローを手動でトリガーする", "送りたいときにボタンで起動", False),
             ("excel", "表内に存在する行を一覧表示", "テーブル <b>送付先</b> の行を全部取る", True),
             ("ctrl", "それぞれに適用する", "1行ずつ、くり返す", False),
             ("outlook", "メールの送信 (V2)", "宛先・件名・本文に<b>その行の値</b>を差し込む", True),
             ("bulb", "一覧を直せば、次回も同じフローで送れる", "宛先や日時を変えたいときは Excel を直すだけ", False)]
    page("vol-150c", "Vol.150-3", "実際のフロー", "実際に作ったフロー：<span class=\"hl\">アクションは4つ</span>",
         "point", "PA45 Demo 環境に作ったフローの画面です。<br>メールの送信は<b>それぞれに適用する</b>の中に置くので、行の数だけ送られます",
         flow_stage(150, "vol-150c", [68, 248, 425, 604], 470, steps, "Power Automate デザイナー"),
         uses_bar("向いている人", ["営業事務", "採用の面接案内", "セミナーの当日案内", "保護者への個別連絡"]))

    shots = [
        {"name": "p-excel", "segs": [(0, 80), (280, 790)], "title": "表内に存在する行を一覧表示", "icon": "excel",
         "frames": [(30, 583, 1198, 648, "A"), (30, 714, 1198, 782, "B")],
         "notes": [("A", "ファイルは OneDrive の <b>/PA45一時/面談のご案内_送付先.xlsx</b>"), ("B", "テーブルは Excel で付けた名前 <b>送付先</b>")]},
        {"name": "p-mail", "segs": [(0, 80), (255, 800)], "title": "メールの送信 (V2)", "icon": "outlook", "box_h": 268,
         "frames": [(25, 298, 1080, 357, "C"), (25, 414, 1080, 473, "D"), (25, 603, 1080, 800, "E")],
         "notes": [("C", "宛先は列の <b>メールアドレス</b>"), ("D", "件名に<b>面談日・会社名・氏名</b>"), ("E", "本文にも同じ値。差し込んだ所だけが人ごとに変わる")]},
    ]
    page("vol-150d", "Vol.150-4", "要の設定", "要の設定は<span class=\"hl\">テーブル</span>と<span class=\"hl\">差し込み</span>",
         "guts", "動的コンテンツに <b>会社名・氏名・面談日</b> と Excel の見出しがそのまま並びます。<br>選んで置くだけで、行ごとに違う宛名と日時のメールになります",
         settings_stage(150, "vol-150d", shots), next_bar("添付を付けたいときは、行に<b>ファイル名の列</b>を足して取り出す"))


# ════════════════ Vol.151 フラグを付けたメールを原本で保管（型C変形）
def v151():
    files = [("20261027_0930_tanaka@example.com_見積の件.eml", True), ("20261024_1612_sato@example.com_納期の変更について.eml", False),
             ("20261023_1105_yamada@example.com_仕様の確認.eml", False), ("20261020_0848_suzuki@example.com_契約更新のご案内.eml", False)]
    rows = "".join(f'<tr class="{"hot" if h else ""}"><td>{f}</td></tr>' for f, h in files)
    stage = f'''    <div class="col neutral" style="flex:1">
      <div class="ch2"><span class="n">1</span>大事なメールにフラグ</div>
      <div class="win outlook" style="flex:1"><div class="wh"><img src="{ICON['outlook']}" alt="">受信トレイ</div><div class="wb">
        <div class="mail new" style="display:flex;gap:8px"><div style="flex:1"><div class="mf">田中 健（田中物産）9:30</div><div class="ms">見積の件</div>
          <div class="mb">先日の見積、単価 1,200 円で進めてください。納期は 11/20 で問題ありません。</div></div>
          <svg viewBox="0 0 24 24" width="30" height="30"><path d="M5 3v18" stroke="#B91C1C" stroke-width="2.4"/><path d="M5 4h12l-3 4 3 4H5z" fill="#DC2626"/></svg></div>
        <div class="mail"><div class="mf">社内通知 9:12</div><div class="ms">今週の予定</div></div>
        <div class="mail"><div class="mf">佐藤 花子 8:55</div><div class="ms">会議室の予約</div></div>
      </div></div>
      <div class="cap">押すのは<b>旗のアイコン</b>だけ</div>
    </div>
    <div class="col good" style="flex:1.45">
      <div class="ch2"><span class="n">2</span>案件フォルダーに原本が残る</div>
      <div class="win sp" style="flex:1"><div class="wh"><img src="{ICON['sp']}" alt="">ドキュメント ＞ 案件メール</div><div class="wb">
        <table class="lt"><tr><th>名前（受信日時_差出人_件名.eml）</th></tr>{rows}</table>
        <div style="display:flex;gap:8px;margin-top:auto">
          <span class="tag g">開くと Outlook でそのまま読める</span><span class="tag b">添付も中に入っている</span></div>
      </div></div>
      <div class="cap">言った言わないのときに、<b>日付と相手</b>で探せる</div>
      <img class="chara" src="{A}chara/chara_point.png" alt="" style="position:absolute;right:6px;bottom:52px;height:112px">
    </div>'''
    page("vol-151", "Vol.151-1", "フラグでメールを原本保管", "フラグを付けたメールを、<br><span class=\"hl\">原本のまま案件フォルダー</span>にしまう",
         "smile", "Outlook でフラグを付けると、そのメールを <b>.eml ファイル</b>にして SharePoint の案件フォルダーへ保存します。<br>受信トレイを探さずに、日付と相手からすぐ出せます",
         stage, next_bar(NEXT1))

    cols = [
        {"t": "フラグで動く", "ex": '<div>旗を付けたメール1通ごとに1回動く</div><div style="color:#64748B">フォルダー：Inbox</div>',
         "acts": [("outlook", "メールにフラグが設定されている場合 (V3)", [("フォルダー", "Inbox", True), ("重要度", "Any", False), ("添付ファイルを含める", "いいえ", False)], "")],
         "cap": "フラグは<b>あとで見返すメールの印</b>として付ける"},
        {"t": "原本を取り出す", "ex": '<div>件名・本文・添付をまとめた1つのファイル</div><div style="color:#64748B">（拡張子 .eml）</div>',
         "acts": [("outlook", "メールのエクスポート (V2)", [("メッセージ ID", "メッセージ ID（トリガーの出力）", True)], "メール1通を EML 形式で書き出す")],
         "cap": "転送や印刷と違い、<b>ヘッダーごと</b>残る"},
        {"t": "名前を付けて保存", "ex": '<div style="font-family:Roboto Mono;font-size:13.5px">20261027_0930_tanaka@example.com_見積の件.eml</div>',
         "acts": [("sp", "ファイルの作成", [("フォルダーのパス", "/Shared Documents/案件メール", False), ("ファイル名", "受信日時_差出人_件名.eml", True), ("ファイル コンテンツ", "本文（エクスポートの出力）", True)], "件名の / : ? は replace で置き換える")],
         "cap": "日時を先頭にすると<b>名前順＝時系列</b>"},
    ]
    page("vol-151b", "Vol.151-2", "作り方", "作り方は<span class=\"hl\">3ステップ</span>（フラグ → 書き出す → 保存）",
         "laptop", "<b>メールのエクスポート (V2)</b> の出力を、そのままファイルの中身にします。<br>ファイル名の先頭に受信日時を入れておくと、フォルダーの並びがそのまま時系列になります",
         howto_cols(cols), warn_bar(["フラグ済みのメールに返信やカテゴリ変更をすると、もう一度動くことがある", "件名にファイル名で使えない文字があると保存に失敗する", "案件ごとに分けたいときは件名や差出人で条件を足す"]))

    steps = [("outlook", "メールにフラグが設定されている場合 (V3)", "受信トレイでフラグを付けたら起動", False),
             ("outlook", "メールのエクスポート (V2)", "メッセージ ID を渡して<b>.eml</b> を作る", True),
             ("sp", "ファイルの作成", "<b>案件メール</b>フォルダーに日時_差出人_件名で保存", True),
             ("bulb", "保存したファイルは Outlook で開ける", "ダブルクリックで、受け取ったときと同じ形で読める", False),
             ("bulb", "フォルダーを案件ごとに分けるなら", "条件を足して、件名の言葉で保存先のパスを変える", False)]
    page("vol-151c", "Vol.151-3", "実際のフロー", "実際に作ったフロー：<span class=\"hl\">アクションは3つ</span>",
         "point", "PA45 Demo 環境に作ったフローの画面です。<br>トリガーのあと、<b>書き出す</b>と<b>保存する</b>の2つだけで終わります",
         flow_stage(151, "vol-151c", [88, 288, 468], 470, steps, "Power Automate デザイナー"),
         uses_bar("向いている人", ["営業・購買の担当", "契約や見積を扱う人", "監査に備えたい管理部門", "引き継ぎの多いチーム"]))

    shots = [
        {"name": "p-export", "segs": [(0, 80), (280, 400)], "title": "メールのエクスポート (V2)", "icon": "outlook", "box_h": 200,
         "frames": [(30, 328, 1228, 394, "A")],
         "notes": [("A", "メッセージ ID はトリガーの動的コンテンツ <b>メッセージ ID</b>"), ("A", "出力は<b>本文</b>という名前で次のアクションに出てくる")]},
        {"name": "p-file", "segs": [(0, 80), (380, 710)], "title": "ファイルの作成", "icon": "sp",
         "frames": [(25, 410, 1107, 472, "B"), (25, 530, 1107, 590, "C"), (25, 645, 1107, 705, "D")],
         "notes": [("B", "フォルダーのパス <b>/Shared Documents/案件メール</b>"), ("C", "ファイル名は 受信日時（式）_差出人_件名（式）<b>.eml</b>"),
                   ("D", "ファイル コンテンツにエクスポートの <b>本文</b>")]},
    ]
    page("vol-151d", "Vol.151-4", "要の設定", "要の設定は<span class=\"hl\">ファイル名</span>と<span class=\"hl\">中身</span>",
         "guts", "ファイル名は受信日時を <b>yyyyMMdd_HHmm</b>（日本時間）にし、件名の記号は replace で消します。<br>中身はエクスポートの出力をそのまま渡します",
         settings_stage(151, "vol-151d", shots), next_bar("件名の記号は <b>replace</b> を重ねて、/ : ? を - や空に置き換える"))


# ════════════════ Vol.152 今日のチャネル投稿を夕方に一覧で（型A変形：受信の差）
def v152():
    stage = f'''    <div class="col bad" style="flex:0 0 380px">
      <div class="ph"><span class="mk">{X}</span>会議の合間に追いきれない</div>
      <div class="win teams" style="flex:1"><div class="wh"><img src="{ICON['teams']}" alt="">営業部 ＞ General<span class="tag r" style="margin-left:auto">未読 23</span></div><div class="wb" style="gap:5px">
        <div class="post"><span class="av">佐藤</span><div class="bb"><div class="t">展示会のブース、配置が決まりました</div></div></div>
        <div class="post"><span class="av">鈴木</span><div class="bb"><div class="t">明日の定例は 10:00 からに変更です</div></div></div>
        <div class="post"><span class="av">高橋</span><div class="bb"><div class="t">見積テンプレートを更新しました</div></div></div>
        <div style="text-align:center;font-size:15px;font-weight:900;color:#94A3B8">…ほか 20 件</div>
      </div></div>
      <div class="cap">大事な変更を<b>翌朝知る</b>ことがある</div>
    </div>
    <div class="col good">
      <div class="ph"><span class="mk">{OK}</span>17:30 に今日の分が1通で届く</div>
      <div class="win outlook" style="flex:1"><div class="wh"><img src="{ICON['outlook']}" alt="">受信トレイ</div><div class="wb">
        <div class="mail new"><div class="mf">自分 → 自分　17:30</div><div class="ms">【今日のチャネル】10/27 の投稿まとめ</div>
          <div class="mb">今日、チャネルに投稿されたメッセージです（23 件）。</div></div>
        <table class="lt"><tr><th style="width:70px">時刻</th><th style="width:110px">投稿した人</th><th>内容</th></tr>
          <tr><td>09:12</td><td>佐藤 花子</td><td>展示会のブース、配置が決まりました</td></tr>
          <tr class="hot"><td>11:40</td><td>鈴木 一郎</td><td>明日の定例は 10:00 からに変更です</td></tr>
          <tr><td>14:05</td><td>高橋 美咲</td><td>見積テンプレートを更新しました</td></tr>
          <tr><td>16:48</td><td>田中 健</td><td>来週の訪問先リストを共有します</td></tr></table>
      </div></div>
      <div class="cap">帰る前に<b>上から読むだけ</b>で今日の動きが分かる</div>
      <img class="chara" src="{A}chara/chara_smile.png" alt="" style="position:absolute;right:8px;bottom:52px;height:112px">
    </div>'''
    page("vol-152", "Vol.152-1", "今日のチャネル投稿まとめ", "今日チャネルに投稿されたものが、<br><span class=\"hl\">夕方に一覧のメール</span>で届く",
         "smile", "平日の17:30に、そのチャネルの<b>今日の投稿だけ</b>を表にして自分へメールします。<br>会議続きの日でも、帰る前に1通読めば追いつけます",
         stage, next_bar(NEXT1))

    cols = [
        {"t": "夕方に投稿を取る", "ex": '<div>そのチャネルの投稿が新しい順に取れる</div><div style="color:#64748B">昨日以前の投稿も混ざっている</div>',
         "acts": [("rec", "繰り返し", [("時刻", "平日 17:30", False)], ""),
                  ("teams", "チャネルのメッセージを取得します。", [("チーム", "PA45 Demo", False), ("チャネル", "General", True)], "")],
         "cap": "アクション名の最後に<b>。</b>まで付いている"},
        {"t": "今日の分だけにする", "ex": '<div>作成日時（日本時間の日付）＝ 今日 の投稿だけ残る</div>',
         "acts": [("data", "アレイのフィルター処理", [("From", "メッセージの一覧", False), ("条件", "<code>convertFromUtc(createdDateTime)</code> 等しい 今日", True)], "日付は両方とも yyyy-MM-dd にそろえて比べる")],
         "cap": "UTC のままだと<b>朝9時前</b>の投稿がずれる"},
        {"t": "表にしてメール", "ex": '<div>11:40 ｜ 鈴木 一郎 ｜ 明日の定例は 10:00 から…</div>',
         "acts": [("data", "選択", [("時刻", "HH:mm（日本時間）", False), ("投稿した人", "from.user.displayName", False), ("内容", "<code>take(…, 120)</code>", True)], ""),
                  ("data", "HTML テーブルの作成", [], ""), ("outlook", "メールの送信 (V2)", [("件名", "【今日のチャネル】M/d の投稿まとめ", False)], "")],
         "cap": "内容は<b>120文字</b>で切って読みやすく"},
    ]
    page("vol-152b", "Vol.152-2", "作り方", "作り方は<span class=\"hl\">3ステップ</span>（取る → 今日に絞る → 表で送る）",
         "laptop", "チャネルのメッセージをまとめて取り、<b>アレイのフィルター処理</b>で今日の日付の投稿だけ残します。<br>選択で3列に絞ってから表にすると、メールで読みやすくなります",
         howto_cols(cols), warn_bar(["スレッドへの返信は入らない（返信は別のアクションで取る）", "本文は HTML のまま入る。タグが見えるときは Html からテキストへ を挟む", "見たいチャネルの数だけ同じ組を並べる"]))

    steps = [("rec", "繰り返し", "平日の <b>17:30</b> に起動", False),
             ("teams", "チャネルのメッセージを取得します。", "チーム <b>PA45 Demo</b>／チャネル <b>General</b>", True),
             ("data", "アレイのフィルター処理", "作成日時が<b>今日</b>のものだけ残す", True),
             ("data", "選択", "時刻・投稿した人・内容の3列に", False),
             ("data", "HTML テーブルの作成", "3列を表にする", False),
             ("outlook", "メールの送信 (V2)", "件数と表を自分へ", False)]
    page("vol-152c", "Vol.152-3", "実際のフロー", "実際に作ったフロー：<span class=\"hl\">今日に絞る</span>のが真ん中",
         "point", "PA45 Demo 環境に作ったフローの画面です。<br>取る → 絞る → 整える → 送るの順で、データ操作のアクションが3つ続きます",
         flow_stage(152, "vol-152c", [68, 248, 428, 608, 788, 968], 470, steps, "Power Automate デザイナー"),
         uses_bar("向いている人", ["会議が多い管理職", "複数のチームに入っている人", "時短勤務の人", "現場と事務所を行き来する人"]))

    shots = [
        {"name": "p-channel", "segs": [(0, 80), (280, 530)], "title": "チャネルのメッセージを取得します。", "icon": "teams",
         "frames": [(30, 326, 1228, 520, "A")],
         "notes": [("A", "チームとチャネルは<b>一覧から選ぶ</b>だけ"), ("A", "取ってくるのはチャネルの投稿。返信は入らない")]},
        {"name": "p-filter", "segs": [(0, 80), (280, 595)], "title": "アレイのフィルター処理", "icon": "data",
         "frames": [(30, 330, 1228, 392, "B"), (28, 460, 1230, 520, "C")],
         "notes": [("B", "From は取得の出力 <b>メッセージの一覧</b>"),
                   ("C", "左 <code>convertFromUtc(item()?['createdDateTime'],'Tokyo Standard Time','yyyy-MM-dd')</code> 等しい 右は utcNow() で同じ形")]},
    ]
    page("vol-152d", "Vol.152-4", "要の設定", "要の設定は<span class=\"hl\">今日に絞る条件</span>",
         "guts", "投稿の作成日時は UTC なので、左右とも <b>日本時間の yyyy-MM-dd</b> にしてから比べます。<br>片方だけ直すと、朝9時前の投稿が前の日に入ってしまいます",
         settings_stage(152, "vol-152d", shots), next_bar("宛先を<b>チームの共有アドレス</b>にすると、休みの人の引き継ぎにも使える"))


# ════════════════ Vol.153 OneDrive の写真を年月フォルダーへ（型A）
def v153():
    import random
    random.seed(3)
    cols_ = ["#93C5FD", "#86EFAC", "#FDE68A", "#FCA5A5", "#C4B5FD", "#67E8F9"]
    thumbs = "".join(f'<span style="aspect-ratio:4/3;border-radius:4px;background:linear-gradient(135deg,{random.choice(cols_)},#fff)"></span>' for _ in range(24))
    folders = [("2026-08", 45), ("2026-09", 88), ("2026-10", 62)]
    fold = "".join(f'''<div style="display:flex;align-items:center;gap:10px;border:1.5px solid #DCE3EE;border-radius:9px;padding:7px 10px;background:#fff">
          <svg viewBox="0 0 24 24" width="34" height="34"><path d="M2 6a2 2 0 0 1 2-2h5l2 2h9a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z" fill="#F6C343"/></svg>
          <div style="flex:1"><div class="ms">{n}</div><div class="mf">{c} 枚</div></div>
          <div style="display:grid;grid-template-columns:repeat(4,22px);gap:3px">{"".join(f'<span style="height:16px;border-radius:3px;background:{random.choice(cols_)}"></span>' for _ in range(4))}</div></div>''' for n, c in folders)
    stage = f'''    <div class="col bad">
      <div class="ph"><span class="mk">{X}</span>1つのフォルダーに195枚</div>
      <div class="win od" style="flex:1"><div class="wh"><img src="{ICON['od']}" alt="">写真の受け取り</div><div class="wb">
        <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:5px">{thumbs}</div>
        <div style="font-size:15px;font-weight:800;color:#64748B">IMG_4021.jpg ／ IMG_4022.jpg ／ IMG_4023.jpg …</div>
      </div></div>
      <div class="cap">現場写真を探すのに<b>スクロールが続く</b></div>
      <img class="chara" src="{A}chara/chara_tired.png" alt="" style="position:absolute;right:8px;bottom:50px;height:112px">
    </div>
    <div class="col good">
      <div class="ph"><span class="mk">{OK}</span>入ったそばから年月へ移る</div>
      <div class="win od" style="flex:1"><div class="wh"><img src="{ICON['od']}" alt="">写真</div><div class="wb" style="gap:7px">{fold}
        <div style="font-size:15px;font-weight:800;color:#065F46">写真の受け取り は、いつも空のまま</div></div></div>
      <div class="cap">年月のフォルダーは<b>無くても自動で作られる</b></div>
    </div>'''
    page("vol-153", "Vol.153-1", "写真を年月フォルダーへ", "スマホから上がった写真が、<br><span class=\"hl\">年月のフォルダーへ自動で</span>振り分けられる",
         "smile", "OneDrive の受け取りフォルダーに写真が入ると、<b>2026-10</b> のような年月フォルダーへ移します。<br>フォルダーを先に作っておく必要はありません",
         stage, next_bar(NEXT1))

    cols = [
        {"t": "受け取りフォルダーを見張る", "ex": '<div>スマホの OneDrive アプリで<br>写真の受け取り にアップロード</div><div style="color:#64748B">5分ごとに新しいファイルを確認</div>',
         "acts": [("od", "ファイルの作成時 (プロパティのみ)", [("フォルダー", "/写真の受け取り", True), ("サブフォルダーを含める", "いいえ", False)], "フォルダーはアイコンから選ぶ")],
         "cap": "受け取り専用の<b>空のフォルダー</b>を1つ作る"},
        {"t": "年月のパスへ移す", "ex": '<div style="font-family:Roboto Mono;font-size:14px">/写真/2026-10/IMG_4023.jpg</div><div style="color:#64748B">2026-10 が無ければ作られる</div>',
         "acts": [("od", "ファイルの移動または名前変更", [("ファイル", "{Identifier}", False), ("対象ファイルのパス", "/写真/<code>yyyy-MM</code>/ファイル名", True)], "yyyy-MM は convertFromUtc で作成日時から作る")],
         "cap": "フォルダーが無くても<b>移すときに作られる</b>"},
        {"t": "応用", "ex": '<div>/写真/2026-10/山田工業/… のように<br>案件名の段を足すこともできる</div>',
         "acts": [("od", "対象ファイルのパスを変えるだけ", [("年ごと", "/写真/<code>yyyy</code>/", False), ("種類ごと", "拡張子で分ける", False)], "")],
         "cap": "アクションは<b>増やさずに</b>パスの式だけ変える"},
    ]
    page("vol-153b", "Vol.153-2", "作り方", "作り方は<span class=\"hl\">アクション2つ</span>（見張る → 移す）",
         "laptop", "移動先のパスに<b>年月の式</b>を入れるのが要です。<br>フォルダーが無いときは移すときに作られるので、月が変わっても何もしなくて済みます",
         howto_cols(cols), warn_bar(["分かれるのは撮影日ではなく、OneDrive に入った日の年月", "同じ名前のファイルがあると上書きせず失敗する（上書きは いいえ）", "受け取りフォルダーの中のサブフォルダーは見ない設定"]))

    steps = [("od", "ファイルの作成時 (プロパティのみ)", "<b>/写真の受け取り</b> に入ったら起動", True),
             ("od", "ファイルの移動または名前変更", "<b>/写真/yyyy-MM/</b> ファイル名 へ移す", True),
             ("bulb", "年月フォルダーは自動で作られる", "PA45 第32回の実機で、無いフォルダーが移動のときに作られることを確認", False),
             ("bulb", "日本時間の年月にする", "作成日時は UTC。月末の夜に撮った写真が翌月にならないよう convertFromUtc を使う", False),
             ("bulb", "スマホの自動アップロードとは別", "カメラ ロールの自動バックアップ先ではなく、手で上げる受け取り用フォルダーにしている", False)]
    page("vol-153c", "Vol.153-3", "実際のフロー", "実際に作ったフロー：<span class=\"hl\">アクションは2つ</span>だけ",
         "point", "PA45 Demo 環境に作ったフローの画面です。<br>短いフローですが、<b>移動先のパス</b>に年月の式が入っているのが要です",
         flow_stage(153, "vol-153c", [68, 248], 470, steps, "Power Automate デザイナー", box_w=300, box_h=260),
         uses_bar("向いている人", ["現場写真を撮る施工・保守", "店舗の売場写真", "イベントの記録係", "家族の写真の整理"]))

    shots = [
        {"name": "p-trigger", "segs": [(0, 80), (280, 400)], "title": "ファイルの作成時 (プロパティのみ)", "icon": "od", "box_h": 210,
         "frames": [(32, 330, 1228, 398, "A")],
         "notes": [("A", "フォルダーは <b>/写真の受け取り</b>。右のフォルダーのアイコンから選ぶ"), ("A", "ここに入ったファイルだけが対象になる")]},
        {"name": "p-move", "segs": [(0, 80), (280, 530)], "title": "ファイルの移動または名前変更", "icon": "od",
         "frames": [(32, 330, 1228, 398, "B"), (32, 462, 1228, 528, "C")],
         "notes": [("B", "ファイルはトリガーの <b>{Identifier}</b>"),
                   ("C", "<code>/写真/</code> 式 <code>/</code> ファイル名。式は <code>convertFromUtc(triggerBody()?['{CreatedDate}'],'Tokyo Standard Time','yyyy-MM')</code>")]},
    ]
    page("vol-153d", "Vol.153-4", "要の設定", "要の設定は<span class=\"hl\">移動先のパス</span>の1か所",
         "guts", "対象ファイルのパスに <b>/写真/年月/ファイル名</b> と組みます。<br>年月の部分を式にすると、毎月のフォルダー作りが要らなくなります",
         settings_stage(153, "vol-153d", shots), next_bar("同じ形で<b>請求書の PDF</b> を受け取った月のフォルダーへ片付けることもできる"))


# ════════════════ Vol.154 リストを毎週 CSV でバックアップ（型F：時間の流れ）
def v154():
    weeks = [("10/9（金）", "社員名簿_20261009.csv", False), ("10/16（金）", "社員名簿_20261016.csv", False),
             ("10/23（金）", "社員名簿_20261023.csv", True), ("10/30（金）", "社員名簿_20261030.csv", False)]
    w = "".join(f'''<div class="col {"good" if h else "info"}" style="gap:6px">
        <div class="ch2" style="font-size:21px"><span class="n" style="width:auto;padding:0 8px">18:00</span>{d}</div>
        <div class="win sp" style="flex:1"><div class="wh"><img src="{ICON['sp']}" alt="">バックアップ ＞ 社員名簿</div><div class="wb" style="align-items:center;justify-content:center;gap:8px">
          <svg viewBox="0 0 48 60" width="62" height="78"><path d="M4 2h28l12 12v44H4z" fill="#fff" stroke="#16A34A" stroke-width="3"/><path d="M32 2v12h12" fill="#DCFCE7" stroke="#16A34A" stroke-width="3"/>
            <rect x="9" y="30" width="30" height="14" rx="3" fill="#16A34A"/><text x="24" y="41" font-size="10" font-weight="900" fill="#fff" text-anchor="middle" font-family="Roboto Mono">CSV</text></svg>
          <div style="font-family:Roboto Mono;font-size:13.5px;font-weight:700;color:var(--navy);text-align:center">{f}</div>
          <div style="font-size:14.5px;font-weight:900;color:#64748B">3 行・6 列</div></div></div>
        {('<div class="cap">10/27 に誤って消した行は<b>この版</b>から戻せる</div>' if h else '<div class="cap">毎週この時刻に<b>1つ増える</b></div>')}</div>''' for d, f, h in weeks)
    stage = w + f'\n    <img class="chara" src="{A}chara/chara_confident.png" alt="" style="position:absolute;right:30px;bottom:66px;height:112px">'
    page("vol-154", "Vol.154-1", "リストを毎週CSVで保存", "SharePoint リストを、<br><span class=\"hl\">毎週金曜に CSV で</span>とっておく",
         "confident", "毎週金曜の18時に、リストの全行を<b>日付入りの CSV</b> にして同じフォルダーへ保存します。<br>行を消した・上書きしたときに、先週の中身と見比べて戻せます",
         stage, next_bar(NEXT1), ".stage{position:relative}")

    cols = [
        {"t": "毎週金曜に全行を取る", "ex": '<div>金 18:00 ／ 金 18:00 ／ 金 18:00 …</div><div style="color:#64748B">上位カウント 5000 で全行を取る</div>',
         "acts": [("rec", "繰り返し", [("曜日", "金曜日", True), ("時間", "18", False)], ""),
                  ("sp", "複数の項目の取得", [("リスト名", "社員名簿", False), ("上位カウント", "5000", True)], "指定しないと既定の件数で止まる")],
         "cap": "曜日と時刻は<b>人が触らない時間</b>に"},
        {"t": "CSV の形にする", "ex": '<div style="font-family:Roboto Mono;font-size:13.5px">ID,氏名,部署,誕生日,入社日,更新日時<br>1,山田 太郎,営業部,1990-10-28,…</div>',
         "acts": [("data", "CSV テーブルの作成", [("From", "body/value", False), ("Columns", "カスタム", True), ("見出しと値", "ID・氏名・部署・誕生日…", False)], "列名を日本語の見出しにそろえる")],
         "cap": "カスタムにすると<b>要る列だけ</b>を順番どおりに出せる"},
        {"t": "日付入りで保存", "ex": '<div style="font-family:Roboto Mono;font-size:14px">/バックアップ/社員名簿/<br>社員名簿_20261030.csv</div>',
         "acts": [("sp", "ファイルの作成", [("フォルダーのパス", "/Shared Documents/バックアップ/社員名簿", False), ("ファイル名", "社員名簿_<code>yyyyMMdd</code>.csv", True), ("ファイル コンテンツ", "<code>concat(BOM, CSV)</code>", True)], "BOM を付けると Excel で開いたとき文字化けしない")],
         "cap": "日付をファイル名に入れて<b>上書きしない</b>"},
    ]
    page("vol-154b", "Vol.154-2", "作り方", "作り方は<span class=\"hl\">3ステップ</span>（取る → CSV にする → 保存）",
         "laptop", "取得した行を <b>CSV テーブルの作成</b> で表の文字に変え、日付入りの名前でファイルにします。<br>先頭に BOM を足しておくと、Excel でそのまま開けます",
         howto_cols(cols), warn_bar(["SharePoint にもごみ箱（93日）とバージョン履歴がある。これは追加の保険", "5000 行を超えるリストは、取得の設定でページ処理を有効に", "人や選択肢の列は、表示名を取り出す式にする"]))

    steps = [("rec", "繰り返し", "毎週<b>金曜 18:00</b>（東京）", False),
             ("sp", "複数の項目の取得", "社員名簿の全行（上位 5000）", True),
             ("data", "CSV テーブルの作成", "6列を<b>日本語の見出し</b>で", True),
             ("sp", "ファイルの作成", "<b>社員名簿_yyyyMMdd.csv</b> で保存", True),
             ("bulb", "保存先はリストと同じサイトのライブラリ", "サイトごと消えると一緒に無くなる。重要なら別のサイトにも置く", False)]
    page("vol-154c", "Vol.154-3", "実際のフロー", "実際に作ったフロー：<span class=\"hl\">アクションは4つ</span>",
         "point", "PA45 Demo 環境に作ったフローの画面です。<br>取る → 形を変える → 保存する、の一本道です",
         flow_stage(154, "vol-154c", [68, 248, 428, 608], 470, steps, "Power Automate デザイナー"),
         uses_bar("向いている人", ["リストで台帳を回している総務", "複数人で編集するリスト", "監査で過去の状態を出す必要がある部署"]))

    shots = [
        {"name": "p-csv", "segs": [(0, 80), (255, 360), (630, 1068)], "title": "CSV テーブルの作成", "icon": "data", "box_h": 322,
         "frames": [(27, 296, 1082, 355, "A"), (27, 735, 1082, 1068, "B")],
         "notes": [("A", "From は取得の <b>body/value</b>（行の一覧）"), ("B", "Columns を <b>カスタム</b>にして、見出しと値を1行ずつ")]},
        {"name": "p-file", "segs": [(0, 80), (380, 710)], "title": "ファイルの作成", "icon": "sp",
         "frames": [(27, 411, 1108, 473, "C"), (27, 531, 1108, 591, "D"), (27, 646, 1108, 706, "E")],
         "notes": [("C", "フォルダーのパス <b>/Shared Documents/バックアップ/社員名簿</b>"), ("D", "ファイル名に <code>yyyyMMdd</code> の日付"),
                   ("E", "<code>concat(uriComponentToString('%EF%BB%BF'), body('CSV_テーブルの作成'))</code> で BOM を先頭に")]},
    ]
    page("vol-154d", "Vol.154-4", "要の設定", "要の設定は<span class=\"hl\">列の指定</span>と<span class=\"hl\">BOM</span>",
         "guts", "CSV の列は<b>カスタム</b>で決めておくと、リストに列が増えてもファイルの形が変わりません。<br>中身の先頭に BOM を付けて、日本語が Excel で化けないようにします",
         settings_stage(154, "vol-154d", shots), next_bar("戻すときは CSV を Excel で開き、<b>消えた行だけ</b>リストに貼り直す"))


if __name__ == "__main__":
    for f in (v150, v151, v152, v153, v154):
        f()
    print("ok")

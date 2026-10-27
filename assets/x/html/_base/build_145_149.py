# -*- coding: utf-8 -*-
"""X技術Tips Vol.145〜149（2026-10-27 作り直し）の4枚組を生成する。python build_145_149.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x145lib import *

NEXT1 = "作り方は<b>2枚目</b>、実際に作ったフローの画面は<b>3・4枚目</b>"


# ════════════════ Vol.145 毎朝、天気と予定が1通で届く（型C：主役モック）
def v145():
    sun = ('<svg viewBox="0 0 120 120" width="88" height="88"><defs><radialGradient id="sg" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#FFE38A"/>'
           '<stop offset="1" stop-color="#F59E0B"/></radialGradient><linearGradient id="cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/>'
           '<stop offset="1" stop-color="#CBD5E1"/></linearGradient></defs><circle cx="50" cy="48" r="26" fill="url(#sg)"/>'
           '<path d="M38 96h56a17 17 0 0 0 0-34 24 24 0 0 0-45-6 16 16 0 0 0-11 40z" fill="url(#cg)" stroke="#94A3B8" stroke-width="2"/></svg>')
    stage = f'''    <div class="col bad" style="flex:0 0 340px">
      <div class="ph"><span class="mk">{SVGW('<path d="M6 6l12 12M18 6L6 18"/>', 3)}</span>朝に3つのアプリを開く</div>
      <div class="body" style="gap:8px">
        <div class="win" style="flex:0 0 auto"><div class="wh" style="background:#0EA5E9">天気アプリ</div><div class="wb"><div class="t" style="font-size:15.5px;font-weight:800;color:#0F172A">くもり　降水確率 60%</div></div></div>
        <div class="win outlook" style="flex:0 0 auto"><div class="wh"><img src="{ICON['outlook']}" alt="">予定表</div><div class="wb"><div style="font-size:15.5px;font-weight:800;color:#0F172A">9:30 定例…11:00 は何だったか</div></div></div>
        <div class="win teams" style="flex:0 0 auto"><div class="wh"><img src="{ICON['teams']}" alt="">Teams</div><div class="wb"><div style="font-size:15.5px;font-weight:800;color:#0F172A">未読を追ううちに家を出る時間</div></div></div>
        <div class="cap" style="margin-right:96px">傘を忘れる日と、<b>最初の会議を見落とす日</b>が出る</div>
      </div>
      <img class="chara" src="{A}chara/chara_trouble.png" alt="" style="position:absolute;right:2px;bottom:6px;height:118px">
    </div>
    <div class="col good" style="flex:1">
      <div class="ph"><span class="mk">{SVGW('<path d="M5 12l5 5 9-10"/>', 3)}</span>7:30 に Teams へ1通だけ届く</div>
      <div class="win teams" style="flex:1"><div class="wh"><img src="{ICON['teams']}" alt="">Teams チャット ＞ Workflows</div>
        <div class="wb" style="gap:8px">
          <div class="post bot"><span class="av">PA</span><div class="bb"><div class="nm">フロー ボット<i>7:30</i></div>
            <div class="t" style="display:flex;gap:12px;align-items:center">{sun}<div><b style="font-size:19px">おはようございます。今日の天気と予定です。</b><br>
              天気：くもり時々雨　最高 18℃／最低 11℃　<span class="tag b">降水確率 60%</span></div></div>
            <table class="lt" style="margin-top:6px"><tr><th style="width:90px">時刻</th><th>予定</th><th style="width:170px">場所</th></tr>
              <tr class="hot"><td>09:30</td><td>営業部 定例</td><td>Teams 会議</td></tr>
              <tr><td>11:00</td><td>山田工業さま 打ち合わせ</td><td>本社 3F 会議室B</td></tr>
              <tr><td>15:00</td><td>見積の締め</td><td></td></tr></table>
          </div></div>
        </div></div>
      <div class="metric"><span class="ml">朝に開くアプリ</span><span class="mv">3つ</span><span class="ar">{SVGW(P_ARROW, 3)}</span><span class="mv to">Teams 1通</span><span class="ml">平日だけ・7:30</span></div>
    </div>'''
    page("vol-145", "Vol.145-1", "毎朝の天気と予定", "毎朝7:30、<span class=\"hl\">今日の天気と予定</span>が<br>Teams に1通で届く",
         "smile", "天気と今日の予定を、フロー ボットが平日の朝に自分の Teams へ送ります。<br>傘が要るかと最初の会議の時刻を、<b>家を出る前に1か所で</b>確かめられます",
         stage, next_bar(NEXT1), ".col.bad .body{position:relative}")

    cols = [
        {"t": "毎朝7:30に動かす", "ex": '<div>月 7:30 ／ 火 7:30 ／ 水 7:30 ／ 木 7:30 ／ 金 7:30</div><div style="color:#94A3B8">土・日は起動しない</div>', "acts": [("rec", "繰り返し", [("頻度", "週", False), ("曜日", "月〜金", False), ("時刻", "7 時 30 分", True), ("タイム ゾーン", "大阪、札幌、東京", False)], "土日は動かない設定にしておく")],
         "cap": "タイム ゾーンを<b>東京</b>にしないと9時間ずれる"},
        {"t": "今日の天気を取る", "ex": '<div>日 条件：くもり時々雨</div><div>最高気温 18 ／ 最低気温 11</div><div>日 降水確率 60</div>', "acts": [("weather", "今日の予測を取得する", [("場所", "東京都千代田区", True), ("単位", "Metric", False)], "MSN 天気は標準コネクタ。サインインは要らない")],
         "cap": "場所は<b>市区町村名</b>でも郵便番号でも入る"},
        {"t": "今日の予定を取る", "ex": '<table class="lt"><tr><th>subject</th><th>start（UTC）</th></tr><tr><td>営業部 定例</td><td>00:30</td></tr><tr><td>打ち合わせ</td><td>02:00</td></tr></table>', "acts": [("outlook", "イベントの予定表ビューを取得する (V3)", [("カレンダー ID", "Calendar", False), ("開始時刻", "<code>utcNow()</code>", True), ("終了時刻", "<code>addHours(utcNow(), 14)</code>", True)], "朝から14時間分＝夜までの予定")],
         "cap": "開始・終了は<b>UTC で入れる</b>欄"},
        {"t": "表にして Teams へ", "acts": [("data", "選択", [("時刻", "<code>convertFromUtc(…,'HH:mm')</code>", True), ("予定", "subject", False)], ""),
                                            ("data", "HTML テーブルの作成", [], ""),
                                            ("teams", "チャットまたはチャネルでメッセージを投稿する", [("投稿先", "フロー ボットとチャットをする", False)], "")],
         "cap": "予定の時刻は<b>日本時間に直してから</b>表へ"},
    ]
    page("vol-145b", "Vol.145-2", "作り方", "作り方は<span class=\"hl\">4ステップ</span>（時刻 → 天気 → 予定 → 投稿）",
         "laptop", "天気は<b>MSN 天気</b>、予定は<b>予定表ビュー</b>で取り、Teams の1通にまとめます。<br>コネクタはどちらも標準なので、追加のライセンスは要りません",
         howto_cols(cols), warn_bar(["予定表の時刻は UTC。表にする前に convertFromUtc で日本時間へ", "MSN 天気の呼び出しは1接続あたり60秒に8回まで", "予定が無い日は表が空のまま届く"]))

    steps = [("rec", "繰り返し", "平日の <b>7:30</b>（月〜金・東京）に起動", False),
             ("weather", "今日の予測を取得する", "場所 <b>東京都千代田区</b>・単位 Metric", True),
             ("outlook", "イベントの予定表ビューを取得する (V3)", "いまから14時間ぶんの予定を取る", True),
             ("data", "選択", "時刻・予定・場所の3列に絞る", False),
             ("data", "HTML テーブルの作成", "3列をそのまま表にする", False),
             ("teams", "チャットまたはチャネルでメッセージを投稿する", "天気の値と表を<b>フロー ボット</b>から自分へ", True)]
    page("vol-145c", "Vol.145-3", "実際のフロー", "実際に作ったフロー：<span class=\"hl\">アクションは6つ</span>",
         "point", "PA45 Demo 環境に作ったフローの画面です。<br>上から順に、時刻 → 天気 → 予定 → 表 → 投稿の並びになっています",
         flow_stage(145, "vol-145c", [68, 248, 428, 608, 788, 985], 470, steps, "Power Automate デザイナー"),
         uses_bar("向いている人", ["外回りの営業", "現場に直行する人", "朝に会議が多い管理職", "在宅と出社が混ざる人"]))

    shots = [
        {"name": "p-weather", "segs": [(0, 80), (280, 540)], "title": "今日の予測を取得する", "icon": "weather",
         "frames": [(25, 325, 1233, 397, "A"), (25, 453, 1233, 527, "B")],
         "notes": [("A", "場所は<b>住所の言葉そのまま</b>。東京都千代田区で通る"), ("B", "単位は Metric（℃）。Imperial にすると °F で返る")]},
        {"name": "p-teams", "segs": [(0, 80), (370, 470), (690, 960)], "title": "チャットまたはチャネルでメッセージを投稿する", "icon": "teams",
         "frames": [(25, 408, 1080, 467, "C"), (25, 712, 1080, 955, "D")],
         "notes": [("C", "投稿先 <b>フロー ボットとチャットをする</b>＝自分だけに届く"), ("D", "天気の欄は<b>日 条件・最高気温・最低気温・日 降水確率</b>を選ぶ")]},
    ]
    page("vol-145d", "Vol.145-4", "要の設定", "要の設定は<span class=\"hl\">場所</span>と<span class=\"hl\">本文の4つの値</span>",
         "guts", "天気の値は、動的コンテンツで<b>日 条件・最高気温・最低気温・日 降水確率</b>を選ぶと日本語の名前で並びます。<br>予定の表は「HTML テーブルの作成」の Output をそのまま差し込みます",
         settings_stage(145, "vol-145d", shots, box_h=400), next_bar("宛先を<b>チャネル</b>にすると、チーム全員の朝の連絡にも使える"))


# ════════════════ Vol.146 申込者へ受付番号入りの確認メール（型A：Before/After）
def v146():
    stage = f'''    <div class="col bad">
      <div class="ph"><span class="mk">{SVGW('<path d="M6 6l12 12M18 6L6 18"/>', 3)}</span>申し込んだ人が不安になる</div>
      <div class="win outlook" style="flex:1"><div class="wh"><img src="{ICON['outlook']}" alt="">受信トレイ（担当者）</div><div class="wb">
        <div class="mail"><div class="mf">佐藤 花子</div><div class="ms">申し込めていますか？</div><div class="mb">フォームを送りましたが、何も届かないので念のため…</div></div>
        <div class="mail"><div class="mf">鈴木 一郎</div><div class="ms">先ほどの申込について</div><div class="mb">二重に送ったかもしれません。確認をお願いします</div></div>
        <div class="mail"><div class="mf">高橋 美咲</div><div class="ms">キャンセルしたい</div><div class="mb">どの申込か分かるように、何を伝えればよいですか</div></div>
      </div></div>
      <div class="cap">確認の返事を<b>1件ずつ手で</b>書くことになる</div>
      <img class="chara" src="{A}chara/chara_tired.png" alt="" style="position:absolute;right:6px;bottom:46px;height:112px">
    </div>
    <div class="col good">
      <div class="ph"><span class="mk">{SVGW('<path d="M5 12l5 5 9-10"/>', 3)}</span>送った直後に受付番号が届く</div>
      <div class="win outlook" style="flex:1"><div class="wh"><img src="{ICON['outlook']}" alt="">受信トレイ（申し込んだ人）</div><div class="wb">
        <div class="mail new"><div class="mf">セミナー事務局　10:02</div><div class="ms">【受付番号 A-12】お申し込みを受け付けました</div>
          <div class="mb">お申し込みありがとうございます。<br><b style="color:#0F6CBD;font-size:19px">受付番号：A-12</b><br>当日の受付でこの番号をお伝えください。<br>変更・キャンセルのときも、この番号をお知らせください。</div></div>
        <table class="lt"><tr><th style="width:70px">ID</th><th>氏名</th><th>申込セミナー</th></tr>
          <tr class="dim"><td>11</td><td>山田 太郎</td><td>11月 はじめての自動化セミナー</td></tr>
          <tr class="hot"><td>12</td><td>佐藤 花子</td><td>11月 はじめての自動化セミナー</td></tr></table>
      </div></div>
      <div class="cap">番号は<b>リストの ID</b>。重ならないので問い合わせがすぐ引ける</div>
    </div>'''
    page("vol-146", "Vol.146-1", "受付番号つきの確認メール", "申込フォームに答えた人へ、<br><span class=\"hl\">受付番号入りの確認メール</span>がすぐ届く",
         "smile", "フォームの回答を SharePoint リストに1行入れ、その行の <b>ID を受付番号</b>にしてメールを返します。<br>申し込めたかの問い合わせと、どの申込かを探す手間が減ります",
         stage, next_bar(NEXT1))

    cols = [
        {"t": "回答が届いたら動く", "ex": '<div>回答者：sato@contoso.com</div><div>送信時刻：10:02</div>', "acts": [("forms", "新しい応答が送信されるとき", [("フォーム ID", "申込フォームを選ぶ", True)], ""),
                                          ("forms", "応答の詳細を取得する", [("応答 ID", "応答 ID（動的コンテンツ）", False)], "回答の中身はこの2つ目で取る")],
         "cap": "フォームは<b>組織内で名前を記録</b>する設定に"},
        {"t": "申込台帳に1行入れる", "ex": '<table class="lt"><tr><th>ID</th><th>氏名</th></tr><tr class="dim"><td>11</td><td>山田 太郎</td></tr><tr class="hot"><td>12</td><td>佐藤 花子</td></tr></table>', "acts": [("sp", "項目の作成", [("リスト名", "申込台帳", True), ("氏名", "Responders' Email", False), ("メールアドレス", "Responders' Email", False), ("申込セミナー", "11月 はじめての自動化セミナー", False)], "")],
         "cap": "作った行には<b>ID が自動で振られる</b>"},
        {"t": "受付番号を入れて返信", "ex": '<div style="font-weight:900">【受付番号 A-12】お申し込みを受け付けました</div><div>受付番号：A-12</div>', "acts": [("outlook", "メールの送信 (V2)", [("宛先", "Responders' Email", False), ("件名", "【受付番号 A-<code>ID</code>】お申し込みを…", True), ("本文", "受付番号：A-<code>ID</code>", True)], "ID は「項目の作成」の動的コンテンツから選ぶ")],
         "cap": "A- のような<b>頭の文字</b>を付けると番号らしく見える"},
    ]
    page("vol-146b", "Vol.146-2", "作り方", "作り方は<span class=\"hl\">3ステップ</span>（受け取る → 台帳に入れる → 返信）",
         "laptop", "リストの <b>ID</b> は1から順に振られ、同じ番号は二度と使われません。<br>この性質をそのまま受付番号に使うので、番号を数える仕組みを作らなくて済みます",
         howto_cols(cols), warn_bar(["Responders' Email が入るのは、組織内で回答者を記録するフォームだけ", "社外の人の申込は、メールアドレスの質問を作ってその回答を宛先に", "まず自分で1回答えて届くか確かめる"]))

    steps = [("forms", "新しい応答が送信されるとき", "申込フォームに回答が届いたら起動", False),
             ("forms", "応答の詳細を取得する", "回答した人のメールアドレスなどを取る", False),
             ("sp", "項目の作成", "<b>申込台帳</b>に1行。ここで ID が決まる", True),
             ("outlook", "メールの送信 (V2)", "件名と本文に <b>A-ID</b> を入れて返信", True),
             ("bulb", "番号を数える変数は使っていない", "ID はリストが振るので、同時に2人が送っても番号は重ならない", False)]
    page("vol-146c", "Vol.146-3", "実際のフロー", "実際に作ったフロー：<span class=\"hl\">アクションは4つ</span>だけ",
         "point", "PA45 Demo 環境に作ったフローの画面です。<br>受付番号を作る専用の仕組みは無く、<b>項目の作成</b>の結果をそのまま使っています",
         flow_stage(146, "vol-146c", [68, 248, 428, 608], 488, steps, "Power Automate デザイナー", box_w=360),
         uses_bar("向いている人", ["セミナー・勉強会の事務局", "社内研修の受付", "備品の貸出申請", "相談窓口"]))

    shots = [
        {"name": "p-create", "segs": [(0, 80), (375, 600), (855, 1000)], "title": "項目の作成", "icon": "sp",
         "frames": [(25, 408, 1078, 468, "A"), (25, 887, 1012, 946, "B")],
         "notes": [("A", "リスト名は<b>申込台帳</b>。列は氏名・メールアドレス・申込セミナー"), ("B", "メールアドレスは <b>Responders' Email</b> を選ぶ")]},
        {"name": "p-mail", "segs": [(0, 80), (255, 700)], "title": "メールの送信 (V2)", "icon": "outlook",
         "frames": [(25, 413, 1078, 472, "C"), (40, 652, 720, 700, "D")],
         "notes": [("C", "件名の <b>ID</b> は「項目の作成」の動的コンテンツ"), ("D", "本文にも同じ ID。受付で番号を言ってもらう")]},
    ]
    page("vol-146d", "Vol.146-4", "要の設定", "要の設定は<span class=\"hl\">件名と本文の ID</span>",
         "guts", "メールの件名と本文に、<b>項目の作成</b>の出力 ID を差し込みます。<br>台帳の行と受付番号が同じなので、問い合わせが来たら ID で1行に絞れます",
         settings_stage(146, "vol-146d", shots, box_h=400), next_bar("キャンセルの連絡も<b>受付番号で受ける</b>と、台帳のどの行かすぐ分かる"))


# ════════════════ Vol.147 新人に毎朝その日の資料（型F：紙芝居4コマ）
def v147():
    def koma(day, date, title, point, cap, reply, hot=False):
        return f'''<div class="col {"good" if hot else "info"}" style="gap:6px">
        <div class="ch2" style="font-size:21px"><span class="n" style="width:auto;padding:0 8px">{day}日目</span>{date}</div>
        <div class="win teams" style="flex:1"><div class="wh"><img src="{ICON['teams']}" alt="">Teams ＞ Workflows</div><div class="wb">
          <div class="post bot"><span class="av">PA</span><div class="bb"><div class="nm">フロー ボット<i>8:30</i></div>
            <div class="t" style="font-size:16.5px"><b>入社 {day} 日目の資料です</b><br>{title}<br><span style="color:#64748B;font-size:14.5px">読むポイント：{point}</span><br><span style="color:#2563EB;text-decoration:underline">資料を開く</span></div></div></div>
          <div class="post" style="margin-left:30px"><span class="av" style="background:#0891B2">新人</span><div class="bb"><div class="t" style="font-size:15px">{reply}</div></div></div>
          <div style="margin-top:auto"><div style="font-size:13.5px;font-weight:900;color:#64748B;margin-bottom:3px">30日のうち {day} 日目</div>
            <div style="display:grid;grid-template-columns:repeat(10,1fr);gap:4px">{"".join(f'<span style="height:14px;border-radius:4px;background:{"#16A34A" if k+1==day else ("#93C5FD" if k+1<day else ("#F1F5F9" if (k+1)%7 in (6,0) else "#E2E8F0"))}"></span>' for k in range(30))}</div></div>
        </div></div><div class="cap">{cap}</div></div>'''
    stage = "\n".join([koma(1, "11/2（月）", "ようこそ：最初の1週間の過ごし方", "予定表と席の場所", "初日は<b>1つだけ</b>読めばよい", "席と予定表、確認しました"),
                       koma(3, "11/4（水）", "経費精算のしかた", "締切は毎月25日", "使う<b>直前</b>に届く", "ちょうど今日、交通費を出します"),
                       koma(5, "11/6（金）", "部署の仕事の全体像", "誰が何を担当しているか", "1週目の終わりに<b>全体</b>を見る", "誰に聞けばいいか分かりました"),
                       koma(8, "11/9（月）", "1週目のふりかえり", "分からなかったことを3つ", "土日の6・7日目は<b>行を作らない</b>", "3つ書いて上長に送ります", True)])
    page("vol-147", "Vol.147-1", "新人に毎朝の資料", "入社の日から毎朝、<br><span class=\"hl\">その日に読む資料</span>が1つずつ届く",
         "smile", "初日にリンク集をまとめて渡す代わりに、<b>毎朝8:30に1つだけ</b>新人の Teams へ届けます。<br>何日目に何を読むかは、リストに1行ずつ書いておくだけです",
         stage, next_bar(NEXT1), ".stage{position:relative}")

    cols = [
        {"t": "毎朝動かして日数を出す", "acts": [("rec", "繰り返し", [("時刻", "平日 8:30", False)], ""),
                                            ("var", "変数を初期化する", [("入社日", "2026-11-02", True), ("新人のメール", "本人のアドレス", False)], ""),
                                            ("data", "作成", [("入力", "<code>add(div(sub(ticks(今日), ticks(入社日)), 864000000000), 1)</code>", True)], "入社日を1日目として何日目かを出す")],
         "cap": "新人が来るたび<b>変数2つ</b>を書き換える"},
        {"t": "その日の資料を探す", "ex": '<table class="lt"><tr><th>DayNo</th><th>資料名</th></tr><tr class="dim"><td>2</td><td>社内のチャットの使い方</td></tr><tr class="hot"><td>3</td><td>経費精算のしかた</td></tr><tr class="dim"><td>4</td><td>勤怠の入力ルール</td></tr></table>', "acts": [("sp", "複数の項目の取得", [("リスト名", "新人の30日", False), ("フィルター クエリ", "DayNo eq <code>出力</code>", True)], "何日目（DayNo）が今日の数字の行だけ取る")],
         "cap": "リストは<b>何日目・資料名・リンク・読むポイント</b>"},
        {"t": "本人の Teams へ送る", "ex": '<div style="font-weight:900">入社 3 日目の資料です</div><div>経費精算のしかた</div><div style="color:#64748B">読むポイント：締切は毎月25日</div>', "acts": [("ctrl", "それぞれに適用する", [], ""),
                                          ("teams", "チャットまたはチャネルでメッセージを投稿する", [("Recipient", "新人のメール（変数）", True), ("メッセージ", "資料名・読むポイント・リンク", False)], "")],
         "cap": "その日の行が無ければ<b>何も送らない</b>"},
    ]
    page("vol-147b", "Vol.147-2", "作り方", "作り方は<span class=\"hl\">3ステップ</span>（日数を出す → 探す → 送る）",
         "laptop", "<b>何日目</b>を式で出し、同じ数字の行をリストから取ります。<br>資料を差し替えたいときは、フローを触らずリストの行を直すだけで済みます",
         howto_cols(cols), warn_bar(["日数は土日も数える。土日にあたる日（6・7日目など）の行は作らない", "入社日は日本時間の日付で比べる式にしている", "新人が複数なら、入社日と宛先もリストで持つ形に広げる"]))

    steps = [("rec", "繰り返し", "平日の 8:30 に起動", False),
             ("var", "変数を初期化する", "<b>入社日</b> 2026-11-02", True),
             ("var", "変数を初期化する 1", "<b>新人のメール</b>（送り先）", False),
             ("data", "作成", "今日が入社<b>何日目</b>かを式で出す", True),
             ("sp", "複数の項目の取得", "新人の30日から DayNo が同じ行", True),
             ("ctrl", "それぞれに適用する", "見つかった行ごとに", False),
             ("teams", "チャットまたはチャネルでメッセージを投稿する", "資料名とリンクを本人へ", False)]
    page("vol-147c", "Vol.147-3", "実際のフロー", "実際に作ったフロー：<span class=\"hl\">日数の計算</span>が真ん中",
         "point", "PA45 Demo 環境に作ったフローの画面です。<br>入社日と宛先を変数にしてあるので、次の新人のときは<b>上の2つだけ</b>書き換えます",
         flow_stage(147, "vol-147c", [65, 215, 365, 515, 665, 810, 975], 418, steps, "Power Automate デザイナー"),
         uses_bar("向いている人", ["人事・総務の受け入れ担当", "新人の指導役", "異動者の引き継ぎ", "アルバイトの研修"]))

    shots = [
        {"name": "p-expr", "segs": [(0, 200)], "title": "作成 ＞ 式", "icon": "data", "box_h": 180,
         "frames": [(10, 66, 935, 192, "A")],
         "notes": [("A", "<code>ticks</code> の差を <code>864000000000</code>（1日ぶん）で割って日数にし、<b>＋1</b>で入社日を1日目にする"),
                   ("A", "今日の日付は <code>convertFromUtc(utcNow(),'Tokyo Standard Time','yyyy-MM-dd')</code> で日本時間にしてから比べる")]},
        {"name": "p-get", "segs": [(0, 80), (375, 470), (740, 840)], "title": "複数の項目の取得", "icon": "sp",
         "frames": [(25, 408, 1078, 468, "B"), (25, 772, 1040, 832, "C")],
         "notes": [("B", "リスト名 <b>新人の30日</b>"), ("C", "フィルター クエリ <code>DayNo eq</code> のあとに「作成」の<b>出力</b>")]},
    ]
    page("vol-147d", "Vol.147-4", "要の設定", "要の設定は<span class=\"hl\">日数の式</span>と<span class=\"hl\">フィルター</span>",
         "guts", "「作成」で今日が何日目かを出し、その数字で<b>リストの行を1つに絞り</b>ます。<br>DayNo は数値の列なので、フィルターの値を ' で囲まずに書きます",
         settings_stage(147, "vol-147d", shots, box_h=400), next_bar("資料を足すときは<b>リストに1行</b>。フローはそのまま"))


# ════════════════ Vol.148 誕生日・入社記念日のお祝い（型D：会話スレッド）
def v148():
    stage = f'''    <div class="col info" style="flex:1.35">
      <div class="win teams" style="flex:1"><div class="wh"><img src="{ICON['teams']}" alt="">PA45 Demo ＞ General</div><div class="wb" style="gap:7px">
        <div class="post bot"><span class="av">PA</span><div class="bb"><div class="nm">フロー ボット<i>9:00</i></div>
          <div class="t"><b style="font-size:18px">今日は営業部の山田 太郎さんの誕生日です！</b><br>おめでとうございます。ひとことお祝いをどうぞ。</div></div></div>
        <div class="post" style="margin-left:40px"><span class="av" style="background:#DB2777">佐藤</span><div class="bb"><div class="nm">佐藤 花子<i>9:04</i></div><div class="t">おめでとうございます！今日の打ち合わせ、ケーキ持っていきます</div></div></div>
        <div class="post" style="margin-left:40px"><span class="av" style="background:#0891B2">鈴木</span><div class="bb"><div class="nm">鈴木 一郎<i>9:11</i></div><div class="t">おめでとうございます。いつも相談に乗ってもらって助かってます</div></div></div>
        <div class="post bot"><span class="av">PA</span><div class="bb"><div class="nm">フロー ボット<i>9:00</i></div>
          <div class="t"><b style="font-size:18px">佐藤 花子さん、入社 5 年目おめでとうございます！</b><br>いつもありがとうございます。</div></div></div>
      </div></div>
    </div>
    <div class="col neutral" style="flex:1">
      <div class="ch2"><span class="n">名</span>名簿に月日を持たせる</div>
      <div class="win sp" style="flex:1"><div class="wh"><img src="{ICON['sp']}" alt="">社員名簿（SharePoint リスト）</div><div class="wb">
        <table class="lt"><tr><th>氏名</th><th>部署</th><th>誕生日の月日</th><th>入社の月日</th></tr>
          <tr class="hot"><td>山田 太郎</td><td>営業部</td><td>10-28</td><td>04-01</td></tr>
          <tr><td>佐藤 花子</td><td>総務部</td><td>06-12</td><td style="background:#ECFDF5;color:#065F46;font-weight:900">10-28</td></tr>
          <tr><td>鈴木 一郎</td><td>開発部</td><td>12-03</td><td>04-01</td></tr></table>
        <div class="cap" style="margin-top:auto">今日が <b>10-28</b> の行だけを毎朝拾う</div>
      </div></div>
      <img class="chara" src="{A}chara/chara_point.png" alt="" style="position:absolute;right:4px;bottom:8px;height:112px">
    </div>'''
    page("vol-148", "Vol.148-1", "誕生日と入社記念日のお祝い", "誕生日と入社記念日の朝に、<br><span class=\"hl\">チャネルへお祝いが自動で投稿</span>される",
         "smile", "名簿に<b>月日だけの列</b>（10-28 など）を持たせ、今日と同じ人をフローが毎朝探してチャネルに投稿します。<br>覚えている人がいなくても、お祝いの声かけが漏れません",
         stage, next_bar(NEXT1), ".col.neutral{position:relative}")

    cols = [
        {"t": "今日の月日で探す", "ex": '<div>今日 2026-10-28 → <b style="color:#1D4ED8">10-28</b> の山田 太郎</div>', "acts": [("rec", "繰り返し", [("時刻", "毎朝 9:00", False)], ""),
                                       ("sp", "複数の項目の取得", [("リスト名", "社員名簿", False), ("フィルター クエリ", "MonthDay eq '<code>今日の MM-dd</code>'", True)], "今日の MM-dd は convertFromUtc で日本時間にして作る")],
         "cap": "日付の列ではなく<b>月日の文字列</b>で比べる"},
        {"t": "見つかった人を祝う", "ex": '<div style="font-weight:900">今日は営業部の山田 太郎さんの誕生日です！</div><div>おめでとうございます。ひとことお祝いをどうぞ。</div>', "acts": [("ctrl", "それぞれに適用する", [], ""),
                                         ("teams", "チャットまたはチャネルでメッセージを投稿する", [("投稿先", "チャネル", False), ("チーム／チャネル", "PA45 Demo／General", False), ("メッセージ", "部署・氏名を差し込む", True)], "")],
         "cap": "該当者がいない日は<b>何も投稿しない</b>"},
        {"t": "入社記念日も同じ形で", "ex": '<div>2026 − 2021 ＝ 5</div><div style="font-weight:900">佐藤 花子さん、入社 5 年目おめでとうございます！</div>', "acts": [("sp", "複数の項目の取得 1", [("フィルター クエリ", "JoinMonthDay eq '…'", True)], ""),
                                           ("teams", "チャットまたはチャネルでメッセージを投稿する 1", [("年数", "今年 − 入社年", True)], "年数は int で年どうしを引く")],
         "cap": "2組並べるだけで<b>記念日も</b>祝える"},
    ]
    page("vol-148b", "Vol.148-2", "作り方", "作り方は<span class=\"hl\">3ステップ</span>（探す → 祝う → 記念日も）",
         "laptop", "誕生日を日付の列で比べると年が邪魔をするので、名簿に <b>10-28 のような月日の列</b>を作ります。<br>フィルターは文字列どうしの一致になり、1行で書けます",
         howto_cols(cols), warn_bar(["誕生日を載せてよいか、本人に確認してから名簿に入れる", "平日だけ動かすと土日生まれの人が飛ぶ。毎日動かすか、金曜に週末分もまとめる", "月日の列は 01-05 のように0を付けた2桁で揃える"]))

    steps = [("rec", "繰り返し", "平日の 9:00 に起動", False),
             ("sp", "複数の項目の取得", "MonthDay が<b>今日の MM-dd</b> の人", True),
             ("ctrl", "それぞれに適用する", "該当した人ごとに", False),
             ("teams", "チャットまたはチャネルでメッセージを投稿する", "General へ<b>誕生日</b>のお祝い", True),
             ("sp", "複数の項目の取得 1", "JoinMonthDay が今日の人", False),
             ("ctrl", "それぞれに適用する 1", "該当した人ごとに", False),
             ("teams", "チャットまたはチャネルでメッセージを投稿する 1", "入社<b>何年目</b>かを添えて投稿", True)]
    page("vol-148c", "Vol.148-3", "実際のフロー", "実際に作ったフロー：<span class=\"hl\">同じ形が2組</span>",
         "point", "PA45 Demo 環境に作ったフローの画面です。<br>上の組が誕生日、下の組が入社記念日。違うのは<b>フィルターの列名</b>とメッセージだけです",
         flow_stage(148, "vol-148c", [45, 172, 295, 425, 637, 760, 890], 335, steps, "Power Automate デザイナー", box_w=300),
         uses_bar("向いている人", ["総務・人事", "チームリーダー", "店舗の店長", "部活・サークルの幹事"]))

    shots = [
        {"name": "p-get", "segs": [(0, 80), (375, 470), (740, 840)], "title": "複数の項目の取得", "icon": "sp",
         "frames": [(25, 408, 1078, 468, "A"), (25, 772, 1040, 832, "B")],
         "notes": [("A", "リスト名 <b>社員名簿</b>"), ("B", "<code>MonthDay eq '</code>式<code>'</code>。式は <code>convertFromUtc(utcNow(),'Tokyo Standard Time','MM-dd')</code>")]},
        {"name": "p-teams", "segs": [(0, 80), (370, 700), (820, 910)], "title": "チャットまたはチャネルでメッセージを投稿する", "icon": "teams",
         "frames": [(25, 408, 1080, 692, "C"), (40, 825, 1060, 905, "D")],
         "notes": [("C", "投稿先 <b>チャネル</b>、チームとチャネルを選ぶ"), ("D", "本文に <b>Dept</b>（部署）と <b>Title</b>（氏名）を差し込む")]},
    ]
    page("vol-148d", "Vol.148-4", "要の設定", "要の設定は<span class=\"hl\">月日のフィルター</span>と<span class=\"hl\">投稿先</span>",
         "guts", "フィルターの値は文字列なので、式の前後を <b>' で囲み</b>ます。<br>投稿先をチャネルにすると、フロー ボットの投稿にみんなが返信でお祝いを書けます",
         settings_stage(148, "vol-148d", shots, box_h=400), next_bar("同じ形で<b>契約の更新日</b>や<b>資格の期限</b>の前日通知にも使える"))


# ════════════════ Vol.149 日本語で頼むと Copilot がフローの下書きを作る（型B：流れ3列）
def v149():
    stage = f'''    <div class="col info">
      <div class="ch2"><span class="n">1</span>やりたいことを1文で書く</div>
      <div class="win pa" style="flex:1"><div class="wh"><img src="{ICON['copilot']}" alt="">Copilot から作成する</div><div class="wb">
        <div style="border:2px solid #A5B4FC;border-radius:10px;padding:10px 12px;font-size:17px;font-weight:800;color:var(--navy);line-height:1.5;background:#F8FAFF">
          添付ファイル付きのメールが届いたら、添付ファイルを OneDrive の請求書フォルダーに保存して、Teams で自分に知らせる</div>
        <div class="why" style="font-size:15.5px">何が起きたら／何を／どこへ、を1文に入れる</div>
      </div></div>
      <div class="cap">送ると<b>10秒ほどで</b>提案が出る</div>
    </div>
    <div class="col info">
      <div class="ch2"><span class="n">2</span>Copilot が骨組みを出す</div>
      <div class="win pa" style="flex:1"><div class="wh"><img src="{ICON['copilot']}" alt="">提案されたフロー</div><div class="wb" style="gap:7px">
        <div class="mail" style="display:flex;gap:8px;align-items:center"><img src="{ICON['outlook']}" style="width:28px;height:28px" alt=""><div><div class="ms">新しいメールが届いたとき</div><div class="mf">トリガー</div></div></div>
        <div class="mail" style="display:flex;gap:8px;align-items:center"><img src="{ICON['ctrl']}" style="width:28px;height:28px" alt=""><div class="ms">Foreach</div></div>
        <div class="mail" style="display:flex;gap:8px;align-items:center;margin-left:22px"><img src="{ICON['outlook']}" style="width:28px;height:28px" alt=""><div class="ms">添付ファイルの取得</div></div>
        <div class="mail" style="border:2px dashed #F87171;background:#FEF2F2;color:#991B1B;font-size:15.5px;font-weight:900">保存と通知は入っていなかった</div>
      </div></div>
      <div class="cap">トリガーと<b>繰り返しの形</b>はできている</div>
    </div>
    <div class="col good">
      <div class="ch2"><span class="n">3</span>足りない所を人が足す</div>
      <div class="win pa" style="flex:1"><div class="wh"><img src="{ICON['pa']}" alt="">デザイナー</div><div class="wb" style="gap:7px">
        <div class="mail" style="display:flex;gap:8px;align-items:center"><img src="{ICON['outlook']}" style="width:28px;height:28px" alt=""><div class="ms">添付ファイルの取得 (V2)</div></div>
        <div class="mail new" style="display:flex;gap:8px;align-items:center;border-left-color:#16A34A;background:#ECFDF5"><img src="{ICON['od']}" style="width:28px;height:28px" alt=""><div><div class="ms">ファイルの作成</div><div class="mf">＋で追加・/請求書</div></div></div>
        <div class="mail new" style="display:flex;gap:8px;align-items:center;border-left-color:#16A34A;background:#ECFDF5"><img src="{ICON['teams']}" style="width:28px;height:28px" alt=""><div><div class="ms">メッセージを投稿する</div><div class="mf">＋で追加・自分へ</div></div></div>
      </div></div>
      <div class="cap">白紙から作るより<b>最初の一歩</b>が早い</div>
      <img class="chara" src="{A}chara/chara_laptop.png" alt="" style="position:absolute;right:-4px;bottom:44px;height:112px">
    </div>'''
    page("vol-149", "Vol.149-1", "Copilot でフローの下書き", "やりたいことを日本語で書くと、<br><span class=\"hl\">Copilot がフローの下書き</span>を作る",
         "think", "Power Automate の<b>Copilot から作成する</b>に1文で頼むと、トリガーと流れの骨組みが出てきます。<br>今回の例では、保存と通知の2つは人が足しました。どこまで作るかを実画面で見ていきます",
         stage, next_bar("頼み方は<b>2枚目</b>、実際の Copilot の画面は<b>3・4枚目</b>"), ".col.good{position:relative}")

    cols = [
        {"t": "開く場所", "ex": '<div>最初から作成する ／ テンプレートから作成する ／ <b style="color:#1D4ED8">Copilot から作成する</b></div>', "acts": [("pa", "ホーム ＞ Copilot から作成する", [("画面", "記述して作成する（ステップ 1/2）", False)], "マイ フローの上にある3つのカードの右端")],
         "cap": "作る前に<b>環境</b>が合っているか右上で確かめる"},
        {"t": "頼み方", "ex": '<div>添付ファイル付きのメールが届いたら、添付ファイルを OneDrive の請求書フォルダーに保存して、Teams で自分に知らせる</div>', "acts": [("copilot", "やりたいことを1文で書く", [("何が起きたら", "添付ファイル付きのメールが届いたら", True), ("何を", "添付ファイルを保存して", False), ("どこへ", "OneDrive の請求書フォルダー・Teams", False)], "例を選ぶ欄もある。近いものを選んで書き換えてもよい")],
         "cap": "フォルダー名や宛先も<b>文に入れておく</b>"},
        {"t": "出てきた後", "ex": '<div>接続：Office 365 Outlook ✓</div><div>足したもの：ファイルの作成／メッセージを投稿する</div>', "acts": [("pa", "保持して続行する", [("ステップ 2/2", "接続の確認", True)], "使うコネクタの接続に緑のチェックが付く"),
                                  ("pa", "フローを作成", [("足りないもの", "＋から手で追加", True), ("空の欄", "フォルダー・宛先を入れる", False)], "")],
         "cap": "提案は<b>保存前の下書き</b>。保存は自分で押す"},
    ]
    page("vol-149b", "Vol.149-2", "頼み方", "頼み方は<span class=\"hl\">何が起きたら／何を／どこへ</span>の1文",
         "laptop", "Copilot は、文に書いたことからトリガーとアクションを選びます。<br>書いていない設定値は入らないので、<b>フォルダー名や宛先も文に入れておく</b>と手直しが減ります",
         howto_cols(cols), warn_bar(["提案はそのまま正しいとは限らない。アクションと設定値を1つずつ見る", "AI が作るので、同じ文でも毎回同じ提案になるとは限らない", "保存してオンにするまでは動かない"]))

    shots3 = [
        {"name": "p-suggest", "segs": [(0, 802)], "title": "提案されたフロー", "icon": "copilot",
         "frames": [(62, 232, 1452, 322, "2"), (62, 490, 1452, 674, "3")],
         "notes": [("2", "トリガーは<b>新しいメールが届いたとき</b>"), ("3", "Foreach の中に<b>添付ファイルの取得</b>。保存と通知はここには無い")]},
        {"name": "p-prompt", "segs": [(40, 240)], "title": "記述して作成する（ステップ 1/2）", "icon": "copilot",
         "frames": [(85, 48, 1492, 228, "1")],
         "notes": [("1", "1枚目の文をそのまま入力して送る"), ("→", "提案の下の<b>保持して続行する</b>を押すと、接続の確認（ステップ 2/2）に進む"),
                   ("→", "接続は <b>Office 365 Outlook</b> だけに緑のチェック。OneDrive と Teams は出てこなかった"), ("→", "<b>フローを作成</b>でデザイナーが開き、ここから手で足す")]},
    ]
    page("vol-149c", "Vol.149-3", "Copilot の提案", "実際の Copilot の提案：<span class=\"hl\">骨組みまで</span>",
         "point", "PA45 Demo 環境で、1枚目の文をそのまま入れた結果です。<br>トリガーと繰り返しは出ましたが、<b>OneDrive への保存と Teams への通知</b>は提案に入りませんでした",
         settings_stage(149, "vol-149c", shots3, box_h=330), uses_bar("向いている人", ["フローを作ったことがない人", "どのトリガーを使うか迷う人", "社内で自動化を広める担当"]))

    shots4 = [
        {"name": "p-copilot-reply", "segs": [(0, 610)], "title": "デザイナーの Copilot に追加を頼んだ返事", "icon": "copilot",
         "frames": [(25, 178, 634, 500, "A")],
         "notes": [("A", "この環境では、OneDrive と Teams は<b>このフローで使えない</b>という返事だった（理由は未確認）")]},
        {"name": "canvas", "segs": [(0, 1010)], "title": "＋から手で2つ足した完成形", "icon": "pa",
         "frames": [(50, 560, 455, 650, "B"), (50, 740, 455, 868, "C")],
         "notes": [("B", "OneDrive <b>ファイルの作成</b>：フォルダーのパス /請求書"), ("C", "Teams で自分へ、保存したファイル名を投稿")]},
    ]
    page("vol-149d", "Vol.149-4", "足りない所を足す", "Copilot が足せないときは<span class=\"hl\">＋から手で</span>足す",
         "guts", "下書きのあと、デザイナー右上の Copilot に追加を頼むこともできます。<br>今回は断られたので、Foreach の中の<b>＋</b>から2つ足して完成させました",
         settings_stage(149, "vol-149d", shots4, box_h=318), next_bar("Copilot には<b>最初の骨組み</b>を任せ、設定値は自分で入れる、と分けると速い"))


if __name__ == "__main__":
    for f in (v145, v146, v147, v148, v149):
        f()
    print("ok")

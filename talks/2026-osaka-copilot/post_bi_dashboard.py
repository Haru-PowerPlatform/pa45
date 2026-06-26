# -*- coding: utf-8 -*-
"""なんでもCopilot大阪 登壇のBI見える化パートを解説する記事を automate136.com に下書き投稿"""
import os, requests, re

ROOT = os.path.dirname(os.path.abspath(__file__))
# .env 読み込み（pa45 リポジトリルート）
env = {}
for p in [os.path.join(ROOT, "..", "..", ".env"), os.path.join(ROOT, "..", "..", "..", ".env")]:
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
        break

WP_USER = env["WP_USER"]; WP_PASS = env["WP_PASS"]; WP_URL = env["WP_URL"].rstrip("/")

AV = "https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png"

def speech(text):
    return (
        '\n\n<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">'
        '<div class="speech-person">'
        f'<figure class="speech-icon"><img class="speech-icon-image" src="{AV}" alt="" width="1024" height="1024" /></figure>'
        '</div>'
        f'<div class="speech-balloon">{text}</div></div>'
    )

def code(text):
    t = text.strip("\n")
    return f'\n\n<pre><code>{t}</code></pre>'

def blue(t):
    return f'<span style="color: #0000ff;"><strong>{t}</strong></span>'

SP = "\n\n&nbsp;"

content = ""

# ── 導入 ──
content += "\n\n<p>先日、「なんでもCopilot 大阪」というイベントで、社内DXの話を10分ほどさせてもらいました。テーマは「学びを、成果に変える」。</p>"
content += "\n\n<p>その中で、いちばん反応が大きかったのが「<strong>講座で配ったフローの成果を、全自動で見える化する</strong>」という部分でした。登壇では仕組みのさわりしか話せなかったので、この記事で、実際の作り方を最初から最後まで丁寧に書いてみます。</p>"
content += "\n\n<p>使うのは Power Automate と Power BI、それと SharePoint リストだけ。特別なものは何も要りません。</p>"

content += speech("講座をやっても「で、結局どれくらい役に立ったの？」が見えないと、続ける理由を見失いがちなんですよね。そこを数字にしたかったんです。")

# ── なぜ見える化か ──
content += "\n\n<h2>そもそも、なぜ「見える化」だったのか</h2>"
content += "\n\n<p>社内でPower Automateの講座を続けていて、ずっと引っかかっていたことがあります。それは「<strong>教えて終わり</strong>」になってしまうことです。</p>"
content += "\n\n<p>講座は開く。フローも配る。みんな「便利だね」と言ってくれる。でも、それが<strong>会社の成果につながっているのか</strong>が、誰にも分からない。頑張りが数字にならないと、やっている本人も、見ている上司も、実感が持てません。</p>"
content += "\n\n<p>そこで考えたのが、「使われた回数」と「削減できた時間」を勝手に記録して、ダッシュボードで見えるようにする、というものでした。ポイントは<strong>「全自動」</strong>。集計のために誰かが毎月Excelを開く、みたいな運用だと、絶対に続かないからです。</p>"
content += SP

# ── 全体像 ──
content += "\n\n<h2>全体像 ── 3つのステップ</h2>"
content += "\n\n<p>仕組みはシンプルで、大きく3ステップです。</p>"
content += ("\n\n<ul>"
           "\n<li><strong>STEP 1</strong>：配布するフロー全部に「実行ログを記録する処理」を仕込む</li>"
           "\n<li><strong>STEP 2</strong>：誰かが使うたびに、SharePointリストへ自動で1行たまっていく</li>"
           "\n<li><strong>STEP 3</strong>：そのリストをPower BIにつないでダッシュボード化し、毎朝・無人で自動更新する</li>"
           "\n</ul>")
content += "\n\n<p>データの流れにすると、こうなります。</p>"
content += code(
"配布フロー（各自が使う）\n"
"   ↓ 使うたびに1行記録\n"
"SharePoint リスト（成果データの貯金箱）\n"
"   ↓ 毎朝 自動で読み込み\n"
"Power BI ダッシュボード（KPI・グラフ）"
)
content += speech("人が触るのは最初の「仕込み」だけ。あとは使えば使うほど、勝手にデータがたまっていく設計にするのがコツです。")
content += SP

# ── STEP1 ──
content += "\n\n<h2>STEP 1：配布フローに「実行ログ」を仕込む</h2>"
content += "\n\n<p>まずは、成果データをためる場所を用意します。今回は手軽な<strong>SharePointリスト</strong>を使いました。Dataverseでも考え方は同じです。</p>"

content += "\n\n<h3>① 記録用のSharePointリストを作る</h3>"
content += "\n\n<p>リストに、次のような列を作っておきます。これが、あとでグラフの材料になります。</p>"
content += ("\n\n<ul>"
           "\n<li><strong>タイトル</strong>（フロー名）── 既定の列をそのまま使う</li>"
           "\n<li><strong>実行日時</strong>（日付と時刻）</li>"
           "\n<li><strong>実行者</strong>（1行テキスト）</li>"
           "\n<li><strong>部署</strong>（1行テキスト ／ または選択肢）</li>"
           "\n<li><strong>削減時間_分</strong>（数値）</li>"
           "\n</ul>")
content += "\n\n<p>「削減コスト（円）」の列は<strong>あえて作りません</strong>。コストは時給単価×時間で後から計算できるので、Power BI側で出したほうが、単価を変えたいときに柔軟だからです（理由は後述します）。</p>"

content += "\n\n<h3>② フローの最後に「項目の作成」を1つ足す</h3>"
content += "\n\n<p>あとは、配布する各フローの<strong>いちばん最後</strong>に、SharePointの「項目の作成」アクションを1つ追加するだけです。本来やりたい処理（メール送信や転記など）が終わったあとに、こっそりログを残すイメージです。</p>"
content += "\n\n<p>各項目には、次の値を入れていきます。</p>"

content += "\n\n<p>" + blue("実行日時") + "（UTCのままだと9時間ズレるので、必ず日本時間に直します）</p>"
content += code("convertTimeZone(utcNow(), 'UTC', 'Tokyo Standard Time', 'yyyy/MM/dd HH:mm')")

content += "\n\n<p>" + blue("実行者・部署") + "（「Office 365 ユーザー」コネクタの<strong>「マイ プロフィールの取得 (V2)」</strong>を、項目の作成より前に置いておきます）</p>"
content += code(
"実行者 → 表示名（DisplayName）\n"
"部署   → 部署（Department）"
)
content += "\n\n<p>このアクションは「<strong>そのフローを動かした本人</strong>」のプロフィールを返してくれます。配布フローは各自が自分の環境に取り込んで使うので、自然と「誰が・どの部署で使ったか」が記録されます。ここが地味に効くポイントです。</p>"

content += "\n\n<p>" + blue("削減時間_分") + "（そのフローで何分浮くかの見積もり）</p>"
content += "\n\n<p>これは正確さより<strong>運用しやすさ</strong>を優先して、フローごとに固定値で置きました。たとえば「お礼メール自動化フロー」なら1回あたり5分、といった具合です。数値アクションでも、項目の作成に直接 <code>5</code> と書いてもOKです。</p>"

content += speech("最初から完璧な削減時間を出そうとすると沼にハマります。まずは『ざっくり1回◯分』で動かして、あとから調整するくらいがちょうどいいです。")

content += "\n\n<p>これで仕込みは完了です。配布フローを使うたびに、SharePointリストへ「いつ・誰が・どの部署で・どのフローを・何分ぶん」が1行ずつ自動でたまっていきます。</p>"
content += SP

# ── STEP2 コスト換算 ──
content += "\n\n<h2>STEP 2：削減時間を「コスト」に翻訳する</h2>"
content += "\n\n<p>経営目線で見てもらうには、「時間」より「<strong>お金</strong>」のほうが圧倒的に伝わります。そこで、たまった削減時間を金額に換算します。考え方はとても単純です。</p>"
content += code(
"削減コスト（円）＝ 削減時間（時間）× 時給単価\n"
"\n"
"例：削減時間 200時間 × 時給 3,000円 ＝ 600,000円"
)
content += "\n\n<p>この計算を<strong>SharePoint側ではなくPower BI側でやる</strong>のがおすすめです。時給単価は「いくらで見積もるか」で結果が変わる数字なので、データに焼き付けず、ダッシュボード側のパラメータにしておくと、あとで「単価を変えたら？」をその場で試せます。</p>"
content += SP

# ── STEP3 Power BI ──
content += "\n\n<h2>STEP 3：Power BIでダッシュボードにする</h2>"
content += "\n\n<p>いよいよ見える化です。Power BI Desktop を開いて進めます。</p>"

content += "\n\n<h3>① SharePointリストに接続する</h3>"
content += ("\n\n<ol>"
           "\n<li>「データを取得」→「<strong>SharePoint Online リスト</strong>」を選ぶ</li>"
           "\n<li>サイトのURLを貼り付ける（リスト名までではなく、サイトのトップURL）</li>"
           "\n<li>表示されたリストの中から、作った記録用リストにチェックを入れて「読み込み」</li>"
           "\n</ol>")
content += "\n\n<p>このとき「2.0」と表示されるほうの実装を選ぶと、列名がきれいに取れて扱いやすいです。</p>"

content += "\n\n<h3>② Power Queryで軽く整える</h3>"
content += "\n\n<p>読み込んだら、エディターで以下くらいを整えます。やりすぎず、最低限でOKです。</p>"
content += ("\n\n<ul>"
           "\n<li>使う列だけ残す（実行日時・実行者・部署・フロー名・削減時間_分）</li>"
           "\n<li><strong>実行日時を「日付/時刻」型</strong>に、<strong>削減時間_分を「整数」型</strong>に変換</li>"
           "\n<li>部署の表記ゆれ（全角スペースなど）があれば、ここでそろえる</li>"
           "\n</ul>")

content += "\n\n<h3>③ DAXメジャーで「数字」を作る</h3>"
content += "\n\n<p>KPIカードに出す数字を、メジャーとして3つ作ります。リスト名を <code>実行ログ</code> とした場合の例です。</p>"
content += code(
"総実行回数 = COUNTROWS('実行ログ')\n"
"\n"
"総削減時間（時間） = DIVIDE( SUM('実行ログ'[削減時間_分]), 60 )\n"
"\n"
"時給単価 = 3000\n"
"\n"
"総削減コスト（円） = ROUND( [総削減時間（時間）] * [時給単価], 0 )"
)
content += "\n\n<p><code>DIVIDE</code> を使うのは、データがまだ0件のときに「0で割るエラー」を出さないためのちょっとした保険です。<code>時給単価</code> は、本格的に運用するなら「What-if パラメータ」にすると、スライダーで単価を動かしながら金額の変化を見せられます。</p>"

content += speech("メジャーは『計算の部品』です。一度作っておけば、カードにもグラフにも使い回せるので、まずこの3つを作るのが近道です。")

content += "\n\n<h3>④ ビジュアルを並べる</h3>"
content += "\n\n<p>登壇で見せたダッシュボードは、こんな構成にしました。</p>"
content += ("\n\n<ul>"
           "\n<li><strong>カード × 4</strong>：総実行回数 ／ 総削減時間 ／ 総削減コスト ／ 参加者数（KPIをドンと上段に）</li>"
           "\n<li><strong>折れ線＋集合縦棒の複合グラフ</strong>：月別の削減コストと業務削減コストの推移（軸＝実行日時の「月」）</li>"
           "\n<li><strong>横棒グラフ</strong>：部署（Gr・係）別の実行回数（どこで一番使われているかが一目で分かる）</li>"
           "\n</ul>")
content += "\n\n<p>「どこの部署が使っているか」が横棒で見えると、社内で『あの部署すごいね』という会話が生まれて、これが地味に推進力になりました。</p>"
content += SP

# ── 自動更新 ──
content += "\n\n<h2>仕上げ：毎朝・無人で自動更新する</h2>"
content += "\n\n<p>最後に、いちばん大事な「全自動」の部分です。手で更新ボタンを押す運用だと、結局見なくなります。Power BI サービスのスケジュール更新を設定します。</p>"
content += ("\n\n<ol>"
           "\n<li>Power BI Desktop から「<strong>発行</strong>」で、Power BI サービス（クラウド）にレポートを上げる</li>"
           "\n<li>サービス側で、対象の<strong>セマンティックモデル（データセット）→「設定」→「スケジュールされた更新」</strong>を開く</li>"
           "\n<li>更新をオンにして、時刻を毎朝（例：午前7時）に設定する</li>"
           "\n</ol>")
content += "\n\n<p>データ元がSharePoint Onlineのようなクラウドサービスなら、<strong>オンプレミスデータゲートウェイは不要</strong>です。ここがクラウド完結で組むメリットで、設定がぐっと楽になります。</p>"
content += speech("これで、夜のうちにデータが集計されて、朝出社したら最新のダッシュボードが待っている状態になります。誰も何もしなくていい、というのが続けるコツです。")
content += SP

# ── なぜ効くか ──
content += "\n\n<h2>見える化が「やる気」に変わる理由</h2>"
content += "\n\n<p>仕組みの話はここまでですが、最後に、いちばん伝えたかったことを。</p>"
content += "\n\n<p>このダッシュボードを社内に出してから、空気が少し変わりました。「<strong>自分の自動化が、これだけ会社に貢献している</strong>」が数字で見えると、それ自体が楽しさややる気につながるんです。</p>"
content += "\n\n<p>効率化はゴールではなくて、本当はその先 ──「浮いた時間を、自分が本当にやりたい仕事に使う」ことが目的だと思っています。成果が見えるから、人は続けたくなる。続くから、現場が少しずつ前に進む。見える化は、その入口だと感じています。</p>"
content += SP

# ── まとめ ──
content += "\n\n<h2>まとめ</h2>"
content += ("\n\n<ul>"
           "\n<li>配布フローの最後に「項目の作成」を1つ足すだけで、成果ログが自動でたまる</li>"
           "\n<li>実行者・部署は「マイ プロフィールの取得 (V2)」で自動取得、日時は<code>convertTimeZone</code>でJSTに</li>"
           "\n<li>コスト換算（時給×時間）はPower BI側のメジャーにしておくと柔軟</li>"
           "\n<li>SharePoint Onlineならゲートウェイ不要。スケジュール更新で毎朝・無人で最新化</li>"
           "\n</ul>")
content += "\n\n<p>難しい技術は1つも使っていません。「使うたびに1行たまる」という小さな仕掛けを、配るフロー全部に仕込んでおく ── それだけで、講座の成果がちゃんと積み上がって見えるようになります。</p>"
content += "\n\n<p>もし社内で同じ悩みを持っている方がいたら、ぜひ試してみてください。</p>"

title = "社内講座の成果を“全自動”で見える化する｜Power Automate × Power BI ダッシュボードの作り方"

payload = {
    "title": title,
    "content": content,
    "status": "draft",
    "categories": [76, 78],
}

r = requests.post(
    f"{WP_URL}/wp-json/wp/v2/posts",
    auth=(WP_USER, WP_PASS),
    json=payload,
    timeout=60,
)
print("STATUS", r.status_code)
data = r.json()
print("POST ID:", data.get("id"))
print("EDIT:", f"{WP_URL}/wp-admin/post.php?post={data.get('id')}&action=edit")
print("PREVIEW:", data.get("link"))

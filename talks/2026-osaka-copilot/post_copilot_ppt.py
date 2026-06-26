# -*- coding: utf-8 -*-
"""CopilotでPPT資料を早くキレイに作る手順 を automate136.com に下書き投稿"""
import os, requests

ROOT = os.path.dirname(os.path.abspath(__file__))
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
    return ('\n\n<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">'
            '<div class="speech-person">'
            f'<figure class="speech-icon"><img class="speech-icon-image" src="{AV}" alt="" width="1024" height="1024" /></figure>'
            '</div>'
            f'<div class="speech-balloon">{text}</div></div>')

def code(text):
    return f'\n\n<pre><code>{text.strip(chr(10))}</code></pre>'

def blue(t):
    return f'<span style="color: #0000ff;"><strong>{t}</strong></span>'

SP = "\n\n&nbsp;"
c = ""

# ── 導入 ──
c += "\n\n<p>プレゼン資料づくり、けっこう時間がかかりますよね。構成を考えて、文字を打ち込んで、配置を整えて……気づいたら半日が溶けている、みたいなこと、私もよくありました。</p>"
c += "\n\n<p>最近は Copilot を使って、資料を「早く」「そこそこキレイに」作る手順が自分の中で固まってきたので、整理してみます。コツは、いきなりPowerPointで作らせないことです。</p>"
c += speech("一番のポイントは、<strong>まずHTMLで“見た目つきの下書き”を作って、それを見ながら直していく</strong>こと。これだけで体感のスピードがかなり変わりました。")

# ── 全体の流れ ──
c += "\n\n<h2>全体の流れは3ステップ</h2>"
c += ("\n\n<ul>"
      "\n<li><strong>STEP 1</strong>：Copilotを「<strong>Think Deeper</strong>」モードに切り替える</li>"
      "\n<li><strong>STEP 2</strong>：スライドを<strong>HTMLで出力</strong>させる（ブラウザでそのまま見られる形）</li>"
      "\n<li><strong>STEP 3</strong>：そのHTMLを見ながら、<strong>気になる所を指示して直していく</strong></li>"
      "\n</ul>")
c += "\n\n<p>仕上がったら、最後にPowerPointへ落とすか、HTMLのまま投影します。順番に見ていきます。</p>"
c += SP

# ── なぜHTML ──
c += "\n\n<h2>なぜ「HTML出力」が効くのか</h2>"
c += "\n\n<p>Copilotにいきなり「PowerPointを作って」と頼むと、中身は出てくるものの、<strong>レイアウトが見えない</strong>ので、結局自分で開いて直すことになります。これが地味に時間を食います。</p>"
c += "\n\n<p>そこで、まずHTMLで出してもらいます。HTMLならブラウザで開くだけで<strong>「実際の見た目」</strong>がすぐ分かるので、「ここの文字が多い」「グラフが大きすぎる」といった修正を、目で見ながらサッと指示できます。文章だけのやり取りより、圧倒的に速いんです。</p>"
c += speech("HTMLは“紙芝居のラフ”みたいなもの。完成版をいきなり作るより、ラフを見ながら直すほうが早い、という感覚です。")
c += SP

# ── STEP1 ──
c += "\n\n<h2>STEP 1：Copilotを「Think Deeper」モードにする</h2>"
c += "\n\n<p>Copilotの入力欄のそばに、モードを選ぶボタンがあります。ここを<strong>「Think Deeper」</strong>に切り替えます。じっくり深く考えてくれるモードで、回答までは少し時間がかかりますが、そのぶん<strong>構成の質が上がります</strong>。</p>"
c += "\n\n<p>資料づくりは「何をどの順番で見せるか」という構成がいちばん大事なので、ここはケチらず、深く考えるモードに任せるのがおすすめです。普通のモードだと、それっぽいけど浅い構成になりがちでした。</p>"
c += speech("普段のサクッとした質問は通常モードでいいですが、<strong>“考えてほしい”ものはThink Deeper</strong>、と使い分けています。")
c += SP

# ── STEP2 ──
c += "\n\n<h2>STEP 2：HTMLでスライドを出力させる</h2>"
c += "\n\n<p>最初の指示で、テーマと条件を伝えて、HTMLで出してもらいます。私がよく使うプロンプトの形はこんな感じです。</p>"
c += code(
"あなたはプレゼン資料のデザイナーです。\n"
"次のテーマで、スライド5枚分の構成を作ってください。\n"
"\n"
"出力は、ブラウザでそのまま見られる「1つのHTMLファイル」にまとめてください。\n"
"・1枚のスライド = 1つのセクション\n"
"・画面比率は16:9\n"
"・各スライドに「見出し」と「要点3つ」を入れる\n"
"・配色は青系で統一、文字は大きめ\n"
"\n"
"# テーマ\n"
"（ここに、伝えたいこと・聞き手・ゴールを書く）"
)
c += "\n\n<p>ポイントは、<strong>「テーマ」だけでなく「誰に・何のために」も一緒に書く</strong>こと。聞き手とゴールを伝えると、構成の精度がぐっと上がります。</p>"
c += "\n\n<p>出てきたHTMLは、コードをコピーして拡張子 <code>.html</code> で保存し、ダブルクリックでブラウザで開けば、スライドの見た目が確認できます。</p>"
c += SP

# ── STEP3 ──
c += "\n\n<h2>STEP 3：HTMLを見ながら指示して仕上げる</h2>"
c += "\n\n<p>ここからが本番です。ブラウザでスライドを見ながら、気になった所を<strong>そのまま言葉で</strong>直していきます。難しい操作はいりません。</p>"
c += "\n\n<p>たとえば、こんな感じで指示します。</p>"
c += code(
"・2枚目、文字が多いので要点を3つに絞って\n"
"・3枚目のグラフを半分の大きさにして、右に寄せて\n"
"・全体のフォントをもう少し大きく\n"
"・タイトルスライドに、サブタイトルを1行足して\n"
"・配色を、青からもう少し落ち着いた紺系に変えて"
)
c += "\n\n<p>1回の指示で全部直そうとせず、<strong>2〜3個ずつ、見ては直す</strong>を繰り返すのがコツです。少しずつ詰めていくと、崩れにくく、納得のいく形に近づきます。</p>"
c += speech("「ここがイマイチ」を口で言うだけで直っていくので、PowerPointと格闘していた時間が、ほぼ無くなりました。")
c += SP

# ── STEP4 ──
c += "\n\n<h2>仕上げ：PowerPointに落とす or そのまま投影</h2>"
c += "\n\n<p>HTMLで形が決まったら、最後の仕上げです。やり方は2つあります。</p>"
c += ("\n\n<ul>"
      "\n<li><strong>そのまま投影する</strong>：HTMLは全画面表示すれば、そのままプレゼンに使えます。手間ゼロで一番ラク。</li>"
      "\n<li><strong>PowerPointに変換する</strong>：会社の様式に合わせる必要があるときは、「この構成でPowerPointの各スライドの文章を書き出して」と頼み、中身をPPTに流し込みます。</li>"
      "\n</ul>")
c += "\n\n<p>私は、社内の決まった様式が必要なときだけPPTに移して、それ以外はHTMLのまま使うことが多いです。</p>"
c += SP

# ── コツ ──
c += "\n\n<h2>うまく作るための小さなコツ</h2>"
c += ("\n\n<ul>"
      "\n<li><strong>最初に枚数を決める</strong>（「5枚で」と言うと、間延びしない）</li>"
      "\n<li><strong>聞き手とゴールを必ず伝える</strong>（構成の質が変わる)</li>".replace("変わる)","変わる）") +
      "\n<li><strong>直しは少しずつ</strong>（一度に詰め込むと崩れる）</li>"
      "\n<li><strong>図やグラフは“placeholder（枠）”で先に置いてもらう</strong>（あとで自分の画像に差し替え）</li>"
      "\n</ul>")
c += SP

# ── まとめ ──
c += "\n\n<h2>まとめ</h2>"
c += "\n\n<p>あらためて、手順はこれだけです。</p>"
c += ("\n\n<ul>"
      "\n<li>Copilotを<strong>Think Deeper</strong>に切り替える</li>"
      "\n<li>テーマ＋聞き手＋ゴールを伝えて<strong>HTMLで出力</strong>させる</li>"
      "\n<li>ブラウザで見ながら、<strong>少しずつ指示して仕上げる</strong></li>"
      "\n<li>そのまま投影、または<strong>PowerPointに変換</strong></li>"
      "\n</ul>")
c += "\n\n<p>「いきなり完成版を作らせない」「見た目を見ながら直す」。この2つだけで、資料づくりはずいぶん楽になりました。よかったら試してみてください。</p>"

title = "Copilotで“早くキレイに”PowerPoint資料を作る手順｜Think Deeper × HTML出力のすすめ"

payload = {"title": title, "content": c, "status": "draft", "categories": [76]}
r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", auth=(WP_USER, WP_PASS), json=payload, timeout=60)
print("STATUS", r.status_code)
d = r.json()
print("POST ID:", d.get("id"))
print("EDIT:", f"{WP_URL}/wp-admin/post.php?post={d.get('id')}&action=edit")
print("PREVIEW:", d.get("link"))

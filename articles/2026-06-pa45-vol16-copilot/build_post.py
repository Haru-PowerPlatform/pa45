# -*- coding: utf-8 -*-
"""PA45 第16回 レポート記事を WordPress 下書きとして作成（画像アップロード込み）。
お手本: articles/2026-06-dekiru-pad-copilot-review の文体・CSS を踏襲。
"""
import os, re, json, mimetypes, requests
from requests.auth import HTTPBasicAuth

ROOT = r"C:\Users\isamu\Documents\pa45"
PNG  = os.path.join(ROOT, "slides", "vol-16", "png")

env = {}
for line in open(os.path.join(ROOT, ".env"), encoding="utf-8", errors="ignore"):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

WP   = env["WP_URL"].rstrip("/")
AUTH = HTTPBasicAuth(env["WP_USER"], env["WP_PASS"])
SLUG = "pa45-vol16-copilot"
AVATAR = "https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png"

# ---------- 画像アップロード ----------
def upload(fname, title):
    path = os.path.join(PNG, fname)
    data = open(path, "rb").read()
    ct = mimetypes.guess_type(path)[0] or "image/png"
    r = requests.post(f"{WP}/wp-json/wp/v2/media",
        auth=AUTH,
        headers={"Content-Disposition": f'attachment; filename="{fname}"',
                 "Content-Type": ct},
        data=data, timeout=120)
    r.raise_for_status()
    j = r.json()
    # alt/caption/title を設定
    requests.post(f"{WP}/wp-json/wp/v2/media/{j['id']}", auth=AUTH,
                  json={"title": title, "alt_text": title}, timeout=60)
    print(f"  uploaded {fname} -> id={j['id']}")
    return j["id"], j["source_url"]

# 記事に使うスライド
NEED = {
    "s05": "PA45 第16回 タイトル｜Copilotと作るPower Automate",
    "s07": "今日作る1本のフロー（Forms→日付を整形→メール通知）",
    "s06": "Copilotをうまく使うコツ：フローの中身を正確に把握してもらう",
    "s08": "STEP1 まず動かして出力を出す",
    "s09": "STEP2 出力JSONを先にCopilotへ見せる",
    "s10": "STEP3 式をCopilotに書かせる（convertTimeZone）",
    "s11": "STEP4 完成フローのJSONを読ませる",
    "s12": "うまく頼む3つのコツ",
    "s13": "フロー全体をCopilotに渡す（ソリューションのJSON）",
    "s14": "新しいソリューションの入力欄",
    "s15": "エクスポートからJSON取り出しまでの流れ",
    "s16": "Copilotを使うときの注意",
}

print("画像アップロード中...")
img = {}
for key, title in NEED.items():
    img[key] = upload(f"vol16-{key}.png", title)

ids = {k: v[0] for k, v in img.items()}
url = {k: v[1] for k, v in img.items()}

# ---------- HTML パーツ ----------
def figure(key, cap):
    return (f'\n\n<figure class="v16-fig">'
            f'<img src="{url[key]}" alt="{NEED[key]}" />'
            f'<figcaption>▲ {cap}</figcaption></figure>')

def balloon(text):
    return ('\n\n<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">'
            '<div class="speech-person"><figure class="speech-icon">'
            f'<img class="speech-icon-image" src="{AVATAR}" alt="" width="1024" height="1024" /></figure></div>'
            f'<div class="speech-balloon">{text}</div></div>')

STYLE = """
<style>
.hl-marker{background:linear-gradient(transparent 58%,#fff176 58%);font-weight:700;padding:0 .12em;border-radius:2px;}
.v16-fig{margin:26px 0;text-align:center;}
.v16-fig img{width:100%;max-width:820px;height:auto;border:1px solid #e2e8f0;border-radius:12px;box-shadow:0 6px 22px rgba(20,82,143,.12);}
.v16-fig figcaption{font-size:.86em;color:#7c8694;margin-top:8px;}
.v16-step{background:#f6faff;border:2px solid #cfe0f3;border-radius:14px;padding:18px 22px 6px;margin:24px 0;}
.v16-step .st-ttl{display:flex;align-items:center;gap:12px;font-weight:800;color:#14528f;font-size:1.08em;margin-bottom:6px;}
.v16-step .st-no{flex:none;width:34px;height:34px;border-radius:50%;background:#2a7dd4;color:#fff;display:flex;align-items:center;justify-content:center;font-size:1em;}
.v16-point{background:#f6faff;border-left:6px solid #4a90d9;border-radius:8px;padding:16px 22px;margin:24px 0;line-height:2.0;}
.v16-note{background:#fffdf5;border:2px solid #ffd54f;border-radius:12px;padding:16px 22px;margin:26px 0;line-height:2.0;}
.v16-note .nt-ttl{font-weight:700;color:#e8920c;margin:0 0 6px;}
.v16-warn{background:#fff6f6;border-left:6px solid #e57373;border-radius:8px;padding:16px 22px;margin:24px 0;line-height:2.0;}
.v16-code{background:#0f172a;color:#e2e8f0;font-family:Consolas,'DM Mono',monospace;font-size:.92em;line-height:1.6;padding:14px 18px;border-radius:10px;margin:14px 0;overflow-x:auto;white-space:pre-wrap;word-break:break-all;}
</style>
"""

P  = lambda t: f"\n\n<p>{t}</p>"
H2 = lambda t: f"\n\n<h2>{t}</h2>"
SP = "\n\n&nbsp;"

def step(no, title, body):
    return (f'\n\n<div class="v16-step"><div class="st-ttl"><span class="st-no">{no}</span>{title}</div>{body}</div>')

# ---------- 本文 ----------
html = STYLE

html += P('PA45（Power Automate を45分でひとつ作るハンズオン）の第16回をやりました。テーマは「<strong>Copilotと作る Power Automate</strong>」です。')
html += P('式やJSONって、フロー作りでいちばん手が止まりやすいところですよね。そこを<span class="hl-marker">AI（Copilot）に手伝ってもらって、止まらずに進む</span>。今回はそのやり方を、フローを1本作りながら一緒に試しました。')
html += P('この記事は、当日参加できなかった方でも同じ手順をたどれるように、スライドを交えて整理しておきます。お手元で読みながら、ぜひ一緒に作ってみてください。')
html += SP

html += H2('今日作るのは、こんな1本のフロー')
html += P('まず、ゴールの形を見ておきます。作るのは「<strong>Formsに回答が届いたら → 受付日を日本語の日付に整えて → 自分にメールで通知する</strong>」という流れのフローです。')
html += figure("s07", "今日のゴール。まん中の「日付を整形」を式でやり、その式をCopilotに書いてもらいます")
html += P('ポイントはまん中の「日付を整形」のところ。フローに流れてくる日付は <code>2026-06-25T11:30:00Z</code> みたいな、ちょっと無機質な形をしています。これを <code>2026年6月25日</code> に直すのが「式」の仕事です。ここを今回 Copilot に書いてもらいます。')
html += SP

html += H2('今日いちばん伝えたかったこと')
html += P('手順の前に、私がCopilotをPower Automateで使うときに、いちばん大事にしている考え方を先に置いておきます。')
html += figure("s06", "コツはひとつ。フローの“中身”をCopilotに正確に把握してもらうこと")
html += P('それは、<span class="hl-marker">フローの「中身」をCopilotに正確に把握してもらう</span>、ということです。')
html += P('Copilotは賢いのですが、こちらが何も渡さずに「日付の式を書いて」とだけ頼むと、フローの中の項目名を知らないので、当て推量で書いてきます。結果、惜しいけど合っていない式が返ってくる。これがいちばんありがちなつまずきなんですよね。')
html += P('逆に、実物のデータ（出力JSON）を<strong>先に見せてから</strong>頼むと、項目名まで合った式が一発で返ってきます。今日の4ステップは、ぜんぶこの考え方でできています。')
html += balloon('「いきなり頼まない。まず材料を見せる」。今日はこれだけ覚えて帰ってもらえたら十分です😊')
html += SP

html += H2('STEP1：まず動かして「出力」を出す')
html += P('最初にやるのは、Copilotに渡す<strong>材料を用意する</strong>ことです。ここではまだCopilotは開きません。')
html += figure("s08", "STEP1。トリガーを置いて1回だけテスト実行し、実行履歴から「出力」をコピーします")
html += step("1", "トリガーを置く",
    P('Power Automate で新しいクラウドフローを作り、トリガーに <strong>Microsoft Forms「新しい応答が送信されるとき」</strong> を置きます。フローの名前は <code>PA45-No16-CopilotAssist</code> としました。'))
html += step("2", "テストで1回だけ回答する",
    P('フローを保存してテスト実行し、対象のFormsに自分で1回だけ回答します。これで「本物のデータ」がフローを通ります。'))
html += step("3", "実行履歴から「出力」をコピーする",
    P('実行履歴を開いてトリガーの<strong>「出力」</strong>を表示し、そこに出ているJSONをコピーします。これが次でCopilotに見せる材料です。'))
html += '\n\n<div class="v16-warn"><strong>⚠️ ここでのコツ：</strong> 本物のデータがあるほど、Copilotの答えは正確になります。架空の値で済ませず、一度ちゃんと動かして「本物の出力」を取っておくのが第一歩です。</div>'
html += SP

html += H2('STEP2：出力JSONを“先に”Copilotへ見せる ── ここが肝')
html += P('材料がそろったら、いよいよCopilotに相談します。ただし、<strong>いきなり式を頼まない</strong>のがコツ。まず、さっきコピーした出力JSONを「これ覚えておいてね」と<strong>先に見せる</strong>だけにします。')
html += figure("s09", "STEP2。先に出力JSONを見せておくと、項目名（submitDateなど）をCopilotが正確に把握してくれます")
html += P('たったこれだけで、Copilotは <code>responder</code>（回答者）や <code>submitDate</code>（送信日時）といった<strong>実際の項目名</strong>を把握します。見せないと当て推量で項目名を外しますが、先に見せると実物に合わせてくれる。同じ質問でも、ここで答えの精度が大きく変わります。')
html += balloon('「まず、トリガーの出力JSONを見せるね。覚えておいて👇」── このひと手間が、あとで効いてきます。')
html += SP

html += H2('STEP3：式をCopilotに書かせる')
html += P('下ごしらえができたので、ここで初めて式を頼みます。むずかしい関数の書き方を覚える必要はありません。<strong>ことばで頼むだけ</strong>です。')
html += figure("s10", "STEP3。「どれを・どうしたい・どんな形で欲しいか」を伝えると、項目名まで合った式が返ってきます")
html += P('頼むときは、次の3つをそろえると、ほしい答えがまっすぐ返ってきます。')
html += "\n\n<ul>\n<li><strong>どれを</strong>：さっきの <code>submitDate</code> を</li>\n<li><strong>どうしたい</strong>：「2026年6月25日」の形にしたい</li>\n<li><strong>どんな形で</strong>：<strong>式だけ</strong>教えて</li>\n</ul>"
html += P('すると、こんな式が返ってきます。これをメール本文の「式」タブに貼るだけで完成です。')
html += '\n\n<div class="v16-code">convertTimeZone(triggerOutputs()?[\'body/submitDate\'],\'UTC\',\'Tokyo Standard Time\',\'yyyy年M月d日\')</div>'
html += '\n\n<div class="v16-point"><span class="hl-marker">STEP2で先に見せておいたから、項目名まで合った式が返ってくる</span>。覚えるのではなく、<strong>正しく頼んで貼る</strong>。これだけで日付の整形は済みます。</div>'
html += SP

html += H2('STEP4：完成フローのJSONを読ませる')
html += P('フローができたら、最後にもうひとつCopilotの使い道があります。<strong>完成したフローのJSONを貼って「これ、何してる？」と聞く</strong>使い方です。')
html += figure("s11", "STEP4。完成フローのJSONを貼って「3行で教えて」と頼むと、中身を要約してくれます")
html += P('「3行で教えて」と添えると、たとえばこんなふうに返してくれます。')
html += "\n\n<ul>\n<li>① Formsの回答を受け取り</li>\n<li>② 日付を日本時間に整え</li>\n<li>③ メールで送っています</li>\n</ul>"
html += P('これは、あとから自分が見返すときのメモにもなりますし、誰かにフローを引き継ぐときの説明にもそのまま使えます。JSONは「見せる（=答えが正確になる）」「読ませる（=理解できる）」の2回、活躍してくれるんですね。')
html += SP

html += H2('うまく頼む、3つのコツ')
html += P('ここまでの流れを、持ち帰れる形にまとめておきます。Copilotにうまく頼むコツは、この3つです。')
html += figure("s12", "うまく頼む3つのコツ。これだけ覚えて帰れば十分です")
html += "\n\n<ul>\n<li><strong>① 材料を“先に”見せる</strong>：いきなり頼まず、データをまず見せる（今日の核）</li>\n<li><strong>② 形を指定する</strong>：「式だけ」「3行で」など、ほしい形を先に言う</li>\n<li><strong>③ 役割を与える</strong>：「初心者向けに」と一言そえると、やさしく答えてくれる</li>\n</ul>"
html += '\n\n<div class="v16-note"><p class="nt-ttl">📋 そのまま使えるテンプレ</p>「初心者です。まず材料を見せます〔JSONを貼る〕。これを〔やりたいこと〕。<strong>式だけ教えて。</strong>」</div>'
html += SP

html += H2('もう一歩：フロー“全体”をCopilotに渡したいとき')
html += P('ここからは応用です。STEP2では出力JSONの一部を見せましたが、「フロー全体を相談したい」「改修やエラーの相談をしたい」ときは、<strong>フロー全体のJSON</strong>を渡すのがおすすめです。一部だけだとCopilotが推測で補ってズレることがあるので、全体を渡すと相談がぐっと的確になります。')
html += figure("s13", "フロー全体を渡す流れは4ステップ。ソリューションにしてエクスポートし、中のJSONを取り出します")
html += P('全体JSONは「ソリューション」という入れ物に入れてエクスポートすると取り出せます。流れはこの4つです。')
html += "\n\n<ul>\n<li>① フローを<strong>ソリューションに入れる</strong>（公開元は <strong>PA45</strong>）</li>\n<li>② ソリューションを<strong>エクスポート → アンマネージド</strong>でZipダウンロード</li>\n<li>③ Zipを解凍して、中の<strong>フロー定義のJSONファイル</strong>を取り出す</li>\n<li>④ そのJSONをCopilotに貼って相談する</li>\n</ul>"
html += P('まず①の「新しいソリューション」を作るところは、入力欄が4つあります。次のように埋めればOKです。')
html += figure("s14", "「新しいソリューション」の入力。表示名・名前・公開元・バージョンの4つを埋めるだけ")
html += "\n\n<ul>\n<li><strong>表示名</strong>：<code>PA45 No.16 CopilotAssist</code></li>\n<li><strong>名前</strong>：表示名を入れると自動で入ります（半角英数）</li>\n<li><strong>公開元</strong>：<strong>PA45</strong> を選ぶ（無ければ「＋新しい公開元」で作成）</li>\n<li><strong>バージョン</strong>：<code>1.0.0.0</code> のままでOK</li>\n</ul>"
html += P('作成できたら「既存を追加」でさっきのフローを入れて、エクスポートに進みます。エクスポートからJSONを取り出すまでは、押す順番にちょっとクセがあるので、ここも図にしておきます。')
html += figure("s15", "エクスポートからJSON取り出しまで。エクスポートは“一覧で行を選ぶ”と出てきます")
html += P('とくに引っかかりやすいのが最初の一手。<strong>エクスポートは、ソリューションの中身を開いた画面には出てきません。</strong>一覧でソリューションの行を選ぶと、上のコマンドバーに「エクスポート」が現れます。あとは「公開 → 次へ」「不足している接続参照は✓のまま追加」「アンマネージドを選ぶ」と進めばZipがダウンロードできます。')
html += '\n\n<div class="v16-warn"><strong>⚠️ 黄色い「特権が不十分」の帯が出ても大丈夫。</strong> エクスポート自体は通ることが多いので、まず試してみてください。どうしても押せないときだけ、管理者に「システム カスタマイザー」ロールを依頼します。</div>'
html += SP

html += H2('使うときに、ここだけは守りたいこと')
html += P('便利な反面、AIに頼むときに気をつけたいこともあります。最後にこの3つだけ、共有させてください。')
html += figure("s16", "Copilotを使うときの3つの注意。便利だからこそ、ここは守りたいところ")
html += "\n\n<ul>\n<li><strong>🔒 機密データを貼らない</strong>：個人情報・社外秘・実在のメアドはチャットに入れない。サンプル値に置き換えてから相談する</li>\n<li><strong>✅ 生成物は必ず検証する</strong>：AIの式も間違うことがあります。そのまま信じず、実行して確かめてから本番へ</li>\n<li><strong>🏢 会社の設定を確認する</strong>：テナントによってはCopilotがオフのことも。使えないときは管理者に相談を</li>\n</ul>"
html += '\n\n<div class="v16-point"><strong>合言葉は、「AIはすごく頼れる下書き役。でも、最後に確かめるのは自分」。</strong> この2つを守れば、安心して毎日の味方にできます。</div>'
html += SP

html += H2('おわりに')
html += P('第16回は、式やJSONで止まっていたところを「Copilotに相談すれば前に進める」に変える回でした。むずかしい関数を暗記するより、<strong>正しく頼んで、確かめて使う</strong>。そのほうが、これからのPower Automateとは長く付き合えると思っています。')
html += P('当日のスライドは下のリンクから復習できます。よかったら手を動かしながら、自分のフローでも試してみてください。')
html += "\n\n<ul>\n<li>📚 <a href=\"https://haru-powerplatform.github.io/pa45/slides/vol-16/\" target=\"_blank\" rel=\"noopener\">第16回のスライド（復習用）</a></li>\n<li>📅 <a href=\"https://powerautomate-create.connpass.com/event/398546/\" target=\"_blank\" rel=\"noopener\">次回PA45の開催をチェックする</a></li>\n</ul>"
html += P('また次回、一緒に「できた！」を作りましょう。')

# ---------- 投稿作成 ----------
payload = {
    "title": "【PA45 第16回レポート】Copilotと作るPower Automate ── 式とJSONをAIに手伝わせる",
    "slug": SLUG,
    "status": "draft",
    "categories": [77],
    "content": html,
    "featured_media": ids["s05"],
}

# 既存スラッグがあれば更新
ex = requests.get(f"{WP}/wp-json/wp/v2/posts", auth=AUTH,
                  params={"slug": SLUG, "status": "draft,publish"}, timeout=60).json()
if ex:
    pid = ex[0]["id"]
    r = requests.post(f"{WP}/wp-json/wp/v2/posts/{pid}", auth=AUTH, json=payload, timeout=120)
    action = "更新"
else:
    r = requests.post(f"{WP}/wp-json/wp/v2/posts", auth=AUTH, json=payload, timeout=120)
    action = "新規作成"
r.raise_for_status()
post = r.json()
print(f"\n下書き{action}完了  ID={post['id']}")
print(f"編集URL : {WP}/wp-admin/post.php?post={post['id']}&action=edit")
print(f"プレビュー: {WP}/?p={post['id']}&preview=true")

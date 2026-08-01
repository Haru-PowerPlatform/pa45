#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""コパスタ第4弾ブログ＝「エージェントに社内文書を読ませて社内FAQにする（ナレッジの追加）」。
- 第3弾(Post2588)の"新オーケストレーターを試した"の続き。Vol.3の締め「ナレッジを足せば社内FAQに」を回収する記事。
- 画像＝コパスタVol.4スライド2枚（新規アップ）＋既にWPへ上げてある実機スクショ(build)を再利用。
- Microsoft Learn のスクショは転載せず、実機（はる本人の画面）と自作図解のみ使う。
- WordPress に新規下書きを作成。status:draft固定（自動公開しない）。post_state.jsonで同ID上書き。"""
import base64, requests, pathlib, re, json

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
STATE = HERE / "post_state.json"

TITLE = "Copilot Studioで社内FAQに答えるAIを作る｜エージェントに社内文書を読ませる「ナレッジ」の追加手順"
SLUG  = "copilot-studio-knowledge-add"
CAT   = 76

YT_URL   = "https://www.youtube.com/@Haru_PowerAutomate136"
CP_URL   = "https://powerautomate-create.connpass.com/event/399555/"
PA45_URL = "https://www.automate136.com/pa45/"

# 新規アップロードする画像（コパスタVol.4のスライド2枚）
IMG = {
    "concept": ROOT/"assets"/"x"/"html"/"cs-vol-04"/"csvol04.png",
    "steps":   ROOT/"assets"/"x"/"html"/"cs-vol-04b"/"csvol04b.png",
}
# 既にWPにある実機スクショ（第2弾でアップ済み）を再利用
U_BUILD = "https://www.automate136.com/wp-content/uploads/2026/07/cs-first-agent-build-scaled.png"

CSS = """
<style>
.mb-body > p{margin:1.9em 0!important;line-height:2.05!important;}
.mb-body > h2{margin-top:2.8em!important;}
.mb-body > h3{margin-top:2.4em!important;}
.mb-body > ul{margin:1.7em 0!important;line-height:2.0;}
.mb-body > ul li{margin:.55em 0;}
.mb-lead{line-height:2.1;}
.hl-marker{background:linear-gradient(transparent 58%,#e9d5ff 58%);font-weight:700;padding:0 .12em;border-radius:2px;}
.mb-intro{background:#f6f4fb;border:1px solid #e0d7f3;border-left:5px solid #a78bda;border-radius:10px;padding:13px 18px;margin:4px 0 30px;font-size:.9em;color:#5b4a7a;line-height:1.8;}
.mb-fig{margin:44px 0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#e7e0f5;border:1px solid #d0c4ec;border-radius:16px;padding:18px 16px 12px;box-shadow:0 2px 8px rgba(76,29,149,.08);}
.mb-fig img{width:100%;max-width:860px;height:auto;display:block;margin:0 auto;background:#fff;border-radius:10px;box-shadow:0 4px 14px rgba(91,33,182,.16);}
.mb-fig figcaption{font-size:.85em;color:#5b4a7a;margin-top:12px;}
.mb-shot{margin:56px 0;background:#eceef2;border:1px solid #d9dce3;border-radius:16px;padding:16px 16px 13px;box-shadow:0 3px 12px rgba(15,23,42,.09);}
.mb-shot .sh-tag{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:800;color:#475569;background:#dde1e9;border-radius:999px;padding:5px 14px;margin-bottom:12px;letter-spacing:.02em;}
.mb-shot .sh-frame{position:relative;line-height:0;}
.mb-shot .sh-frame img{width:100%;height:auto;display:block;border-radius:10px;border:1px solid #c7cad3;box-shadow:0 6px 18px rgba(15,23,42,.20);}
.mb-shot figcaption{font-size:.85em;color:#5b4a7a;margin-top:14px;line-height:1.65;}
.mb-anno{position:absolute;border:3px solid #e0342f;border-radius:12px;background:rgba(224,52,47,.04);box-shadow:0 5px 14px rgba(224,52,47,.40),0 0 0 4px rgba(224,52,47,.10);}
.mb-anno .an-lb{position:absolute;top:-16px;left:-4px;background:linear-gradient(180deg,#f5504b,#df332e);color:#fff;font-size:12.5px;font-weight:800;line-height:1.4;padding:3px 10px;border-radius:7px;white-space:nowrap;box-shadow:0 3px 7px rgba(0,0,0,.32);}
.mb-cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:30px 0;}
.mb-cards .cd{background:#fff;border:1px solid #e4dbf6;border-left:5px solid #8b5cf6;border-radius:12px;padding:15px 17px;box-shadow:0 2px 8px rgba(76,29,149,.07);}
.mb-cards .cd.old{border-left-color:#A4283C;}
.mb-cards .cd .cd-t{display:block;color:#5b21b6;font-weight:800;font-size:1.02em;margin-bottom:6px;}
.mb-cards .cd.old .cd-t{color:#A4283C;}
.mb-cards .cd .cd-d{font-size:.9em;color:#4b5563;line-height:1.65;}
@media(max-width:600px){.mb-cards{grid-template-columns:1fr;}}
.mb-copy{background:#faf7ff;border:1px dashed #c4b5fd;border-radius:10px;padding:16px 18px;margin:22px 0;line-height:1.95;color:#3b2a5a;font-size:.96em;}
.mb-copy .cp-ttl{font-weight:700;color:#6d28d9;font-size:.85em;margin-bottom:8px;letter-spacing:.03em;}
.mb-quote{background:#f4f6fb;border-left:5px solid #94a3b8;border-radius:8px;padding:15px 20px;margin:22px 0;font-size:1.0em;color:#334155;line-height:1.85;font-weight:600;}
.mb-point{background:#f7f4fd;border-left:6px solid #8b5cf6;border-radius:8px;padding:18px 24px;margin:36px 0;line-height:2.1;}
.mb-note{background:#fffdf5;border:2px solid #ffd54f;border-radius:12px;padding:18px 24px;margin:38px 0;line-height:2.1;}
.mb-note .nt-ttl{font-weight:700;color:#e8920c;margin:0 0 14px;}
.mb-warn{background:#fff6f6;border-left:6px solid #e57373;border-radius:8px;padding:18px 24px;margin:36px 0;line-height:2.1;}
.mb-table{width:100%;border-collapse:collapse;margin:30px 0;font-size:.94em;}
.mb-table th,.mb-table td{border:1px solid #e2ddf0;padding:12px 14px;line-height:1.7;text-align:left;vertical-align:top;}
.mb-table th{background:#f3eefc;color:#5b21b6;font-weight:800;white-space:nowrap;}
.mb-table td strong{color:#4c1d95;}
.mb-check{border:1px solid #ddd0f2;border-radius:14px;padding:22px 26px;background:#fff;margin:40px 0;}
.mb-check .ck-ttl{margin:0 0 14px;font-weight:800;font-size:1.05em;color:#5b21b6;}
.mb-check label{display:flex;align-items:flex-start;gap:10px;line-height:1.7;font-size:1em;margin:10px 0;}
.mb-check input{margin-top:4px;width:16px;height:16px;accent-color:#7c3aed;flex-shrink:0;}
.mb-cta{margin:42px 0;padding:18px 22px;border-radius:16px;text-align:center;}
.mb-cta.pa{background:linear-gradient(135deg,#eaf2fc,#d8e8fa);border:1px solid #b8d3ef;}
.mb-cta.yt{background:#fff5f5;border:1px solid #f4c2c2;}
.mb-cta .cta-ttl{font-weight:800;font-size:1.08em;margin:0 0 6px;color:#14528f;}
.mb-cta.yt .cta-ttl{color:#b91c1c;}
.mb-cta p{margin:0 0 12px;font-size:.92em;color:#475569;line-height:1.7;}
.mb-btn{display:inline-block;text-decoration:none;font-weight:800;font-size:.98em;padding:12px 28px;border-radius:50px;color:#fff!important;}
.mb-btn.pa{background:linear-gradient(135deg,#2a7dd4,#14528f);box-shadow:0 4px 14px rgba(42,125,212,.4);}
.mb-btn.yt{background:linear-gradient(135deg,#ef4444,#b91c1c);box-shadow:0 4px 14px rgba(239,68,68,.35);}
.mb-cta .cta-sub{display:block;margin-top:10px;font-size:.82em;color:#64748b;}
.speech-balloon{line-height:1.95;}
</style>
"""

def jp(t): return re.sub(r'。(?![」）】、\s<]|$)', '。<br>', t)
def fig(src, caption, alt=""):
    return f'\n\n<figure class="mb-fig"><img src="{src}" alt="{alt}" /><figcaption>{caption}</figcaption></figure>'
def shot(src, caption, alt="", annos=None):
    ov="".join(f'<div class="mb-anno" style="left:{l}%;top:{t}%;width:{w}%;height:{h}%;"><span class="an-lb">{lb}</span></div>' for (l,t,w,h,lb) in (annos or []))
    return (f'\n\n<figure class="mb-shot"><span class="sh-tag">&#x1f5a5;&#xfe0f; 実際の画面</span>'
            f'<div class="sh-frame"><img src="{src}" alt="{alt}" />{ov}</div>'
            f'<figcaption>{caption}</figcaption></figure>')
def cards(items):
    cs="".join(f'<div class="cd{" "+c if c else ""}"><span class="cd-t">{t}</span><span class="cd-d">{jp(d)}</span></div>' for t,d,c in items)
    return f'\n\n<div class="mb-cards">{cs}</div>'
def copybox(ttl, lines): return f'\n\n<div class="mb-copy"><div class="cp-ttl">{ttl}</div>'+"<br>".join(lines)+'</div>'
def quote(t): return f'\n\n<div class="mb-quote">{jp(t)}</div>'
def table(head, rows):
    th="".join(f"<th>{h}</th>" for h in head)
    tr="".join("<tr>"+"".join(f"<td>{c}</td>" for c in r)+"</tr>" for r in rows)
    return f'\n\n<table class="mb-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'
P=lambda t:f"\n\n<p>{jp(t)}</p>"
PL=lambda t:f'\n\n<p class="mb-lead">{jp(t)}</p>'
H2=lambda t:f"\n\n<h2>{t}</h2>"
H3=lambda t:f"\n\n<h3>{t}</h3>"
NB="\n\n&nbsp;"
def ul(items): return "\n\n<ul>"+"".join(f"\n<li>{jp(i)}</li>" for i in items)+"\n</ul>"
def point(t): return f'\n\n<div class="mb-point">{jp(t)}</div>'
def note(ttl,t): return f'\n\n<div class="mb-note"><p class="nt-ttl">{ttl}</p>{jp(t)}</div>'
def warn(t): return f'\n\n<div class="mb-warn">{jp(t)}</div>'
def cta_yt():
    return ('\n\n<div class="mb-cta yt"><p class="cta-ttl">&#x25b6; 動きは動画で見るのが早いです</p>'
            '<p>エージェントの作り方や実演は、PA45の各回をYouTubeにアーカイブしています。</p>'
            f'<a class="mb-btn yt" href="{YT_URL}" target="_blank" rel="noopener">PA45のYouTubeチャンネルを見る</a></div>')
def cta_pa(ttl, body):
    return (f'\n\n<div class="mb-cta pa"><p class="cta-ttl">{ttl}</p><p>{jp(body)}</p>'
            f'<a class="mb-btn pa" href="{CP_URL}" target="_blank" rel="noopener">次回のPA45に申し込む（無料）</a>'
            '<span class="cta-sub">毎週木曜の夜・オンライン・参加無料／途中入退室OK・見るだけ参加も歓迎です</span></div>')

# ---- WP ----
env={}
for line in (ROOT/".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1); env[k.strip()]=v.strip()
WP=env["WP_URL"].rstrip("/")
auth=base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
H={"Authorization":f"Basic {auth}"}
state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"post_id":None,"media":{}}

def upload(key):
    if key in state["media"]: return state["media"][key]["url"]
    p=IMG[key]
    if not p.exists(): print("WARN not found",p); return ""
    mh=dict(H); mh["Content-Disposition"]=f'attachment; filename="cs-knowledge-{key}.png"'; mh["Content-Type"]="image/png"
    r=requests.post(f"{WP}/wp-json/wp/v2/media",headers=mh,data=p.read_bytes(),timeout=180); r.raise_for_status(); j=r.json()
    state["media"][key]={"id":j["id"],"url":j["source_url"]}; print("uploaded",key,"->",j["id"]); return j["source_url"]

U_CONCEPT=upload("concept")
U_STEPS=upload("steps")
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")

# ---- 本文 ----
H_=[]; a=H_.append
a('\n\n<div class="mb-intro">この記事は、筆者が Copilot Studio を実際にさわりながら、公式ドキュメント（Microsoft Learn）で仕様を確かめつつ整理したものです。専門用語はなるべく使わず、はじめてさわる方向けの言葉で書いています。</div>')

a(PL('前回までで、Copilot Studio に<strong>指示文を4行書いただけ</strong>のエージェント（AI）を作りました。まとめて質問しても自分で分解して答えてくれる、なかなか賢い子です。'))
a(PL('ただ、ひとつ足りないものがありました。<span class="hl-marker">会社のことは答えられない</span>のです。'))
a(PL('「有給って何日前までに申請するの？」と聞いても、返ってくるのは「一般的には…」という話。結局は自分で就業規則を開くことになります。'))
a(PL('ここで足すのが<strong>ナレッジ（Knowledge）</strong>です。エージェントに"参考資料"として会社の文書を渡すと、答えが一気に社内基準に変わります。'))

a(fig(U_CONCEPT, "▲ 社内文書を1つ足すだけで、答えが「一般論」から「うちのルール」に変わる", "Copilot Studioでナレッジを追加する前と後の回答の違い"))

a(NB)
a(H2('ナレッジとは、エージェントに渡す"参考資料"のこと'))
a(P('ナレッジは、エージェントが回答するときに参照できるデータのことです。指示文が「どう振る舞うか」を決めるのに対して、ナレッジは「何をもとに答えるか」を決めます。'))
a(cards([
 ('&#x1f4dd; 指示文（Instructions）', 'キャラクターや答え方のルールを決める部分。「日本語で丁寧に」「わからないことは正直にわからないと言う」など、振る舞いを書く。', ''),
 ('&#x1f4da; ナレッジ（Knowledge）', '答えの根拠になる資料そのもの。就業規則、手順書、製品マニュアル、SharePointのサイトなどを渡すと、その中身をもとに答えるようになる。', ''),
]))
a(point('言いかえると、<span class="hl-marker">指示文＝人柄、ナレッジ＝手元の資料</span>です。新人さんに「丁寧に応対してね」と伝えるだけでなく、社内マニュアルを渡してあげるのと同じことをしています。'))
a(note('&#x1f4a1; 「PA45」とは？','この記事に出てくる <strong>PA45</strong> は、筆者が運営している<strong>「Power Automate を45分で学ぶ、無料のオンライン勉強会」</strong>です（毎週木曜の夜・初心者歓迎）。今回のエージェントも、この勉強会の題材として作っています。'))

a(NB)
a(H2('追加できる資料の種類'))
a(P('ナレッジとして追加できるものは、思ったより幅広いです。代表的なものを挙げます。'))
a(table(['追加できるもの','こんなときに使う'],[
 ['<strong>ファイルのアップロード</strong>','就業規則、手順書、製品カタログなど、決まった文書を直接読ませたいとき'],
 ['<strong>SharePoint</strong>','部署のサイトやドキュメントライブラリを丸ごと参照させたいとき'],
 ['<strong>公開Webサイト</strong>','自社の公開ページや、公開されている製品ドキュメントを参照させたいとき'],
 ['<strong>Dataverse</strong>','テーブルに入っている業務データ（申請、案件など）を参照させたいとき'],
 ['<strong>Azure AI Search</strong>','大量の文書をすでに検索用に整えてある場合'],
 ['そのほか','Dynamics 365、Salesforce、ServiceNow など。追加ダイアログの「Advanced」タブには Confluence や Jira なども並びます'],
]))
a(P('最初の一歩としておすすめなのは、いちばん上の<strong>ファイルのアップロード</strong>です。PDF や Word をドラッグして入れるだけなので、管理者に相談しなくても試せます。'))

a(NB)
a(H2('やってみる：ナレッジを足す3ステップ'))
a(P('新しい画面（新エクスペリエンス）での手順です。ここでは、就業規則の PDF を1つ読ませてみます。'))
a(fig(U_STEPS, "▲ ナレッジの足し方。追加ダイアログから資料を選び、名前と説明を書いて追加するだけ", "Copilot Studioのナレッジ追加ダイアログと3ステップの図解"))

a(H3('① Buildタブの右パネルで「Knowledge」の＋を押す'))
a(P('エージェントを開くと、画面の右側にコンポーネントのパネルが並んでいます。Model（モデル）、Tools（ツール）と続いて、<strong>Knowledge</strong> の行があります。その右端の <strong>＋</strong> が入口です。'))
a(shot(U_BUILD, "▲ 右パネルの Knowledge。既定では「Search all websites（Web検索）」だけが入っている", "Copilot StudioのBuildタブ右パネルにあるKnowledgeの項目",
   annos=[(70.5,44,28.5,17,"① ここの＋から追加")]))
a(P('作ったばかりのエージェントには、たいてい <strong>Search all websites</strong>（Web を検索する）だけが入っています。冒頭の「一般論しか返ってこない」は、これが理由です。'))

a(H3('②「Add knowledge」で追加元を選ぶ'))
a(P('＋を押すと <strong>Add knowledge</strong>（ナレッジの追加）というダイアログが開きます。'))
a(P('いちばん目立つ場所に<strong>ファイルの投入エリア</strong>があり、そこへ PDF や Word をドラッグするだけで追加できます。OneDrive や SharePoint にあるファイルを指定することもできます。'))
a(P('その下には <strong>Featured</strong>（おすすめ）と <strong>Advanced</strong> のタブがあり、SharePoint、公開Webサイト、Dataverse などのカードが並びます。使いたい追加元をここから選びます。'))
a(copybox('&#x1f4c2; ファイルで追加するときの対応形式', [
 'Word（doc / docx）、Excel（xls / xlsx）、PowerPoint（ppt / pptx）、PDF',
 'テキスト（txt / md / log）、HTML、CSV、XML、JSON、YAML など',
 '※ 画像・動画・音声そのものは追加できません（PDFに埋め込まれた画像は読めます）',
]))

a(H3('③ 名前と「説明」を書いて追加する'))
a(P('資料を選んだあとは、名前と説明を入力して「エージェントに追加」で完了です。'))
a(P('ここでいちばん大事なのが<strong>説明</strong>です。エージェントは、質問を受けたときに「どの資料を見にいくか」を自分で判断します。その判断材料が、この説明文です。'))
a(cards([
 ('&#x274c; もったいない説明', '「就業規則」だけ。何が書いてあるのか分からないので、AI が参照すべき場面を判断しづらい。', 'old'),
 ('&#x2b55; 効く説明', '「有給休暇・特別休暇・勤務時間・申請期限など、社員の勤務に関する社内規程。休暇や勤怠の質問はこの資料を参照する」と具体的に書く。', ''),
]))
a(point('資料が2つ3つと増えてくると、この説明の書き方で回答の精度がはっきり変わってきます。<span class="hl-marker">面倒でも、1〜2文は具体的に書いておく</span>のがおすすめです。'))

a(NB)
a(H2('追加すると、答えはこう変わる'))
a(P('同じ質問をもう一度投げてみます。'))
a(quote('有給って、何日前までに申請すればいいですか？'))
a(P('ナレッジを足す前は「一般的には数日前から2週間前まで…」という一般論でした。'))
a(P('足したあとは、<strong>就業規則の中身</strong>をもとに「原則5営業日前まで」と答えます。しかも回答の下に<strong>出典</strong>が付き、どのファイルの何条を見たのかが分かります。'))
a(point('この<span class="hl-marker">出典が付くところ</span>が、社内で使ううえではかなり重要です。AI の答えをうのみにせず、元の資料をその場で確認できるからです。'))

a(NB)
a(H2('つまずきやすいポイント（先に知っておきたい制限）'))
a(P('公式ドキュメントで確認できた制限のうち、実務で引っかかりそうなものを挙げておきます。'))
a(table(['制限','内容'],[
 ['ファイルサイズ','1ファイル <strong>512MB</strong> まで'],
 ['ファイル数','1つのエージェントに <strong>最大500ファイル</strong> まで'],
 ['読めないファイル','画像・動画・音声・実行ファイルは不可。<strong>パスワード保護や暗号化されたファイル</strong>も不可'],
 ['SharePointリスト','一度に選べるのは最大10個。<strong>35,000行を超えるリスト</strong>は精度と応答速度に影響'],
 ['アクセス権','SharePoint を参照する場合、<strong>その人が見られる資料からしか回答しない</strong>（権限が引き継がれる）'],
 ['環境の設定','ファイルをアップロードして使うには、環境で <strong>Dataverse 検索</strong>が有効になっている必要があります'],
]))
a(warn('とくに注意したいのが<strong>アクセス権</strong>です。SharePoint をナレッジにした場合、回答は「質問した人が見られる範囲」に限られます。これは安全側の動きですが、逆に言えば<strong>「同じ質問でも人によって答えが変わる」</strong>ということでもあります。テストは、実際に使う人の権限でも確認しておくと安心です。'))
a(note('&#x26a0; 新しい画面は今のところ英語表示です','新エクスペリエンス（新しいエージェント作成画面）は、現時点では英語表示で、production-ready preview という位置づけです。ボタン名が英語のままでも、やっていることは記事のとおりです。'))

a(NB)
a(H2('社内で使う前に、ひと呼吸'))
a(P('技術的には数分で追加できてしまうので、つい勢いで進めたくなります。ただ、社内文書を AI に読ませる前に、次の2点だけは確認しておきたいところです。'))
a(ul([
 '<strong>その資料は、誰に見せてよいものか</strong>。人事評価や個人情報を含む資料は、まず対象から外す',
 '<strong>会社としての生成AIの利用ルール</strong>。テナントの設定や社内ガイドラインの範囲内かどうかを、情シスに一度確認しておく',
]))
a(P('筆者は、まず自分で作った公開資料（勉強会の案内など）で試してから、社内文書に広げるようにしています。'))

a(NB)
a(H2('まとめ'))
a(P('今回やったことは、これだけです。'))
a(ul([
 'Buildタブ右パネルの <strong>Knowledge の＋</strong> を押す',
 '<strong>Add knowledge</strong> のダイアログで、ファイルや SharePoint を選ぶ',
 '<strong>名前と説明</strong>を書いて「エージェントに追加」',
]))
a(P('指示文は1文字も変えていません。それでも、答えは「たぶん一般論」から「うちのルール」に変わります。'))
a(P('社内の"よくある質問"を集めた FAQ ページを作ってはみたものの、けっきょく誰も見にこない。そんな資料こそ、エージェントに読ませてしまうのが向いていると思っています。'))

a('\n\n<div class="mb-check"><p class="ck-ttl">&#x1f4cb; この記事で学んだこと</p>'
 + "".join(f'<label><input type="checkbox">{t}</label>' for t in [
   'ナレッジ＝エージェントが答えの根拠にする<strong>参考資料</strong>',
   '追加は <strong>Build タブ → Knowledge の＋ → Add knowledge</strong> の3ステップ',
   'PDFやWordは<strong>ドラッグするだけ</strong>で追加できる',
   '<strong>説明</strong>を具体的に書くほど、参照する資料の選び方が正確になる',
   '<strong>512MB／500ファイル</strong>、画像・動画・暗号化ファイルは不可',
   'SharePointは<strong>閲覧権限が引き継がれる</strong>ので、テストは実際の権限でも行う',
 ]) + '</div>')

a(NB)
a(H2('次回のPA45で、続きを一緒に作りませんか'))
a(P('PA45 では、こうした「45分でひとつ作る・試す」ハンズオンを、<strong>毎週木曜の夜にオンライン無料</strong>でやっています。手が止まりやすいところも、その場で質問しながら進められます。'))
a(cta_pa('&#x1f64c; こういうのを、毎週みんなで試しています',
 'PA45は知識ゼロ・見るだけ参加も大歓迎です。次回もまた、ひとつ新しいものを一緒にさわります。お申し込みは下のボタンから（無料）。'))
a(P(f'過去回のまとめや、PA45がどんな勉強会かは <a href="{PA45_URL}" target="_blank" rel="noopener">PA45の紹介ページ</a> にまとめています。また次回、一緒に「できた！」を作りましょう。'))
a(cta_yt())

a('\n\n<p style="font-size:13px;color:#888;line-height:1.9;">※ 本記事は公開日時点の情報をもとに、筆者が実際に学んで試した内容を整理したものです。Copilot Studio の画面や仕様は更新されることがあるため、最新の状況は公式情報（Microsoft Learn）もあわせてご確認ください。ファイル形式・容量・件数などの制限は Microsoft Learn の記載を参照しています。</p>')
a('\n\n<p style="font-size:13px;color:#888;line-height:1.9;">※ 本記事の構成や図解の一部は、AI と壁打ちしながら作成しています。</p>')

content=CSS+'\n\n<div class="mb-body">'+"".join(H_)+'\n\n</div>'
(HERE/"article.html").write_text(content,encoding="utf-8")
print("article.html:",len(content),"chars")

payload={"title":TITLE,"slug":SLUG,"status":"draft","content":content,"categories":[CAT]}
if state["media"].get("concept"): payload["featured_media"]=state["media"]["concept"]["id"]
if state.get("post_id"):
    r=requests.post(f"{WP}/wp-json/wp/v2/posts/{state['post_id']}",headers=H,json=payload,timeout=120); r.raise_for_status(); pid=state["post_id"]; print("UPDATED",pid)
else:
    r=requests.post(f"{WP}/wp-json/wp/v2/posts",headers=H,json=payload,timeout=120); r.raise_for_status(); pid=r.json()["id"]; state["post_id"]=pid; print("CREATED",pid)
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")
print("status:",r.json()["status"])
print("EDIT    =",f"{WP}/wp-admin/post.php?post={pid}&action=edit")
print("PREVIEW =",f"{WP}/?p={pid}&preview=true")

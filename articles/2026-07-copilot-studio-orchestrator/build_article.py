#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""コパスタ第3弾ブログ＝「新オーケストレーターを試してみた」実演レポート。
- 第2弾(Post2583)の作り方記事と重複させず、"何がすごいか"を実機で見せる角度。
- 実機スクショは第2弾でアップ済みのWPメディアURLを再利用（build/plan/answer）。concept=csvol03を新規アップ。
- .mb-*系（紫）テイスト／実機スクショ枠＋赤枠マーカー／図解カード／冒頭の一言／PA45補足／末尾免責。
- WordPress に新規下書きを作成。status:draft固定（自動公開しない）。post_state.jsonで同ID上書き。"""
import base64, requests, pathlib, re, json

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
STATE = HERE / "post_state.json"

TITLE = "“4行の指示書”だけで、まとめ質問に出典つきで答えるAI｜Copilot Studioの新オーケストレーターを試してみた"
SLUG  = "copilot-studio-orchestrator-test"
CAT   = 76

YT_URL   = "https://www.youtube.com/@Haru_PowerAutomate136"
CP_URL   = "https://powerautomate-create.connpass.com/event/399555/"
PA45_URL = "https://www.automate136.com/pa45/"

# concept=新規アップ、他3枚は第2弾(Post2583)でアップ済みURLを再利用
IMG = { "concept": ROOT/"assets"/"x"/"html"/"cs-vol-03"/"csvol03.png" }
U_BUILD  = "https://www.automate136.com/wp-content/uploads/2026/07/cs-first-agent-build-scaled.png"
U_PLAN   = "https://www.automate136.com/wp-content/uploads/2026/07/cs-first-agent-plan.png"
U_ANSWER = "https://www.automate136.com/wp-content/uploads/2026/07/cs-first-agent-answer.png"

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
def bubble(text):
    return ('\n\n<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">'
            '<div class="speech-person"><figure class="speech-icon">'
            '<img class="speech-icon-image" src="https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png" alt="" width="1024" height="1024" /></figure></div>'
            f'<div class="speech-balloon">{jp(text)}</div></div>')
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
    mh=dict(H); mh["Content-Disposition"]=f'attachment; filename="cs-orch-{key}.png"'; mh["Content-Type"]="image/png"
    r=requests.post(f"{WP}/wp-json/wp/v2/media",headers=mh,data=p.read_bytes(),timeout=180); r.raise_for_status(); j=r.json()
    state["media"][key]={"id":j["id"],"url":j["source_url"]}; print("uploaded",key,"->",j["id"]); return j["source_url"]

U_CONCEPT=upload("concept")
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")

# ---- 本文 ----
H_=[]; a=H_.append
a('\n\n<div class="mb-intro">この記事は、筆者が実際に Copilot Studio で作った AI を試しながら、気になったポイントを AI と壁打ち（相談）しつつまとめたものです。「なぜこう動くのか」を、実際の画面で追いかけていきます。</div>')

a(PL('前回、Copilot Studio で「質問に答える受付 AI」を作りました。今回は、その AI に <span class="hl-marker">"まとめて3つ"の質問を一度に投げてみます</span>。'))
a(PL('おどろいたのは、こちらが書いたのは<strong>指示文4行だけ</strong>なのに、AI が<strong>自分で質問を分解し、必要な情報を調べて、出典つきで答えた</strong>こと。「会話の台本（分岐）」は1つも作っていません。'))
a(PL('この「AI が自分で段取りを組む」しくみ＝<strong>新オーケストレーター</strong>を、実際のやり取りで見ていきます。'))

a(fig(U_CONCEPT, "▲ 今回のポイント。渡した4行から、AI が自分で段取りして答えるまで", "Copilot Studioの新オーケストレーターの概念図"))

a(NB)
a(H2('用意したのは「4行の指示書」だけ'))
a(P('今回テストする AI に与えた指示（Instructions）は、これだけです。むずかしい設定はしていません。'))
a(copybox('&#x1f4dd; 与えた指示文（4行）', [
 'あなたは「PA45」という Power Automate 勉強会の受付エージェントです。',
 '参加者からの質問に日本語で丁寧に答えます。',
 'PA45 は毎月開催・参加無料・初心者歓迎のオンライン勉強会です。',
 'わからないことは正直に「わからない」と答え、推測で断言しません。',
]))
a(shot(U_BUILD, "▲ 与えたのはこの4行と、既定のまま（右側の道具はいじっていない）", "Copilot Studioの指示文を入れた作成画面",
   annos=[(5.3,29.5,35,15,"① この4行だけ"),(84.8,11,14,7,"あとは既定のまま")]))
a(note('&#x1f4a1; 「PA45」とは？','この記事に出てくる <strong>PA45</strong> は、筆者が運営している<strong>「Power Automate を45分で学ぶ、無料のオンライン勉強会」</strong>です（毎週木曜の夜・初心者歓迎）。今回はこの勉強会の受付 AI を題材にしています。'))

a(NB)
a(H2('まとめて"3つ"質問してみた'))
a(P('わざと意地悪をして、1つのメッセージに<strong>3つの用件を詰め込んで</strong>送ってみます。'))
a(quote('初参加を考えています。PA45 がどんな会か教えて。あと、まったく触ったことがなくても大丈夫か、参加前に準備しておくことも合わせて教えて。'))
a(P('ふつうのチャットボットなら「どれか1つ」しか拾えなさそうな質問です。さて、どうなったか。'))

a(H3('AI は、まず"段取り"を組んだ'))
a(P('答えを返す<strong>前に</strong>、AI 自身が「ユーザーは3つ聞いている」と気づき、何をどの順で調べるかを決めていました。その思考の様子が、画面にそのまま出ます。'))
a(shot(U_PLAN, "▲ 回答の前に、質問を3つに分解し「何を調べるか」を自分で段取りしている", "Copilot Studioが回答前に段取りを組んでいる様子",
   annos=[(7.5,67,84,31,"AIが自分で段取り中")]))
a(point('くり返しますが、<span class="hl-marker">会話の分岐（トピック）は1つも作っていません</span>。それでも「3つ聞かれている」と理解し、調べる順番まで自分で決めています。ここが新オーケストレーターの一番の見どころです。'))

a(H3('そして、出典つきで整理して答えた'))
a(P('段取りのあと、返ってきた答えがこちらです。3つの用件が<strong>見出しに分かれ</strong>、表で整理され、右上には<strong>出典番号①</strong>まで付いていました。'))
a(shot(U_ANSWER, "▲ 3つの用件が見出しで整理され、表つき・出典つきで返ってきた", "Copilot Studioエージェントが整理して回答している画面",
   annos=[(4.5,40,86,15,"見出しに整理＋出典①つき")]))
a(P('指示文には「毎週木曜」や「connpass で申込」とは書いていません。それでも正しく答えられたのは、AI が<strong>ナレッジ（今回は Web 検索）を自分で調べて</strong>補ったからです。しかも、どこを参照したかを出典で示してくれます。'))

a(NB)
a(H2('なぜ4行で動くの？── 昔の"台本方式"との違い'))
a(P('少し前まで、この手のボットは<strong>「トピック」</strong>という会話の分岐を、人間が1つずつ設計するのが当たり前でした。今は、その考え方が大きく変わっています。'))
a(cards([
 ('&#x1f3ad; これまで：台本（トピック）方式', '会話の分岐を人がぜんぶ設計。台本にない質問は「わかりません」。質問が増えるたびに分岐を追加・修正…と手間が増える。', 'old'),
 ('&#x1f9e0; これから：新オーケストレーター', '渡すのは指示文（ゴール）と道具だけ。複数の質問も自分で分解し、必要なら調べて、順に答える。分岐の設計そのものが不要。', ''),
]))
a(point('ざっくり言うと、<span class="hl-marker">「何を答えるか」は指示文で教え、「どう段取りするか」は AI に任せる</span>、という分担です。だから、指示文4行でも複雑な質問に対応できました。'))

a(NB)
a(H2('もっと賢く・正確にするには（ナレッジを足す）'))
a(P('今回のナレッジは「Web 検索」だけでした。そのため、<strong>社内固有の情報は一般論になってしまう</strong>ことがあります。'))
a(P('「うちの規程や手順書に沿って答えてほしい」という場合は、右パネルの <strong>Knowledge（ナレッジ）</strong> に、<strong>SharePoint やファイル</strong>を追加します。すると、その資料を根拠に、出典つきで答えてくれるようになります。'))
a(P('この一手を加えると、「社内の"よくある質問"に自動で答える AI」に、ぐっと近づきます。'))

a(NB)
a(H2('まとめ'))
a(P('今回わかったのは、次のことです。'))
a(ul(['<strong>指示文4行だけ</strong>でも、まとめて聞いた3つの質問にちゃんと答えられた',
      '会話の台本（トピック）を作らなくても、AI が<strong>自分で質問を分解</strong>して段取りを組む',
      '必要な情報は<strong>自分で調べ</strong>、しかも<strong>出典つき</strong>で示してくれる',
      '社内の正確な回答をさせたいなら、<strong>ナレッジに社内文書を足す</strong>']))
a(P('「作りたいことを文章で書くだけ」で、ここまで動く。むずかしい分岐設計を覚えなくても、複雑な質問に対応できる。これが今の Copilot Studio の手ざわりです。'))

a('\n\n<div class="mb-check"><p class="ck-ttl">&#x1f4cb; この記事で学んだこと</p>'
 + "".join(f'<label><input type="checkbox">{t}</label>' for t in [
   '新オーケストレーターは、まとめ質問を<strong>自分で分解</strong>して答える',
   'トピック（会話の分岐）を作らなくても複雑な質問に対応できる',
   '回答には<strong>出典①</strong>が付き、どこを参照したか分かる',
   '「何を答えるか」＝指示文／「どう段取りするか」＝AI に任せる',
   '精度を上げたいときは<strong>ナレッジに社内文書</strong>を足す',
 ]) + '</div>')

a(NB)
a(H2('次回のPA45で、続きを一緒に作りませんか'))
a(P('PA45 では、こうした「45分でひとつ作る・試す」ハンズオンを、<strong>毎週木曜の夜にオンライン無料</strong>でやっています。一人で詰まりがちなところも、その場で質問しながら進められます。'))
a(cta_pa('&#x1f64c; こういうのを、毎週みんなで試しています',
 'PA45は知識ゼロ・見るだけ参加も大歓迎です。次回もまた、ひとつ新しいものを一緒にさわります。お申し込みは下のボタンから（無料）。'))
a(P(f'過去回のまとめや、PA45がどんな勉強会かは <a href="{PA45_URL}" target="_blank" rel="noopener">PA45の紹介ページ</a> にまとめています。また次回、一緒に「できた！」を作りましょう。'))
a(cta_yt())

a('\n\n<p style="font-size:13px;color:#888;line-height:1.9;">※ 本記事は公開日時点の情報をもとに、筆者が実際に学んで試した内容を整理したものです。Copilot Studio の画面や仕様は更新されることがあるため、最新の状況は公式情報（Microsoft Learn）もあわせてご確認ください。画面の項目名・挙動は実機（Copilot Studio）で確認しています。</p>')
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

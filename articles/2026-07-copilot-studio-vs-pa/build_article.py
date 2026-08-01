#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""コパスタ第1弾ブログ＝「Copilot Studio って何？ Power Automate との違い」入門・比較。
- 元ネタ=コパスタX Vol.1（作業ロボ↔考える受付係）。concept=csvol01を新規アップ、home=第2弾でアップ済みURL再利用。
- 恒久ルール準拠：.mb-shot(グレー枠+タグ)+.mb-anno(赤枠)/mb-intro冒頭一言/PA45補足/図解カード/比較表/句点改行/末尾免責。
- WordPress新規下書き。status:draft固定（自動公開しない）。post_state.jsonで同ID上書き。"""
import base64, requests, pathlib, re, json

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
STATE = HERE / "post_state.json"

TITLE = "Copilot Studio って何？ Power Automate と何が違うの？｜“作業ロボ”と“考える受付係”のたとえで整理"
SLUG  = "copilot-studio-vs-power-automate"
CAT   = 76

YT_URL   = "https://www.youtube.com/@Haru_PowerAutomate136"
CP_URL   = "https://powerautomate-create.connpass.com/event/399555/"
PA45_URL = "https://www.automate136.com/pa45/"

IMG = { "concept": ROOT/"assets"/"x"/"html"/"cs-vol-01"/"csvol01.png" }
U_HOME = "https://www.automate136.com/wp-content/uploads/2026/07/cs-first-agent-home-scaled.png"

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
.mb-cards .cd.pa{border-left-color:#2563EB;}
.mb-cards .cd .cd-t{display:block;color:#5b21b6;font-weight:800;font-size:1.02em;margin-bottom:6px;}
.mb-cards .cd.pa .cd-t{color:#1e40af;}
.mb-cards .cd .cd-d{font-size:.9em;color:#4b5563;line-height:1.65;}
@media(max-width:600px){.mb-cards{grid-template-columns:1fr;}}
.mb-cmpwrap{overflow-x:auto;margin:26px 0;}
.mb-cmp{width:100%;border-collapse:collapse;font-size:.95em;min-width:460px;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(76,29,149,.07);}
.mb-cmp th,.mb-cmp td{padding:12px 15px;text-align:left;border-bottom:1px solid #ece4f9;line-height:1.6;vertical-align:top;}
.mb-cmp thead th{font-weight:800;font-size:.92em;}
.mb-cmp thead th.h-obs{background:#f5f5f7;color:#4b5563;}
.mb-cmp thead th.h-pa{background:#eaf1fd;color:#1e40af;}
.mb-cmp thead th.h-cs{background:#f3eefc;color:#5b21b6;}
.mb-cmp tbody th{background:#fafafb;color:#4b5563;font-weight:700;font-size:.9em;white-space:nowrap;width:1%;}
.mb-cmp td.c-cs{color:#3b2a5a;}
.mb-cmp tr:last-child td,.mb-cmp tr:last-child th{border-bottom:none;}
.mb-point{background:#f7f4fd;border-left:6px solid #8b5cf6;border-radius:8px;padding:18px 24px;margin:36px 0;line-height:2.1;}
.mb-note{background:#fffdf5;border:2px solid #ffd54f;border-radius:12px;padding:18px 24px;margin:38px 0;line-height:2.1;}
.mb-note .nt-ttl{font-weight:700;color:#e8920c;margin:0 0 14px;}
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
def cmp_table(rows):
    body=""
    for obs,pa,cs in rows:
        body+=f'<tr><th>{obs}</th><td>{pa}</td><td class="c-cs">{cs}</td></tr>'
    return ('\n\n<div class="mb-cmpwrap"><table class="mb-cmp"><thead><tr>'
            '<th class="h-obs">観点</th><th class="h-pa">Power Automate</th><th class="h-cs">Copilot Studio</th>'
            f'</tr></thead><tbody>{body}</tbody></table></div>')
P=lambda t:f"\n\n<p>{jp(t)}</p>"
PL=lambda t:f'\n\n<p class="mb-lead">{jp(t)}</p>'
H2=lambda t:f"\n\n<h2>{t}</h2>"
NB="\n\n&nbsp;"
def ul(items): return "\n\n<ul>"+"".join(f"\n<li>{jp(i)}</li>" for i in items)+"\n</ul>"
def point(t): return f'\n\n<div class="mb-point">{jp(t)}</div>'
def note(ttl,t): return f'\n\n<div class="mb-note"><p class="nt-ttl">{ttl}</p>{jp(t)}</div>'
def cta_yt():
    return ('\n\n<div class="mb-cta yt"><p class="cta-ttl">&#x25b6; 動きは動画で見るのが早いです</p>'
            '<p>Power Automate や Copilot Studio の実演は、PA45の各回をYouTubeにアーカイブしています。</p>'
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
    mh=dict(H); mh["Content-Disposition"]=f'attachment; filename="cs-vs-pa-{key}.png"'; mh["Content-Type"]="image/png"
    r=requests.post(f"{WP}/wp-json/wp/v2/media",headers=mh,data=p.read_bytes(),timeout=180); r.raise_for_status(); j=r.json()
    state["media"][key]={"id":j["id"],"url":j["source_url"]}; print("uploaded",key,"->",j["id"]); return j["source_url"]
U_CONCEPT=upload("concept")
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")

# ---- 本文 ----
H_=[]; a=H_.append
a('\n\n<div class="mb-intro">この記事は、筆者が実際に Copilot Studio をさわりながら、気になったポイントを AI と壁打ち（相談）しつつ整理したものです。「Power Automate は知っているけれど、Copilot Studio は…」という方に向けて、両者の違いをたとえ話でまとめます。</div>')

a(PL('「Power Automate は使っているけれど、<span class="hl-marker">Copilot Studio って何が違うの？</span>」── よく聞かれます。'))
a(PL('ざっくり言うと、Power Automate は<strong>「決めた手順をそのままくり返す」自動化</strong>、Copilot Studio は<strong>「会話して自分で考えて動く」AI</strong>です。'))
a(PL('この記事では、その違いと「<strong>どっちを使えばいいか</strong>」を、なるべくかんたんなたとえ話で整理していきます。'))

a(fig(U_CONCEPT, "▲ ひとことで言うと。Power Automate は“作業ロボ”、Copilot Studio は“考える受付係”", "Power AutomateとCopilot Studioの違いの概念図"))

a(NB)
a(H2('ひとことで言うと ── “作業ロボ”と“考える受付係”'))
a(P('いちばん簡単なたとえは、これです。'))
a(cards([
 ('&#x1f9be; Power Automate ＝ “作業ロボ”', '決めた手順（トリガー→アクション）を、速く・正確に・何度もくり返す。その場の判断は入らず、台本どおりに動く。', 'pa'),
 ('&#x1f4ac; Copilot Studio ＝ “考える受付係”', '自然な言葉で質問に答え、状況に応じて自分で判断する。社内の文書を読んで答えることもできる。', ''),
]))
a(P('<strong>「手順」で動くのが Power Automate、「会話と判断」で動くのが Copilot Studio</strong>。まずはこう覚えると、頭が整理しやすいです。'))

a(NB)
a(H2('具体的に、どう違う？'))
a(P('もう少しかみくだいて、5つの面で並べてみます。'))
a(cmp_table([
 ('動き出すきっかけ','何かが起きたとき（例：メール受信）','人が話しかけたとき'),
 ('動き方','決めた手順どおりに実行','会話して、自分で段取りを判断'),
 ('得意なこと','定型作業のくり返し','質問対応・案内・あいまいな相談'),
 ('苦手なこと','あいまいな会話','厳密な定型処理（それは PA が得意）'),
 ('たとえの例','添付を自動で OneDrive 保存','社内 FAQ に答える AI'),
]))
a(P('どちらが上・下ではなく、<strong>得意分野がちがう</strong>だけです。「手作業のくり返しを消す」なら Power Automate、「人の質問に答える」なら Copilot Studio、というイメージです。'))

a(NB)
a(H2('実際の画面で見ると（Copilot Studio の入口）'))
a(P('Copilot Studio を開くと、最初に<strong>「何を作るか」を2つから選びます</strong>。この2択に、さっきの違いがそのまま表れています。'))
a(shot(U_HOME, "▲ Copilot Studio の新しいホーム。「Agent（会話するAI）」と「Workflow（手順の自動化）」の2つが入口", "Copilot Studioの新しいホーム画面",
   annos=[(27.5,33.5,31.5,37,"会話するAI（エージェント）"),(60.5,33.5,31,37,"手順の自動化（PAに近い）")]))
a(P('左の <strong>「Agent（エージェント）」</strong> が、会話して答える AI。右の <strong>「Workflow（ワークフロー）」</strong> は手順の自動化で、こちらは<strong>使い慣れた Power Automate に近いもの</strong>です。'))
a(point('つまり Copilot Studio の主役は<span class="hl-marker">「会話するAI（エージェント）」</span>です。「決まった手順を自動化したいだけ」なら、無理に乗りかえず<strong>使い慣れた Power Automate でもOK</strong>。目的で選べば大丈夫です。'))

a(NB)
a(H2('どっちを使えばいい？（かんたんな使い分け）'))
a(P('迷ったら、この2つで判断すると分かりやすいです。'))
a(cards([
 ('&#x1f501; 決まった手順を、正確にくり返したい', 'それは Power Automate。例：定期通知・転記・承認・ファイル整理など、手順が決まっている作業。', 'pa'),
 ('&#x1f5e3;&#xfe0f; 会話で質問に答えたい・判断させたい', 'それは Copilot Studio。例：社内FAQ・受付・問い合わせの一次対応など、会話や判断が必要なこと。', ''),
]))

a(NB)
a(H2('じつは、組み合わせて使える'))
a(P('そして大事なのは、<strong>「どちらか一方」ではない</strong>ということです。'))
a(P('Copilot Studio の中から、<strong>Power Automate の自動化（エージェント フロー）を呼び出せます</strong>。たとえば「会話で受け付け → 裏で申請フローを実行」のように、<strong>会話は Copilot Studio、定型処理は Power Automate</strong>、と役割分担できます。'))
a(note('&#x1f4a1; 使い分けのコツ','決まりきった作業は <strong>Power Automate</strong>、会話・判断が要る部分は <strong>Copilot Studio</strong>。<br>そして、必要なら<strong>2つを組み合わせる</strong>。これだけ押さえておけば、まず迷いません。'))

a(NB)
a(H2('まとめ'))
a(P('Power Automate と Copilot Studio の違いは、たったこれだけです。'))
a(ul(['<strong>Power Automate</strong>＝決めた手順をくり返す“作業ロボ”（きっかけは「何かが起きたとき」）',
      '<strong>Copilot Studio</strong>＝会話して自分で考える“受付係”（きっかけは「話しかけられたとき」）',
      '定型作業は PA、会話・判断は CS、で使い分ける',
      '<strong>Copilot Studio から Power Automate を呼べる</strong>ので、組み合わせもできる']))
a(P('新しいツールが出ると身構えてしまいますが、<strong>役割がちがうだけ</strong>と分かると、こわくありません。次は実際に、Copilot Studio で小さな AI を1つ作ってみると、感覚がつかめます。'))

a('\n\n<div class="mb-check"><p class="ck-ttl">&#x1f4cb; この記事で分かったこと</p>'
 + "".join(f'<label><input type="checkbox">{t}</label>' for t in [
   'Power Automate は“手順”で動く／Copilot Studio は“会話と判断”で動く',
   '定型作業のくり返しは <strong>Power Automate</strong>',
   '質問対応・案内・判断は <strong>Copilot Studio</strong>',
   'Copilot Studio のホームは「Agent」と「Workflow」の2つが入口',
   'Copilot Studio から Power Automate を呼んで<strong>組み合わせられる</strong>',
 ]) + '</div>')

a(NB)
a(H2('次回のPA45で、実際にさわってみませんか'))
a(P('PA45 では、こうした Power Automate や Copilot Studio の「45分でひとつ作る・試す」ハンズオンを、<strong>毎週木曜の夜にオンライン無料</strong>でやっています。一人で詰まりがちなところも、その場で質問しながら進められます。'))
a(cta_pa('&#x1f64c; まずは、さわってみるのがいちばん',
 'PA45は知識ゼロ・見るだけ参加も大歓迎です。次回もまた、ひとつ新しいものを一緒にさわります。お申し込みは下のボタンから（無料）。'))
a(P(f'なお、PA45 がどんな勉強会かは <a href="{PA45_URL}" target="_blank" rel="noopener">PA45の紹介ページ</a> にまとめています。<strong>PA45</strong> は、筆者が運営している「Power Automate を45分で学ぶ、無料のオンライン勉強会」です（毎週木曜の夜・初心者歓迎）。'))
a(cta_yt())

a('\n\n<p style="font-size:13px;color:#888;line-height:1.9;">※ 本記事は公開日時点の情報をもとに、筆者が実際に学んで試した内容を整理したものです。Power Automate・Copilot Studio の画面や仕様は更新されることがあるため、最新の状況は公式情報（Microsoft Learn）もあわせてご確認ください。画面の項目名・挙動は実機で確認しています。</p>')
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
print("status:",r.json()["status"]); print("EDIT =",f"{WP}/wp-admin/post.php?post={pid}&action=edit"); print("PREVIEW =",f"{WP}/?p={pid}&preview=true")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copilot Studio 初めてのエージェント記事（automate136ハウツー・.mb-*テイスト）。
- 元テンプレ = 2026-06-attachment-magic-box/build_article.py を Copilot Studio 用に組み替え。
- 実機スクショ（cs-vol-02/_material）を figure に使用。初心者が同じエージェントを作れる粒度。
- 読みやすさ：句点(。)ごとに改行／段落・囲みの余白を広げてメリハリ。
- WordPress に新規下書きを作成。status:draft固定（自動公開しない）。既存下書きがあればID上書き。"""
import base64, requests, pathlib, re, json, mimetypes

ROOT = pathlib.Path(__file__).resolve().parents[2]   # pa45/
HERE = pathlib.Path(__file__).resolve().parent
STATE = HERE / "post_state.json"                     # {"post_id":..,"media":{name:{"id":..,"url":..}}}

TITLE = "Copilot Studioで“質問に答えるAI”を作る｜はじめてのエージェントの作り方（2026年 新UI版）"
SLUG  = "copilot-studio-first-agent"
CAT   = 76  # Power Automate 実践・Tips（ツール系ハウツー）

YT_URL   = "https://www.youtube.com/@Haru_PowerAutomate136"
CP_URL   = "https://powerautomate-create.connpass.com/event/399555/"
PA45_URL = "https://www.automate136.com/pa45/"

# ---- 使う画像（ローカルの実機スクショ／スライド） ----
MAT = ROOT / "assets" / "x" / "html" / "cs-vol-02" / "_material"
IMG = {
    "concept": ROOT / "assets" / "x" / "html" / "cs-vol-02" / "csvol02.png",  # アイキャッチ＆概念図
    "home":    MAT / "new-home.png",
    "build":   MAT / "build-configured.png",
    "plan":    MAT / "preview-conv-1-plan.png",
    "answer":  MAT / "preview-conv-2-answer-top.png",
}

CSS = """
<style>
.mb-body > p{margin:1.9em 0!important;line-height:2.05!important;}
.mb-body > h2{margin-top:2.8em!important;}
.mb-body > h3{margin-top:2.4em!important;}
.mb-body > ul{margin:1.7em 0!important;line-height:2.0;}
.mb-body > ul li{margin:.55em 0;}
.mb-lead{line-height:2.1;}
.hl-marker{background:linear-gradient(transparent 58%,#e9d5ff 58%);font-weight:700;padding:0 .12em;border-radius:2px;}
.mb-fig{margin:40px 0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#e7e0f5;border:1px solid #d0c4ec;border-radius:16px;padding:18px 16px 12px;box-shadow:0 2px 8px rgba(76,29,149,.08);}
.mb-fig img{width:100%;max-width:860px;height:auto;display:block;margin:0 auto;background:#fff;border-radius:10px;box-shadow:0 4px 14px rgba(91,33,182,.16);}
.mb-fig svg{width:100%;max-width:760px;height:auto;display:block;margin:0 auto;background:#fff;border-radius:10px;padding:14px 10px;}
.mb-fig figcaption{font-size:.85em;color:#5b4a7a;margin-top:12px;}
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
.mb-step{background:#f7f4fd;border:2px solid #ddd0f2;border-radius:14px;padding:18px 22px 6px;margin:36px 0;}
.mb-step .st-ttl{display:flex;align-items:center;gap:12px;font-weight:800;color:#5b21b6;font-size:1.08em;margin-bottom:6px;}
.mb-step .st-no{flex:none;width:34px;height:34px;border-radius:50%;background:#7c3aed;color:#fff;display:flex;align-items:center;justify-content:center;font-size:1em;}
.mb-step ol{margin:6px 0 14px;padding-left:0;list-style:none;counter-reset:s;}
.mb-step ol li{position:relative;padding:8px 0 8px 30px;line-height:1.8;border-top:1px solid #ece4f9;}
.mb-step ol li:first-child{border-top:none;}
.mb-step ol li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:8px;width:22px;height:22px;background:#ede9fe;color:#5b21b6;border-radius:50%;font-size:.78em;font-weight:800;display:flex;align-items:center;justify-content:center;}
.mb-point{background:#f7f4fd;border-left:6px solid #8b5cf6;border-radius:8px;padding:18px 24px;margin:36px 0;line-height:2.1;}
.mb-note{background:#fffdf5;border:2px solid #ffd54f;border-radius:12px;padding:18px 24px;margin:38px 0;line-height:2.1;}
.mb-note .nt-ttl{font-weight:700;color:#e8920c;margin:0 0 14px;}
.mb-warn{background:#fff6f6;border-left:6px solid #e57373;border-radius:8px;padding:18px 24px;margin:36px 0;line-height:2.1;}
.mb-copy{background:#faf7ff;border:1px dashed #c4b5fd;border-radius:10px;padding:16px 18px;margin:22px 0;line-height:1.95;color:#3b2a5a;font-size:.96em;}
.mb-copy .cp-ttl{font-weight:700;color:#6d28d9;font-size:.85em;margin-bottom:8px;letter-spacing:.03em;}
.mb-code{background:#1e1533;color:#e9e2f7;font-family:Consolas,'DM Mono',monospace;font-size:.92em;line-height:1.6;padding:14px 18px;border-radius:10px;margin:18px 0;overflow-x:auto;white-space:pre-wrap;word-break:break-all;}
.mb-check{border:1px solid #ddd0f2;border-radius:14px;padding:22px 26px;background:#fff;margin:40px 0;}
.mb-check .ck-ttl{margin:0 0 14px;font-weight:800;font-size:1.05em;color:#5b21b6;}
.mb-check label{display:flex;align-items:flex-start;gap:10px;line-height:1.7;font-size:1em;margin:10px 0;}
.mb-check input{margin-top:4px;width:16px;height:16px;accent-color:#7c3aed;flex-shrink:0;}
.speech-balloon{line-height:1.95;}
.mb-intro{background:#f6f4fb;border:1px solid #e0d7f3;border-left:5px solid #a78bda;border-radius:10px;padding:13px 18px;margin:4px 0 30px;font-size:.9em;color:#5b4a7a;line-height:1.8;}
/* --- スクリーンショット枠（テキストとはっきり区別・グレー台紙＋タグ＋影） --- */
.mb-shot{margin:56px 0;background:#eceef2;border:1px solid #d9dce3;border-radius:16px;padding:16px 16px 13px;box-shadow:0 3px 12px rgba(15,23,42,.09);}
.mb-shot .sh-tag{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:800;color:#475569;background:#dde1e9;border-radius:999px;padding:5px 14px;margin-bottom:12px;letter-spacing:.02em;}
.mb-shot .sh-frame{position:relative;line-height:0;}
.mb-shot .sh-frame img{width:100%;height:auto;display:block;border-radius:10px;border:1px solid #c7cad3;box-shadow:0 6px 18px rgba(15,23,42,.20);}
.mb-shot figcaption{font-size:1.02em;color:#5b4a7a;margin-top:14px;line-height:1.8;}
/* 赤い角丸・影つきの注目マーカー（見るべき場所を囲む） */
.mb-anno{position:absolute;border:3px solid #e0342f;border-radius:12px;background:rgba(224,52,47,.04);box-shadow:0 5px 14px rgba(224,52,47,.40),0 0 0 4px rgba(224,52,47,.10);}
.mb-anno .an-lb{position:absolute;top:-16px;left:-4px;background:linear-gradient(180deg,#f5504b,#df332e);color:#fff;font-size:12.5px;font-weight:800;line-height:1.4;padding:3px 10px;border-radius:7px;white-space:nowrap;box-shadow:0 3px 7px rgba(0,0,0,.32);}
/* 図解カード（文章の羅列を視覚化） */
.mb-cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:30px 0;}
.mb-cards .cd{background:#fff;border:1px solid #e4dbf6;border-left:5px solid #8b5cf6;border-radius:12px;padding:15px 17px;box-shadow:0 2px 8px rgba(76,29,149,.07);}
.mb-cards .cd .cd-t{display:block;color:#5b21b6;font-weight:800;font-size:1.02em;margin-bottom:6px;}
.mb-cards .cd .cd-d{font-size:.9em;color:#4b5563;line-height:1.65;}
@media(max-width:600px){.mb-cards{grid-template-columns:1fr;}}
.cs-preface{background:#eef7f1;border:1px solid #cfe8db;border-left:5px solid #5f8a6e;border-radius:10px;padding:14px 18px;margin:0 0 26px;font-size:.86em;color:#3d5647;line-height:1.85;}
.cs-preface b{color:#2f6b4f;}
.cs-preface a{color:#1d4ed8;font-weight:700;}
</style>
"""

def jp(t):
    return re.sub(r'。(?![」）】、\s<]|$)', '。<br>', t)

def bubble(text):
    return ('\n\n<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">'
            '<div class="speech-person"><figure class="speech-icon">'
            '<img class="speech-icon-image" src="https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png" alt="" width="1024" height="1024" /></figure></div>'
            f'<div class="speech-balloon">{jp(text)}</div></div>')

def fig(src, caption, alt=""):
    return f'\n\n<figure class="mb-fig"><img src="{src}" alt="{alt}" /><figcaption>{caption}</figcaption></figure>'

def fig_svg(svg, caption):
    return f'\n\n<figure class="mb-fig">{svg}<figcaption>{caption}</figcaption></figure>'

def shot(src, caption, alt="", annos=None):
    """実機スクショ。グレー台紙＋『実際の画面』タグ＋赤い注目マーカーで、本文と明確に区別する。
    annos=[(left%,top%,width%,height%,label), ...]（画像に対する割合で赤枠を重ねる）"""
    ov="".join(
        f'<div class="mb-anno" style="left:{l}%;top:{t}%;width:{w}%;height:{h}%;">'
        f'<span class="an-lb">{lb}</span></div>' for (l,t,w,h,lb) in (annos or []))
    return (f'\n\n<figure class="mb-shot"><span class="sh-tag">&#x1f5a5;&#xfe0f; 実際の画面</span>'
            f'<div class="sh-frame"><img src="{src}" alt="{alt}" />{ov}</div>'
            f'<figcaption>{caption}</figcaption></figure>')

def cards(items):
    """図解カード（title, desc の2要素を並べて視覚化）"""
    cs="".join(f'<div class="cd"><span class="cd-t">{t}</span><span class="cd-d">{jp(d)}</span></div>' for t,d in items)
    return f'\n\n<div class="mb-cards">{cs}</div>'

def step(no, ttl, ol_items):
    lis = "".join(f"<li>{jp(t)}</li>" for t in ol_items)
    return (f'\n\n<div class="mb-step"><div class="st-ttl"><span class="st-no">{no}</span>{ttl}</div>'
            f'<ol>{lis}</ol></div>')

def mcap(t):
    return f'\n\n<div style="text-align:center;font-size:.82em;color:#5b4a7a;margin:-14px 0 8px;">{t}</div>'

P=lambda t:f"\n\n<p>{jp(t)}</p>"
PL=lambda t:f'\n\n<p class="mb-lead">{jp(t)}</p>'
H2=lambda t:f"\n\n<h2>{t}</h2>"
H3=lambda t:f"\n\n<h3>{t}</h3>"
NB="\n\n&nbsp;"
def ul(items): return "\n\n<ul>"+"".join(f"\n<li>{jp(i)}</li>" for i in items)+"\n</ul>"
def warn(t): return f'\n\n<div class="mb-warn">{jp(t)}</div>'
def point(t): return f'\n\n<div class="mb-point">{jp(t)}</div>'
def note(ttl,t): return f'\n\n<div class="mb-note"><p class="nt-ttl">{ttl}</p>{jp(t)}</div>'
def copybox(ttl, lines):
    body="<br>".join(lines)
    return f'\n\n<div class="mb-copy"><div class="cp-ttl">{ttl}</div>{body}</div>'

def cta_yt():
    return ('\n\n<div class="mb-cta yt"><p class="cta-ttl">&#x25b6; 動きは動画で見るのが早いです</p>'
            '<p>エージェントの作り方や実演は、PA45の各回をYouTubeにアーカイブしています。</p>'
            f'<a class="mb-btn yt" href="{YT_URL}" target="_blank" rel="noopener">PA45のYouTubeチャンネルを見る</a></div>')

def cta_pa(ttl, body):
    return (f'\n\n<div class="mb-cta pa"><p class="cta-ttl">{ttl}</p><p>{jp(body)}</p>'
            f'<a class="mb-btn pa" href="{CP_URL}" target="_blank" rel="noopener">次回のPA45に申し込む（無料）</a>'
            '<span class="cta-sub">毎週木曜の夜・オンライン・参加無料／途中入退室OK・見るだけ参加も歓迎です</span></div>')

# ================= WP接続 =================
env={}
for line in (ROOT/".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1); env[k.strip()]=v.strip()
WP=env["WP_URL"].rstrip("/")
auth=base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
H={"Authorization":f"Basic {auth}"}

state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"post_id":None,"media":{}}

def upload(key):
    """ローカル画像をWPメディアへ（一度上げたらstateにキャッシュ）。返り値=URL"""
    if key in state["media"]:
        return state["media"][key]["url"]
    p = IMG[key]
    if not p.exists():
        print("WARN: image not found:", p); return ""
    fn = f"cs-first-agent-{key}.png"
    mh = dict(H); mh["Content-Disposition"]=f'attachment; filename="{fn}"'; mh["Content-Type"]="image/png"
    r = requests.post(f"{WP}/wp-json/wp/v2/media", headers=mh, data=p.read_bytes(), timeout=180)
    r.raise_for_status(); j=r.json()
    state["media"][key]={"id":j["id"],"url":j["source_url"]}
    print(f"uploaded {key} -> media {j['id']}")
    return j["source_url"]

U = {k: upload(k) for k in IMG}
STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")

# ================= 本文 =================
H_=[]; a=H_.append
a('<div class="cs-preface">📝 実際に <b>Copilot Studio を触って検証</b>し、スクショを撮りながら気づいたことをまとめた記録です。<br>機能・画面・料金は更新が続きます。<br>最新の正確な情報は <a href="https://learn.microsoft.com/ja-jp/microsoft-copilot-studio/" target="_blank" rel="noopener">Microsoft 公式（Microsoft Learn）</a> をご確認ください。</div>')

a('\n\n<div class="mb-intro">この記事は、筆者が実際に Copilot Studio でエージェントを作りながら、気になったポイントを AI と壁打ち（相談）しつつまとめた記録です。<br>「初めての人が、読みながら同じものを作れる」ことを目指して書いています。</div>')

a(PL('Copilot Studio を使って、<span class="hl-marker">よくある質問に日本語で答えてくれる AI（エージェント）</span>を作ります。プログラミングは不要で、やることは「どんな役割か」を文章で書くだけです。'))
a(PL('2026年に画面が新しくなってから触ってみると、以前は必要だった<strong>「トピック（会話の分岐）を自分で設計する」作業がなくなっていました</strong>。ゴールを指示文で渡せば、あとの段取りは AI が自分で組んでくれます。'))
a(PL('Power Automate が「決めた手順をそのままくり返す」自動化なら、Copilot Studio は「会話して自分で考えて動く」AI です。<strong>Copilot Studio を初めて触る人でも、画面のどこを押すかまで分かるように</strong>、手順をひとつずつ書いていきます。'))

a(fig(U["concept"], "▲ このあと作る「AI受付」のイメージ。台本（トピック）は書かず、指示文と道具を渡すだけ", "Copilot Studioの新オーケストレーターの概念図"))

a(NB)
a(H2('今回つくるもの ── “勉強会の受付AI”'))
a(note('&#x1f4a1; 「PA45」とは？','この記事に出てくる <strong>PA45</strong> は、筆者が運営している<strong>「Power Automate を45分で学ぶ、無料のオンライン勉強会」</strong>です（毎週木曜の夜・初心者歓迎）。今回はこの勉強会を題材に、その“受付AI”を作っていきます。題材はご自分の身近なもの（社内のFAQなど）に置きかえてOKです。'))
a(P('題材として、「PA45 という勉強会について、参加希望者の質問に答える受付 AI」を作ります。<strong>「どんな会？」「初心者でも大丈夫？」「準備するものは？」</strong>といった質問に、まとめて答えてくれる状態がゴールです。'))
a(P('できあがると、下のように<strong>1回の質問の中に3つ聞かれても、AI が自分で問いを分解して順番に答えて</strong>くれます。この「段取りを自分で組む」部分が、新しい Copilot Studio の一番のポイントです。'))
a(shot(U["answer"], "▲ 完成後のイメージ。3つの質問に、見出し・表・出典つきで整理して回答してくれる", "Copilot Studioエージェントが質問に整理して回答している画面",
   annos=[(4.5,40,86,15,"見出しに整理＋出典①つき")]))

a(bubble('ひとつだけ正直に。指示文だけでも“それっぽく”は答えますが、<strong>社内の正確な情報を答えさせたいなら、あとで「ナレッジ」に社内文書（SharePoint など）を足すのが本命</strong>です&#x1f60a; まずは今回、"動く最小構成"を作ってしまいましょう。'))

a(NB)
a(H2('用意するもの'))
a(P('特別な準備はいりません。会社や学校の Microsoft 365 アカウントがあれば始められます。'))
a(ul(['<strong>Microsoft 365 のアカウント</strong>（会社・学校のもの）',
      '<strong>Copilot Studio が使える状態</strong>（試用版、またはライセンス）',
      'ブラウザ（Edge や Chrome）']))
a(note('&#x1f4a1; はじめる前に（お金の話）','Copilot Studio は、エージェントとのやり取りに<strong>メッセージ課金（ライセンス）</strong>がかかります。まずは<strong>試用版やデモ環境で触ってみる</strong>のが安心です。会社で使えるかどうかは、情報システム部門に確認しておくと確実です。'))

a(NB)
a(H2('はじめに：Copilot Studio を開く'))
a(P('「そもそもどこから入るの？」という方へ。Copilot Studio は、ふだん使っている<strong>会社（や学校）の Microsoft アカウント</strong>でそのまま入れます。'))
a(step('&#x1f511;','サインインして新しい画面にする',[
 'ブラウザで <code>copilotstudio.microsoft.com</code> を開く',
 '<strong>会社・学校のメールアドレス</strong>でサインインする（多要素認証が出たら、いつものスマホ承認でOK）',
 '画面が出たら、右上や左下の<strong>環境名</strong>が、使いたい環境になっているか確認する',
 '「新しい Copilot Studio エクスペリエンス」の案内が出たら <strong>「Try it now!（今すぐ試す）」</strong> を押す（右上の <strong>「New experience」トグル</strong>でいつでも新旧を切り替えられます）',
]))
a(shot(U["home"], "▲ サインイン後の新しいホーム。「Agent（エージェント）」のカードから作りはじめる", "Copilot Studioの新しいホーム画面",
   annos=[(27.5,33.5,31.5,37,"① ここをクリック"),(85,2.3,12.7,5,"新旧の切替")]))
a(note('&#x26a0;&#xfe0f; 画面が英語で出ます','2026年時点では、新しい画面は<strong>英語表示</strong>です。この記事では、どのボタンかを日本語で補足しながら進めます。慣れると英語のままでも迷いません。'))

a(NB)
a(H2('作るものの全体像'))
a(P('やることは、たった3つです。<strong>①名前と指示文を書く → ②（必要なら）道具を足す → ③テストする</strong>。難しい設定はありません。'))
a(fig_svg(
'<svg viewBox="0 0 720 178" font-family="\'Noto Sans JP\',sans-serif">'
'<marker id="ah" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0 0l6 3-6 3z" fill="#a78bda"/></marker>'
'<rect x="20" y="40" width="190" height="98" rx="14" fill="#F5F3FF" stroke="#7C3AED" stroke-width="2"/>'
'<text x="115" y="84" text-anchor="middle" font-size="16" font-weight="700" fill="#5B21B6">① 指示文を書く</text>'
'<text x="115" y="113" text-anchor="middle" font-size="13" font-weight="700" fill="#6D28D9">役割を文章で</text>'
'<path d="M216 89 H256" stroke="#a78bda" stroke-width="3" marker-end="url(#ah)"/>'
'<rect x="263" y="40" width="190" height="98" rx="14" fill="#FDF4FF" stroke="#C026D3" stroke-width="2"/>'
'<text x="358" y="84" text-anchor="middle" font-size="16" font-weight="700" fill="#86198F">② 道具を足す</text>'
'<text x="358" y="113" text-anchor="middle" font-size="12.5" font-weight="700" fill="#A21CAF">今回は既定でOK</text>'
'<path d="M459 89 H499" stroke="#a78bda" stroke-width="3" marker-end="url(#ah)"/>'
'<rect x="506" y="40" width="190" height="98" rx="14" fill="#FDF2F8" stroke="#EC4899" stroke-width="2"/>'
'<text x="601" y="84" text-anchor="middle" font-size="16" font-weight="700" fill="#9D174D">③ テストする</text>'
'<text x="601" y="113" text-anchor="middle" font-size="13" font-weight="700" fill="#BE185D">Preview で会話</text>'
'</svg>',
"▲ 作る流れは3ステップ。指示文を書いて、テストするだけ"))

a(NB)
a(H2('ステップ0：新しいエージェントを作りはじめる'))
a(P('まずは入れ物（エージェント）を用意します。'))
a(step('0','エージェントを新規作成する',[
 'ホーム画面で、右上の <strong>「New experience」</strong> がオン（新しい画面）になっていることを確認',
 '<strong>「Agent（エージェント）」</strong> のカードをクリック',
 '少し待つと、エージェントの<strong>作成画面（Build）</strong>が開く',
]))
a(point('もし「何を構築しますか?」と聞かれて<strong>入力ボックスが出る場合</strong>は、そこに作りたいことを文章で書いて送ると、AI が骨組みを作ってくれます。今回は<strong>自分で指示文を書く方法</strong>で進めるので、そのまま作成画面へ進んでOKです。'))

a(NB)
a(H2('作り方（実画面つき）'))

a(H3('ステップ①：名前と指示文を書く（ここが本体）'))
a(P('作成画面が開いたら、まず<strong>名前</strong>を付けて、<strong>Instructions（指示文）</strong>を書きます。この指示文が、エージェントの“性格”と“仕事内容”そのものになります。'))
a(step('1','名前と指示文を入れる',[
 '画面上部の名前欄（最初は「Untitled Agent」）をクリックして、<strong>「PA45受付エージェント」</strong> など分かる名前を入れる',
 '中央の <strong>「Instructions」</strong> の入力欄をクリック',
 '下の例文をそのまま貼り付ける（内容は自分の用途に合わせて書き換えOK）',
]))
a(copybox('&#x1f4dd; 指示文の例（コピーして使えます）', [
 'あなたは「PA45」という Power Automate 勉強会の受付エージェントです。',
 '参加者からの質問に日本語で丁寧に答えます。',
 'PA45 は毎月開催・参加無料・初心者歓迎のオンライン勉強会です。',
 'わからないことは正直に「わからない」と答え、推測で断言しません。',
]))
a(shot(U["build"], "▲ 名前と指示文を入れた状態。右側のパネルにモデルや道具（Skills / Tools / ナレッジ）が並ぶ", "Copilot Studioで指示文を入力したエージェント作成画面",
   annos=[(5.3,29.5,35,15,"① ここに指示文"),(84.8,11,14,7,"頭脳＝AIモデル")]))
a(point('指示文を書くときのコツは、<span class="hl-marker">この4つの要素を入れる</span>ことです。むずかしく考えず、下の4つを1〜2行ずつ書けば十分です。'))
a(cards([
 ('&#x1f464; 役割', 'どんな立場の誰か。例：「PA45という勉強会の受付担当」'),
 ('&#x1f4ac; 口調', 'どんな話し方か。例：「日本語で丁寧に」「初心者にやさしく」'),
 ('&#x1f3af; 答える範囲', '何について答えるか。例：「PA45の参加に関する質問」'),
 ('&#x1f91a; わからない時', '知らないことへの対応。例：「推測で断言せず、正直に答える」'),
]))
a(P('とくに最後の<strong>「わからないことは断言しない」</strong>の一文を入れておくと、AI が知ったかぶりの回答をしにくくなります。'))
a(note('&#x1f4a1; 右上の「Model」に注目','作成画面の右パネル上部に <strong>「Model」</strong> という欄があります。ここが今の“頭脳”にあたる AI モデルで、<strong>初期状態でも十分に賢いモデル</strong>が選ばれています。こだわりがなければ、そのままでOKです。'))

a(H3('ステップ②：道具（ナレッジ・ツール）は必要なら足す'))
a(P('右側のパネルには、エージェントに持たせる“道具”が並んでいます。今回は<strong>最小構成なので、基本はさわらなくて大丈夫</strong>です。何があるかだけ、かるく知っておきましょう。'))
a(cards([
 ('&#x1f310; Knowledge（ナレッジ）', '答えの根拠になる情報源。最初から「Search all websites（Web検索）」が入っていて、一般的な質問には Web を調べて答えられます。'),
 ('&#x1f527; Tools（ツール）', '外部のシステムやアクションにつなぐ道具。メール送信や予定登録などをさせたいときに足します。'),
 ('&#x2699;&#xfe0f; Skills / Connected agents', 'ふるまいを細かく定義したり、別のエージェントと連携させたりする、少し進んだ機能です。'),
 ('&#x1f9e0; Model（モデル）', 'エージェントの“頭脳”にあたる AI。初期状態でも十分に賢いので、こだわりがなければそのままでOK。'),
]))
a(note('&#x1f4a1; 社内の正確な回答をさせたいときは','「Web ではなく、うちの社内資料に基づいて答えてほしい」という場合は、<strong>Knowledge に SharePoint やファイルを追加</strong>します。すると、その資料を根拠に、出典つきで答えてくれるようになります（この応用は記事の最後でふれます）。'))

a(H3('ステップ③：保存する'))
a(P('指示文を書いたら保存します。'))
a(step('3','保存する',[
 '画面右上の <strong>保存アイコン</strong>（フロッピーのマーク）をクリック',
 '数秒で保存が完了する（これでいつでもテストできる状態になります）',
]))

a(NB)
a(H2('動かしてみる（Preview でテスト）'))
a(P('作ったら、本当に答えてくれるか確かめます。ここが一番おもしろいところです。'))
a(step('&#x2713;','テストして確認する',[
 '画面上部のタブを <strong>「Build」から「Preview」</strong> に切り替える',
 '右側にチャット画面が出るので、下の入力欄に質問を打ち込む',
 'たとえば <strong>「初参加を考えています。PA45 がどんな会か教えて。あと、まったく触ったことがなくても大丈夫か、準備することも合わせて教えて」</strong> と、まとめて3つ聞いてみる',
 '送信して、答えが返ってくるのを待つ',
]))
a(P('すると、答えを返す前に、<strong>「ユーザーは3つのことを聞いている…」と AI が自分で考え、ナレッジを検索し、順番を組み立てている様子</strong>が画面に出ました。トピック（会話の分岐）を1つも作っていないのに、です。'))
a(shot(U["plan"], "▲ 回答の前に、AI が質問を分解して「何を調べるか」を自分で段取りしている（Searched knowledge の表示）", "Copilot Studioが回答前に段取りを組んでいる様子",
   annos=[(7.5,67,84,31,"AIが自分で段取り中")]))
a(point('この<span class="hl-marker">「質問を分解 → 調べる → 順番に答える」を自動でやってくれる仕組み</span>が、新しい Copilot Studio の“新オーケストレーター”だと分かってきました。昔のように会話の分岐を手で用意しなくても、指示文とゴールだけで複雑な質問に対応できました。'))

a(NB)
a(H2('つまずきポイント（先に知っておくと安心）'))
a(ul(['<strong>最初のあいさつが英語で出る</strong> → 指示文に「日本語で」と書いても、最初の定型あいさつは英語のことがあります。<strong>こちらが日本語で質問すれば、回答は日本語で返ります</strong>。気になる場合は、会話の開始メッセージを別途設定できます。',
      '<strong>指示文にないことを聞くと、一般論やWeb検索の結果を答える</strong> → 今回はナレッジが Web 検索だけなので、社内固有の情報は正確に答えられないことがあります。正確さが必要なら、次の「応用」でナレッジを足します。',
      '<strong>作成画面が重い・固まる</strong> → 新しい画面は動作が重いことがあります。うまく表示されないときは、いちど画面を再読み込みするか、少し待ってから操作してください。']))

a(H3('応用：社内の資料に基づいて答えさせる（次の一歩）'))
a(P('「うちの規程や手順書に沿って答えてほしい」という場合は、ナレッジを足します。'))
a(ul(['右パネルの <strong>「Knowledge」</strong> の <strong>＋</strong> をクリック',
      '<strong>SharePoint・ファイル・Web サイト</strong>などから、根拠にしたい資料を追加',
      'すると、その資料を検索して、<strong>出典（どのページから答えたか）つき</strong>で回答してくれるようになります']))
a(P('ここまでできると、「社内 FAQ に自動で答える AI」に一気に近づきます。今回はその<strong>土台となる最小構成</strong>を作った、というわけです。'))

a(NB)
a(H2('まとめ'))
a(P('やったことは、<strong>名前と指示文を書いて、テストしただけ</strong>です。'))
a(ul(['<strong>①</strong> 名前と指示文（役割・口調・範囲・わからない時の対応）を書く',
      '<strong>②</strong> 道具（ナレッジ・ツール）は、今回は既定のままでOK',
      '<strong>③</strong> Preview で会話して、AI が段取りを組んで答えるのを確認する']))
a(P('会話の分岐を1つも設計していないのに、まとめて聞かれた質問にちゃんと答えてくれました。<strong>「作りたいことを文章で書くだけ」</strong>で AI が動く。これが今の Copilot Studio の手ざわりです。最初の1体を作るテーマとして、ちょうどいいと思います。'))

a('\n\n<div class="mb-check"><p class="ck-ttl">&#x1f4cb; この記事で学んだこと</p>'
 + "".join(f'<label><input type="checkbox">{t}</label>' for t in [
   'Copilot Studio は <code>copilotstudio.microsoft.com</code> から、会社アカウントで入る',
   '新しい画面は右上の <strong>「New experience」トグル</strong>で切り替えられる',
   'エージェントは<strong>指示文（役割・口調・範囲・わからない時の対応）を書くだけ</strong>で作れる',
   'トピック（会話の分岐）を作らなくても、AI が質問を分解して順に答える',
   '社内の正確な回答をさせたいときは <strong>ナレッジに SharePoint やファイルを足す</strong>',
 ]) + '</div>')

a(NB)
a(H2('次回のPA45で、続きを一緒に作りませんか'))
a(P('PA45 では、こうした「45分でひとつ作る」ハンズオンを、<strong>毎週木曜の夜にオンライン無料</strong>でやっています。一人で詰まりがちなところも、その場で質問しながら進められます。'))
a(cta_pa('&#x1f64c; こういうのを、毎週みんなで作っています',
 'PA45は知識ゼロ・見るだけ参加も大歓迎です。次回もまた、ひとつ新しいものを一緒に作ります。お申し込みは下のボタンから（無料）。'))
a(P(f'過去回のまとめや、PA45がどんな勉強会かは <a href="{PA45_URL}" target="_blank" rel="noopener">PA45の紹介ページ</a> にまとめています。また次回、一緒に「できた！」を作りましょう。'))
a(cta_yt())

a('\n\n<p style="font-size:13px;color:#888;line-height:1.9;">※ 本記事は公開日時点の情報をもとに、筆者が実際に学んで試した内容を整理しました。Copilot Studio の画面や仕様は更新されることがあるため、最新の状況は公式情報（Microsoft Learn）もあわせてご確認ください。画面の項目名・挙動は実機（Copilot Studio）で確認しています。</p>')
a('\n\n<p style="font-size:13px;color:#888;line-height:1.9;">※ 本記事の構成や図解の一部は、AI と壁打ちしながら作成しています。</p>')

content=CSS+'\n\n<div class="mb-body">'+"".join(H_)+'\n\n</div>'
(HERE/"article.html").write_text(content,encoding="utf-8")
print("article.html:",len(content),"chars")

# ================= WP 下書き作成/更新 =================
payload={"title":TITLE,"slug":SLUG,"status":"draft","content":content,"categories":[CAT]}
if state["media"].get("concept"):
    payload["featured_media"]=state["media"]["concept"]["id"]

if state.get("post_id"):
    r=requests.post(f"{WP}/wp-json/wp/v2/posts/{state['post_id']}",headers=H,json=payload,timeout=120)
    r.raise_for_status(); pid=state["post_id"]; print("UPDATED",pid)
else:
    r=requests.post(f"{WP}/wp-json/wp/v2/posts",headers=H,json=payload,timeout=120)
    r.raise_for_status(); pid=r.json()["id"]; state["post_id"]=pid; print("CREATED",pid)

STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")
print("status:",r.json()["status"])
print("EDIT    =",f"{WP}/wp-admin/post.php?post={pid}&action=edit")
print("PREVIEW =",f"{WP}/?p={pid}&preview=true")

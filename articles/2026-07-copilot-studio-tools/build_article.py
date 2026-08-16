#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Copilot Studio ツール（AIに手を持たせる）記事｜automate136ハウツー・.mb-*テイスト。
- 元テンプレ = 2026-07-copilot-studio-first-agent/build_article.py を踏襲。
- 画面は HTML/CSS モックで再現（生スクショの写り込み回避／実機で確認済みのUIに基づく）。
- 読みやすさ：句点(。)ごとに改行／段落・囲みの余白を広げてメリハリ。
- 既定 = article.html をローカル生成のみ。WordPress 下書き作成は `python build_article.py --push`。"""
import base64, requests, pathlib, re, json, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]   # pa45/
HERE = pathlib.Path(__file__).resolve().parent
STATE = HERE / "post_state.json"

TITLE = "Copilot Studioで“AIに手を持たせる”｜メールを送るツールの付け方（2026年 新UI版）"
SLUG  = "copilot-studio-tools"
CAT   = 76  # Power Automate 実践・Tips

YT_URL   = "https://www.youtube.com/@Haru_PowerAutomate136"
CP_URL   = "https://powerautomate-create.connpass.com/event/399555/"
PA45_URL = "https://www.automate136.com/pa45/"

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
.mb-check{border:1px solid #ddd0f2;border-radius:14px;padding:22px 26px;background:#fff;margin:40px 0;}
.mb-check .ck-ttl{margin:0 0 14px;font-weight:800;font-size:1.05em;color:#5b21b6;}
.mb-check label{display:flex;align-items:flex-start;gap:10px;line-height:1.7;font-size:1em;margin:10px 0;}
.mb-check input{margin-top:4px;width:16px;height:16px;accent-color:#7c3aed;flex-shrink:0;}
.speech-balloon{line-height:1.95;}
.mb-intro{background:#f6f4fb;border:1px solid #e0d7f3;border-left:5px solid #a78bda;border-radius:10px;padding:13px 18px;margin:4px 0 30px;font-size:.9em;color:#5b4a7a;line-height:1.8;}
.mb-cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:30px 0;}
.mb-cards .cd{background:#fff;border:1px solid #e4dbf6;border-left:5px solid #8b5cf6;border-radius:12px;padding:15px 17px;box-shadow:0 2px 8px rgba(76,29,149,.07);}
.mb-cards .cd .cd-t{display:block;color:#5b21b6;font-weight:800;font-size:1.02em;margin-bottom:6px;}
.mb-cards .cd .cd-d{font-size:.9em;color:#4b5563;line-height:1.65;}
@media(max-width:600px){.mb-cards{grid-template-columns:1fr;}}
/* ---- 画面モック（Segoe UI・実画面を清書して再現）---- */
.mb-mock{margin:50px 0;background:#eceef2;border:1px solid #d9dce3;border-radius:16px;padding:16px 16px 13px;box-shadow:0 3px 12px rgba(15,23,42,.09);}
.mb-mock .mk-tag{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;font-weight:800;color:#475569;background:#dde1e9;border-radius:999px;padding:5px 14px;margin-bottom:12px;}
.mb-mock figcaption{font-size:.85em;color:#5b4a7a;margin-top:14px;line-height:1.65;}
.uiwin{font-family:'Segoe UI','Yu Gothic UI',sans-serif;background:#fff;border:1px solid #c7cad3;border-radius:10px;box-shadow:0 6px 18px rgba(15,23,42,.18);overflow:hidden;position:relative;}
.ui-dtitle{font-weight:700;font-size:15px;color:#242424;padding:14px 18px 6px;}
.ui-dsub{font-size:12.5px;color:#616161;padding:0 18px 12px;border-bottom:1px solid #ededed;}
.ui-tabs{display:flex;gap:8px;flex-wrap:wrap;padding:12px 18px 4px;}
.ui-tab{font-size:12.5px;font-weight:700;color:#424242;background:#f3f2f1;border-radius:999px;padding:5px 13px;}
.ui-tab.on{color:#5b21b6;background:#ede9fe;border:1px solid #cbb7f2;}
.ui-conns{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:14px 18px 18px;}
@media(max-width:560px){.ui-conns{grid-template-columns:1fr;}}
.ui-conn{display:flex;align-items:center;gap:11px;border:1px solid #e1dfdd;border-radius:8px;padding:11px 13px;font-size:13.5px;font-weight:600;color:#242424;background:#fff;}
.ui-conn .ci{width:26px;height:26px;border-radius:6px;flex:none;display:flex;align-items:center;justify-content:center;font-size:14px;color:#fff;font-weight:800;}
.ui-conn .cp{margin-left:auto;color:#8a8886;font-weight:800;}
.ui-conn.pick{border:2px solid #e0342f;box-shadow:0 4px 12px rgba(224,52,47,.22);}
.ui-perm{border:1px solid #e1dfdd;border-radius:10px;padding:18px 20px;margin:6px 0;background:#fff;}
.ui-perm .pt{font-weight:800;font-size:15px;color:#242424;margin-bottom:8px;}
.ui-perm .pb{font-size:13px;color:#424242;line-height:1.7;}
.ui-perm .pb b{color:#5b21b6;}
.ui-perm .pbtns{display:flex;gap:10px;margin-top:14px;}
.ui-btn-primary{background:#5b21b6;color:#fff;font-weight:700;font-size:13px;border-radius:6px;padding:8px 22px;}
.ui-btn-ghost{background:#fff;color:#242424;font-weight:700;font-size:13px;border:1px solid #c7cad3;border-radius:6px;padding:8px 22px;}
.ui-toolrow{display:flex;align-items:center;gap:11px;border:1px solid #e1dfdd;border-radius:8px;padding:12px 14px;font-size:14px;font-weight:600;color:#242424;background:#fafafa;}
.ui-mail{border:1px solid #e1dfdd;border-radius:10px;overflow:hidden;background:#fff;}
.ui-mail .mh{background:#faf9f8;border-bottom:1px solid #ededed;padding:12px 18px;}
.ui-mail .msub{font-weight:800;font-size:15px;color:#242424;}
.ui-mail .mmeta{font-size:12px;color:#616161;margin-top:3px;}
.ui-mail .mbody{padding:16px 18px;font-size:13.5px;color:#323130;line-height:1.9;}
.ui-mail .mbody .mline-hi{background:#fff3bf;font-weight:700;border-radius:3px;padding:0 2px;}
.redbox{border:3px solid #e0342f;border-radius:10px;padding:1px;position:relative;}
.redbox .rl{position:absolute;top:-15px;left:-3px;background:linear-gradient(180deg,#f5504b,#df332e);color:#fff;font-size:12px;font-weight:800;padding:2px 10px;border-radius:7px;white-space:nowrap;box-shadow:0 3px 7px rgba(0,0,0,.3);}
.cs-preface{background:#eef7f1;border:1px solid #cfe8db;border-left:5px solid #5f8a6e;border-radius:10px;padding:14px 18px;margin:0 0 26px;font-size:.86em;color:#3d5647;line-height:1.85;}
.cs-preface b{color:#2f6b4f;}
.cs-preface a{color:#1d4ed8;font-weight:700;}
.csflow-w{margin:30px 0;padding:20px 18px 18px;background:#faf8ff;border:1px solid #e6ddf7;border-radius:14px;}
.csflow-t{font-size:.92em;font-weight:800;color:#5B21B6;margin:0 0 15px;text-align:center;}
.csflow{display:flex;flex-wrap:wrap;align-items:stretch;justify-content:center;gap:9px;}
.csflow .stp{flex:1 1 140px;min-width:120px;background:#fff;border:2px solid #ddd0f2;border-radius:12px;padding:13px 11px;text-align:center;}
.csflow .stp .sn{display:inline-block;font-size:.76em;font-weight:800;color:#fff;background:#7C3AED;border-radius:999px;padding:2px 10px;margin-bottom:8px;}
.csflow .stp .st{font-size:.9em;font-weight:700;color:#2b2540;line-height:1.55;}
.csflow .ar{align-self:center;color:#a78bda;font-weight:900;font-size:1.3em;}
</style>
"""

def jp(t): return re.sub(r'。(?![」）】、\s<]|$)', '。<br>', t)
def bubble(text):
    return ('\n\n<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">'
            '<div class="speech-person"><figure class="speech-icon">'
            '<img class="speech-icon-image" src="https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png" alt="" width="1024" height="1024" /></figure></div>'
            f'<div class="speech-balloon">{jp(text)}</div></div>')
def fig_svg(svg, caption): return f'\n\n<figure class="mb-fig">{svg}<figcaption>{caption}</figcaption></figure>'
def mock(inner, caption):
    return (f'\n\n<figure class="mb-mock"><span class="mk-tag">&#x1f5a5;&#xfe0f; 実際の画面（清書して再現）</span>'
            f'{inner}<figcaption>{caption}</figcaption></figure>')
def cards(items):
    cs="".join(f'<div class="cd"><span class="cd-t">{t}</span><span class="cd-d">{jp(d)}</span></div>' for t,d in items)
    return f'\n\n<div class="mb-cards">{cs}</div>'
def step(no, ttl, ol_items):
    lis="".join(f"<li>{jp(t)}</li>" for t in ol_items)
    return (f'\n\n<div class="mb-step"><div class="st-ttl"><span class="st-no">{no}</span>{ttl}</div><ol>{lis}</ol></div>')
P=lambda t:f"\n\n<p>{jp(t)}</p>"
PL=lambda t:f'\n\n<p class="mb-lead">{jp(t)}</p>'
H2=lambda t:f"\n\n<h2>{t}</h2>"
H3=lambda t:f"\n\n<h3>{t}</h3>"
NB="\n\n&nbsp;"
def ul(items): return "\n\n<ul>"+"".join(f"\n<li>{jp(i)}</li>" for i in items)+"\n</ul>"
def warn(t): return f'\n\n<div class="mb-warn">{jp(t)}</div>'
def point(t): return f'\n\n<div class="mb-point">{jp(t)}</div>'
def note(ttl,t): return f'\n\n<div class="mb-note"><p class="nt-ttl">{ttl}</p>{jp(t)}</div>'
def copybox(ttl, lines): return f'\n\n<div class="mb-copy"><div class="cp-ttl">{ttl}</div>'+"<br>".join(lines)+'</div>'
def cta_yt():
    return ('\n\n<div class="mb-cta yt"><p class="cta-ttl">&#x25b6; 動きは動画で見るのが早いです</p>'
            '<p>エージェントの作り方や実演は、PA45の各回をYouTubeにアーカイブしています。</p>'
            f'<a class="mb-btn yt" href="{YT_URL}" target="_blank" rel="noopener">PA45のYouTubeチャンネルを見る</a></div>')
def cta_pa(ttl, body):
    return (f'\n\n<div class="mb-cta pa"><p class="cta-ttl">{ttl}</p><p>{jp(body)}</p>'
            f'<a class="mb-btn pa" href="{CP_URL}" target="_blank" rel="noopener">次回のPA45に申し込む（無料）</a>'
            '<span class="cta-sub">毎週木曜の夜・オンライン・参加無料／途中入退室OK・見るだけ参加も歓迎です</span></div>')

# ===== モック本体 =====
def conn(icon,color,name,pick=False,plus=True):
    p='<span class="cp">+</span>' if plus else ''
    return (f'<div class="ui-conn{" pick" if pick else ""}"><span class="ci" style="background:{color}">{icon}</span>{name}{p}</div>')

TOOLPICKER = ('<div class="uiwin"><div class="ui-dtitle">ツールの追加</div>'
 '<div class="ui-dsub">エージェントを外部のシステムやアクションにつなぎます</div>'
 '<div class="ui-tabs"><span class="ui-tab on">おすすめ</span><span class="ui-tab">モデル コンテキスト プロトコル (MCP)</span>'
 '<span class="ui-tab">コネクタ</span><span class="ui-tab">ワークフロー</span></div>'
 '<div class="ui-conns">'
 +conn('O','#0f6cbd','Office 365 Outlook',pick=True)
 +conn('T','#5b5fc7','Microsoft Teams')
 +conn('S','#217346','SharePoint')
 +conn('D','#0b6a0b','OneDrive for Business')
 +conn('X','#217346','Excel Online (Business)')
 +conn('◆','#742774','Microsoft Dataverse')
 +'</div></div>')

PERM = ('<div class="ui-perm redbox"><span class="rl">実行前に許可を確認</span>'
 '<div class="pt">Permission Required（許可が必要です）</div>'
 '<div class="pb">このエージェントが <b>shared_office365</b> を使って <b>SendEmailV2（メールの送信）</b> を実行しようとしています。許可しますか？</div>'
 '<div class="pbtns"><span class="ui-btn-primary">Allow（許可）</span><span class="ui-btn-ghost">Deny（拒否）</span></div></div>')

MAIL = ('<div class="ui-mail"><div class="mh"><div class="msub">コパスタ45 お問い合わせ</div>'
 '<div class="mmeta">差出人：コパスタ45 案内係（自動送信）　／　宛先：担当</div></div>'
 '<div class="mbody">担当者さま、<br><br>コパスタ45への<span class="mline-hi">申し込み希望のお問い合わせ</span>が届きました。<br><br>'
 '【内容】<br>「コパスタ45に申し込みたい」とのご希望です。<br><br>ご確認の上、ご連絡をお願いします。<br><br>コパスタ45 案内係より</div></div>')

# ===== 画像（実機スクショ）アップロード =====
PUSH = "--push" in sys.argv
state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"post_id": None, "media": {}}
state.setdefault("media", {})
WP = H = None
if PUSH:
    env = {}
    for line in (ROOT/".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k,v=line.split("=",1); env[k.strip()]=v.strip()
    WP = env["WP_URL"].rstrip("/")
    H = {"Authorization":"Basic "+base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()}

IMG = {"overview": HERE/"assets"/"shot-overview.png"}
def upload(key):
    p = IMG[key]
    if not p.exists(): print("WARN missing:", p); return ""
    if not PUSH: return p.as_uri()
    if key in state["media"]: return state["media"][key]["url"]
    mh = dict(H); mh["Content-Disposition"]=f'attachment; filename="cs-tools-{key}.png"'; mh["Content-Type"]="image/png"
    r = requests.post(f"{WP}/wp-json/wp/v2/media",headers=mh,data=p.read_bytes(),timeout=180); r.raise_for_status(); j=r.json()
    state["media"][key]={"id":j["id"],"url":j["source_url"]}; print("uploaded",key,"->",j["id"]); return j["source_url"]
U = {k: upload(k) for k in IMG}
def real_shot(url, caption):
    if not url: return ""
    return ('\n\n<figure style="margin:32px 0;background:#eceef2;border:1px solid #d9dce3;border-radius:14px;padding:14px;box-shadow:0 3px 12px rgba(15,23,42,.09);">'
            '<span style="display:inline-block;font-size:12.5px;font-weight:800;color:#475569;background:#dde1e9;border-radius:999px;padding:5px 14px;margin-bottom:10px;">&#x1f5a5;&#xfe0f; 実際の画面</span><br>'
            f'<img src="{url}" alt="" style="max-width:100%;height:auto;border-radius:8px;border:1px solid #c7cad3;box-shadow:0 6px 18px rgba(15,23,42,.14);" />'
            f'<figcaption style="font-size:1.02em;color:#5b4a7a;margin-top:12px;line-height:1.65;">{caption}</figcaption></figure>')

# ===== 本文 =====
H_=[]; a=H_.append
a('<div class="cs-preface">📝 実際に <b>Copilot Studio を触って検証</b>し、スクショを撮りながら気づいたことをまとめた記録です。<br>機能・画面・料金は更新が続きます。<br>最新の正確な情報は <a href="https://learn.microsoft.com/ja-jp/microsoft-copilot-studio/" target="_blank" rel="noopener">Microsoft 公式（Microsoft Learn）</a> をご確認ください。</div>')

a('\n\n<div class="mb-intro">この記事は、筆者が実際に Copilot Studio でエージェントに「ツール」を足しながら、気づいたことを AI と壁打ち（相談）しつつまとめました。<br>「初めての人が、読みながら同じことを試せる」ことを目指しています。</div>')

a(PL('前回の記事では、Copilot Studio で<span class="hl-marker">「質問に答えてくれる AI（受付エージェント）」</span>を作りました。ただ、それだけだと AI にできるのは「調べて答える」ことまでです。'))
a(PL('今回は、その AI に<strong>「ツール（道具）」</strong>を持たせて、<span class="hl-marker">実際に手を動かす＝“やっておく”</span>ところまで進めます。題材として、「答えられない質問や“申し込みたい”という声が来たら、担当者にメールで知らせる」手を付けてみます。'))
a(PL('やってみると、<strong>途中で一度つまずきました</strong>。その「つまずき」こそが、ツールを使ううえで一番大事なポイントだったので、失敗もふくめて正直に書いていきます。'))

a(fig_svg(
'<svg viewBox="0 0 720 172" font-family="\'Noto Sans JP\',sans-serif">'
'<marker id="ah" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto"><path d="M0 0l6 3-6 3z" fill="#a78bda"/></marker>'
'<rect x="24" y="42" width="250" height="92" rx="14" fill="#F5F3FF" stroke="#7C3AED" stroke-width="2"/>'
'<text x="149" y="82" text-anchor="middle" font-size="16" font-weight="700" fill="#5B21B6">これまで：調べて答える</text>'
'<text x="149" y="110" text-anchor="middle" font-size="13" font-weight="700" fill="#6D28D9">質問に返事するだけ</text>'
'<path d="M282 88 H330" stroke="#a78bda" stroke-width="3" marker-end="url(#ah)"/>'
'<text x="306" y="78" text-anchor="middle" font-size="12" font-weight="700" fill="#9D174D">道具を足す</text>'
'<rect x="340" y="42" width="356" height="92" rx="14" fill="#FDF2F8" stroke="#EC4899" stroke-width="2"/>'
'<text x="518" y="82" text-anchor="middle" font-size="16" font-weight="700" fill="#9D174D">今回：やっておく</text>'
'<text x="518" y="110" text-anchor="middle" font-size="13" font-weight="700" fill="#BE185D">メールを送る・記録するなど、実際に動く</text>'
'</svg>',
"▲ ツールを足すと、AI は「答える」だけでなく「実際にやる」ようになる"))

a(NB)
a(H2('今回やること ── 受付AIに“メールを送る手”を持たせる'))
a(note('&#x1f4a1; 「コパスタ45」とは？','この記事に出てくる <strong>コパスタ45</strong> は、筆者が準備している<strong>「Copilot Studio を初心者向けにやさしく学ぶ、全14回の勉強会」</strong>です。今回はこの勉強会の“案内係AI”を題材に、ツールの付け方を試します。題材はご自分の身近なもの（社内の問い合わせ受付など）に置きかえてOKです。'))
a(P('前回作った「案内係AI」に、<strong>Office 365 Outlook の「メールを送信する」ツール</strong>を足します。ゴールは、参加希望者が「申し込みたい」と言ったときに、<strong>案内係が自分で担当者あてにメールを送ってくれる</strong>状態です。'))
a(cards([
 ('&#x1f50e; いまの案内係', '講座について、資料をもとに出典つきで答えられる。ただし「答える」だけ。'),
 ('&#x1f527; 足す道具', 'Office 365 Outlook「メールを送信する（V2）」。担当者への連絡を担わせる。'),
 ('&#x1f3af; できるようになること', '「申し込みたい」に対して、案内係が担当へ自動でメール連絡する。'),
 ('&#x1f6e1;&#xfe0f; 安全のしくみ', '送信のような操作は、実行前に「許可しますか?」と確認が出る（後述）。'),
]))

a(NB)
a(H2('用意するもの'))
a(ul(['<strong>前回までに作った Copilot Studio のエージェント</strong>（なくても、簡単な受付AIを1体用意すればOK）',
      '<strong>Office 365（Outlook）が使える Microsoft 365 アカウント</strong>',
      'ブラウザ（Edge や Chrome）']))
a(note('&#x26a0;&#xfe0f; テストで“本当に”メールが飛びます','この設定をテストすると、指定した宛先に<strong>実際にメールが送信されます</strong>。練習のあいだは、<strong>宛先を自分（や自分のチーム）のアドレス</strong>にしておくと安心です。'))

a(NB)
a(H2('作り方（実画面つき）'))
a(P('操作に入る前に、どこから始めるかを確認します。Copilot Studio（copilotstudio.microsoft.com）に会社のアカウントでサインインし、前回つくった受付エージェントを一覧から開きます。開くと編集画面（Build）になり、画面の右側にコンポーネントのパネルが並びます。'))
a('\n\n<div class="csflow-w"><p class="csflow-t">ツールを足す画面にたどり着くまで</p><div class="csflow">'
  '<div class="stp"><span class="sn">①</span><div class="st">Copilot Studioを開く<br>（copilotstudio.microsoft.com）</div></div>'
  '<div class="ar">→</div>'
  '<div class="stp"><span class="sn">②</span><div class="st">受付エージェントを開く<br>（前回つくったもの）</div></div>'
  '<div class="ar">→</div>'
  '<div class="stp"><span class="sn">③</span><div class="st">編集画面（Build）が開く</div></div>'
  '<div class="ar">→</div>'
  '<div class="stp"><span class="sn">④</span><div class="st">右パネルの Tools の「＋」</div></div>'
  '</div></div>')
a(real_shot(U["overview"], '&#x25b2; 編集画面（Build）。右側に Skills／Tools／Knowledge が並ぶ。赤枠が今回さわる Tools'))
a('<figure style="margin:32px 0;background:#eceef2;border:1px solid #d9dce3;border-radius:14px;padding:14px;box-shadow:0 3px 12px rgba(15,23,42,.09);"><span style="display:inline-block;font-size:12.5px;font-weight:800;color:#475569;background:#dde1e9;border-radius:999px;padding:5px 14px;margin-bottom:10px;">&#x1f5a5;&#xfe0f; 実際の画面</span><br><img src="https://www.automate136.com/wp-content/uploads/2026/08/cs-tools-instr-thin.png" alt="" style="max-width:100%;height:auto;border-radius:8px;border:1px solid #c7cad3;box-shadow:0 6px 18px rgba(15,23,42,.14);" /><figcaption style="font-size:1.02em;color:#5b4a7a;margin-top:12px;line-height:1.65;">&#x25b2; 受付エージェントの Instructions。右パネルの Tools に「メールの送信(V2)」を追加してあり、この指示文で「いつ・どんな内容でメールを送るか」を日本語で書いておく</figcaption></figure>')

a(H3('ステップ①：ツールの一覧を開く'))
a(P('エージェントの編集画面（Build）を開きます。右側のパネルに <strong>「Tools（ツール）」</strong> という欄があるので、その <strong>＋</strong> を押します。'))
a(step('1','ツールの追加をひらく',[
 '編集画面の右パネルにある <strong>「Tools」</strong> の <strong>＋</strong> をクリック',
 '<strong>「ツールの追加」</strong>の画面が開く（タブが4つ：おすすめ／MCP／コネクタ／ワークフロー）',
 '「おすすめ」に、Outlook・Teams・SharePoint などがならぶ',
]))
a(mock(TOOLPICKER, "▲ 「ツールの追加」画面。まずは「おすすめ」から Office 365 Outlook を選ぶ"))
a(point('道具は<span class="hl-marker">「おすすめ」以外にも、コネクタ一覧・ワークフロー・MCP から選べます</span>。今回は一番身近な Outlook を使いますが、「SharePoint に記録する」「Teams に通知する」なども同じ手順で足せます。'))

a(H3('ステップ②：「メールを送信する」を選んで追加する'))
a(P('Office 365 Outlook をクリックすると、メール送信・予定取得などの<strong>アクション（できること）の一覧</strong>が出ます。この中から <strong>「メールの送信（V2）」</strong> を選びます。'))
a(step('2','メール送信のアクションを足す',[
 '「Office 365 Outlook」をクリック',
 'アクション一覧から <strong>「メールの送信 (V2)」</strong> をさがす',
 '選んで、<strong>「＋ 追加」</strong> を押す',
 '接続（サインイン）を聞かれたら、自分のアカウントの接続を選ぶ（初回は認証が必要な場合あり）',
]))
a(note('&#x1f4a1; アクションはたくさんある','Outlook だけでも「メール送信」「予定の取得」「連絡先の取得」など多くのアクションがあります。<strong>やらせたいこと1つに対して、必要なアクションだけ</strong>を足すのがコツです。増やしすぎると、AI がどれを使うか迷いやすくなります。'))

a(NB)
a(H2('&#x26a0;&#xfe0f; ここが今回の山：道具を足しただけでは、使ってくれない'))
a(P('道具を足したので、さっそくテストしました。Preview で <strong>「コパスタ45に申し込みたいです」</strong> と話しかけてみます。'))
a(P('ところが──案内係は、<strong>メールを送ってくれませんでした</strong>。「申し込み方法はわかりません。告知ページをご確認ください」と答えて終わり。メールを送る、という発想が出てきませんでした。'))
a(point('理由はシンプルでした。<span class="hl-marker">道具を棚に置いただけでは、AI は「いつ使えばいいか」を知らない</span>からでした。人間でいえば、机に電話を置かれても「どんな時にかけるか」を言われないと使わないのと同じです。'))
a(P('そこで、<strong>指示文（Instructions）に「こういう時は、この道具を使ってね」と一文足します</strong>。これがツールを活かす一番のポイントでした。'))
a(step('3','いつ使うかを、指示文に書く',[
 '編集画面の <strong>Instructions</strong>（指示文）の欄をひらく',
 '「やること」のところに、下の一文を追記する',
 '<strong>宛先は、自分（や担当チーム）のアドレス</strong>に置きかえる',
 '右上の<strong>保存アイコン</strong>で保存する',
]))
a(copybox('&#x1f4dd; 追記する指示文（コピーして使えます）', [
 '参加希望者が「申し込みたい」と言ったときや、答えられない質問が来たときは、',
 '「メールの送信」ツールを使って担当者に知らせます。',
 '宛先＝（担当者のメールアドレス）、件名＝「コパスタ45 お問い合わせ」、',
 '本文に相手の質問や希望を書きます。',
 '送る前に「担当にお伝えしますね」と一言添えます。',
]))
a(note('&#x1f4a1; “いつ使うか”は「説明」でも効く','ツールには一つひとつ<strong>「説明」</strong>を書けます。この説明がくわしいほど、AI が「今はこの道具だ」と正しく選べます。指示文と説明、両方をていねいに書くのがコツです。'))

a(NB)
a(H2('もう一度テスト ── 今度は“手”が動く'))
a(P('指示文を足して保存したら、Preview を <strong>「＋ New chat」</strong>で新しくして、もう一度 <strong>「コパスタ45に申し込みたいです」</strong> と話しかけます。'))
a(P('今度は案内係が <strong>「担当にお伝えしますね」→「メールでご連絡します」</strong> と言って、メール送信ツールを動かそうとしました。ここで、Copilot Studio が<strong>安全のための確認</strong>を出します。'))
a(mock(PERM, "▲ 送信の直前に出る「許可の確認」。人が Allow を押して初めて実行される"))
a(point('メール送信のように<span class="hl-marker">“実際に何かをする”操作は、AI が勝手に実行せず、必ず人に「許可しますか?」と確認</span>します。暴走を防ぐ大事なしくみです。内容を確かめて <strong>「Allow（許可）」</strong> を押すと、初めて実行されます。'))
a(P('「Allow」を押すと、案内係が実際にメールを送信し、<strong>「メールを送りました。担当からご連絡がありますので少々お待ちください」</strong>と返してくれました。そして──'))
a(mock(MAIL, "▲ 実際に届いたメール。件名も本文も、案内係が自分で組み立てて送っている"))
a(P('件名も本文も、こちらでテンプレートを渡していないのに、<strong>案内係が会話の内容から自分で組み立てて</strong>送っていました。「調べて答える」だけだった AI が、ちゃんと“手”を動かした瞬間です。'))

a(NB)
a(H2('この文面、だれが書いたの？── ここが Power Automate との大きな違い'))
a(P('届いたメールを見て、正直「あれ？」と思いました。文面を、私は一度も書いていません。指示文で伝えたのは「件名」と「本文に相手の希望を書く」ことだけ。それなのに、あいさつから結びまで、ちゃんとした文章になって届きました。'))
a(H3('Power Automate なら、文面は自分で組み立てる'))
a(P('ふだんの Power Automate でメールを送るときは、本文を自分で用意します。「〇〇さん、〜のお問い合わせがありました」という文章のかたちを先に作って、動的コンテンツ（差し込み）で名前や内容を埋めていきます。つまり、文章の骨組みは人が先に決めておくのがふつうです。'))
a(P('Copilot Studio では、そこが違いました。文章の骨組みごと、AI が会話の流れから考えて書いてくれる。ここが、今回いちばん「おっ」と思った差でした。'))
a(cards([
 ('&#x1f9f0; Power Automate', 'メールの文面は人が用意する。テンプレートを作って、名前や内容を差し込みで埋める。'),
 ('&#x1f916; Copilot Studio', '文面も AI が会話から考えて書く。テンプレートを渡さなくても、文章になって送られる。'),
]))
a(H3('便利だけど、少し不安 ── その気持ちも正直に'))
a(P('一方で、「指定していないのに、勝手に書かれた」ことに、少し不安も感じました。便利なのは確かですが、「知らないうちに、意図とちがう文章を送ってしまわないか」と考えると、そわそわします。この感覚は、たぶん多くの人が持つのではないかと思います。'))
a(H3('では、この文面はどうやって出てきたのか'))
a(P('気になったので、仕組みを自分なりに整理してみました。むずかしくはありませんでした。'))
a(ul(['AI は「会話の内容（相手が“申し込みたい”と言った）」と「指示文（件名はこれ、本文に相手の希望を書いてね）」の<strong>2つを材料</strong>にします。',
      'その材料をもとに、<strong>頭脳の AI モデルが、自然な日本語の文章に組み立てて</strong>います。',
      'つまり、どこかにテンプレートがあったわけではなく、<strong>その場で書き起こしています</strong>。']))
a(point('だから、送られる文面は毎回まったく同じではありません。会話がちがえば、書かれ方も少し変わります。<span class="hl-marker">「決まった文章を送る」のではなく「その時の内容に合わせて書く」</span>のが、この仕組みの特徴です。これが便利さにつながっている一方で、「勝手に書かれた」と感じる理由にもなっています。'))
a(H3('不安なら、手綱は握れる'))
a(P('「お任せは少しこわい」という場合は、こちらで決めておくこともできます。<strong>お任せか、きっちり指定か、両方えらべる</strong>のが安心なところです。'))
a(cards([
 ('&#x1f4dd; 文面を固定する', '指示文に「本文は必ず次のかたちで書いて」とテンプレートを書いておくと、その形を守って書きます。'),
 ('&#x2705; 送る前に確認する', '今回のように「送る前に許可（Allow）を出す」しくみを使えば、内容を人が確かめてから送れます。'),
 ('&#x1f4e5; 下書きで止める', '「メールを送信」ではなく「下書きを作成」にすれば、送らずに下書きだけ作り、人が最終チェックできます。'),
 ('&#x2696;&#xfe0f; 選べるのが強み', '「お任せの便利さ」と「人が確認する安心」を、自分で選べる。ここが手を持たせるときの肝です。'),
]))
a(P('この便利さと安心のバランスを、自分で選べるのが Copilot Studio のいいところだと思いました。全部お任せにもできるし、大事なところは人が握ることもできる。<strong>「AI が書いた」ことにモヤっとしたら、確認や固定のしくみで手綱を握ればいい</strong>。そう分かると、さっきの不安はだいぶ軽くなりました。'))

a(NB)
a(H2('つまずきポイント（先に知っておくと安心）'))
a(ul(['<strong>道具を足しただけでは使われない</strong> → 一番のポイント。指示文に「いつ・誰に・何を」を書いて、初めて動きます。',
      '<strong>宛先を実在しないアドレスにすると送れない</strong> → テストのときは、届くのを確認できる自分のアドレスにしておきます。',
      '<strong>接続（サインイン）が要ることがある</strong> → 初めてそのサービスの道具を使うときは、アカウントの接続を作る画面が出ます。画面の案内どおりに進めます。',
      '<strong>「許可」を押さないと実行されない</strong> → これは不具合ではなく安全機能です。自動で動かしたい場合の設定は、慣れてから調整します。']))

a(H3('応用：メール以外の“手”も同じ手順'))
a(P('今回はメールでしたが、<strong>やり方はどの道具でも同じ</strong>です。「道具を足す → 指示文でいつ使うか書く → テスト」。'))
a(cards([
 ('&#x1f4dd; 記録する', 'SharePoint の「項目の作成」を足せば、質問を一覧（台帳）に自動で記録できます。'),
 ('&#x1f4ac; 通知する', 'Teams の「メッセージ投稿」を足せば、チャネルに自動でお知らせできます。'),
 ('&#x1f4c5; 予定を作る', 'Outlook の「イベントの作成」を足せば、打ち合わせの予定を入れられます。'),
 ('&#x1f501; 組み合わせる', '複数の道具を足して、「記録して、担当に通知する」のように連携もできます。'),
]))

a(NB)
a(H2('まとめ'))
a(P('やったことは、<strong>道具を1つ足して、指示文に「いつ使うか」を1行書いただけ</strong>です。'))
a(ul(['<strong>①</strong> 右パネルの Tools ＋ から、使いたい道具（今回は Outlook「メールの送信」）を足す',
      '<strong>②</strong> 指示文に「こういう時はこの道具を使う」と書く（ここが一番大事）',
      '<strong>③</strong> テストして、許可を押すと、実際に手が動く']))
a(P('「調べて答える」だけだった AI が、<span class="hl-marker">「じゃあ、やっておきますね」まで踏み込める</span>。ここまで来ると、ぐっと“仕事の相棒”らしくなります。次は、記録や通知など、自分の身近な作業に合う道具を1つ試してみるのがおすすめです。'))

a('\n\n<div class="mb-check"><p class="ck-ttl">&#x1f4cb; この記事で学んだこと</p>'
 + "".join(f'<label><input type="checkbox">{t}</label>' for t in [
   'ツール（道具）は、右パネルの <strong>Tools ＋</strong> から追加できる',
   'Outlook・Teams・SharePoint など、身近なサービスの操作を足せる',
   '<strong>道具を足しただけでは AI は使わない。指示文に「いつ使うか」を書く</strong>',
   'メール送信のような操作は、実行前に <strong>「許可（Allow）」</strong> の確認が出る',
   'メールの<strong>文面は AI が会話から書く</strong>（Power Automate との違い）。不安なら、確認や固定で手綱を握れる',
   '記録・通知・予定作成など、他の道具も同じ手順で足せる',
 ]) + '</div>')

a(NB)
a(H2('次回のPA45で、続きを一緒に作りませんか'))
a(P('PA45 では、こうした「45分でひとつ作る」ハンズオンを、<strong>毎週木曜の夜にオンライン無料</strong>でやっています。一人だと詰まりがちなところも、その場で質問しながら進められます。'))
a(cta_pa('&#x1f64c; こういうのを、毎週みんなで作っています',
 'PA45は知識ゼロ・見るだけ参加も大歓迎です。次回もまた、ひとつ新しいものを一緒に作ります。お申し込みは下のボタンから（無料）。'))
a(P(f'過去回のまとめや、PA45がどんな勉強会かは <a href="{PA45_URL}" target="_blank" rel="noopener">PA45の紹介ページ</a> にまとめています。また次回、一緒に「できた！」を作りましょう。'))
a(cta_yt())

a('\n\n<p style="font-size:13px;color:#888;line-height:1.9;">※ 本記事は公開日時点の情報をもとに、筆者が実際に学んで試した内容を整理しました。Copilot Studio の画面や仕様は更新されることがあるため、最新の状況は公式情報（Microsoft Learn）もあわせてご確認ください。画面の項目名・挙動は実機（Copilot Studio）で確認しています。</p>')
a('\n\n<p style="font-size:13px;color:#888;line-height:1.9;">※ 掲載している画面は、実際の操作画面をもとに、個人情報などを避けて描き直した再現イメージです。構成や図解の一部は、AI と壁打ちしながら作成しています。</p>')

content=CSS+'\n\n<div class="mb-body">'+"".join(H_)+'\n\n</div>'
(HERE/"article.html").write_text(content,encoding="utf-8")
print("article.html:",len(content),"chars")

# ================= WP 下書き作成/更新（--push のときだけ） =================
if PUSH:
    payload={"title":TITLE,"slug":SLUG,"status":"draft","content":content,"categories":[CAT]}
    if state.get("post_id"):
        r=requests.post(f"{WP}/wp-json/wp/v2/posts/{state['post_id']}",headers=H,json=payload,timeout=120)
        r.raise_for_status(); pid=state["post_id"]; print("UPDATED",pid)
    else:
        r=requests.post(f"{WP}/wp-json/wp/v2/posts",headers=H,json=payload,timeout=120)
        r.raise_for_status(); pid=r.json()["id"]; state["post_id"]=pid; print("CREATED",pid)
    STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding="utf-8")
    print("status:",r.json()["status"])
    print("EDIT =",f"{WP}/wp-admin/post.php?post={pid}&action=edit")
else:
    print("（ローカル生成のみ。WordPress下書き作成は  python build_article.py --push  ）")

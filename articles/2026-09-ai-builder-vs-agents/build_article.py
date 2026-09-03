#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""コパスタ記事＝「AI Builder／エージェント ビルダー／Copilot Studio の違い」3者比較。
- 立ち位置：vs-pa(2591)の続き。あちらが PA と CS の2者、こちらが AI Builder を足した3者。
- 数値・無償枠は 2026-09-04 に Microsoft Learn / 公式価格ページで取り直して裏取り済み（末尾に出典）。
- 恒久ルール準拠：cs-preface／現在地バー＋節ゴール(_navkit)／mb-term(用語)／句点改行／図解カード／比較表／末尾免責。
- 実機スクショは撮っていない記事なので、前書きで「公式を読み直して整理した記録」と正直に書く。
- WordPress下書き。status:draft固定（自動公開しない）。post_state.jsonで同ID上書き。

  python build_article.py          # article.html を作るだけ
  python build_article.py --push   # 画像アップ＋WP下書きを作成/更新
"""
import base64, requests, pathlib, re, json, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).resolve().parent
STATE = HERE / "post_state.json"
PUSH = "--push" in sys.argv

TITLE = "AI Builder・エージェント ビルダー・Copilot Studio の違い｜どれで作るか、お金はどこから発生するか"
SLUG  = "ai-builder-agent-builder-copilot-studio"
CAT   = 76

YT_URL   = "https://www.youtube.com/@Haru_PowerAutomate136"
CP_URL   = "https://powerautomate-create.connpass.com/event/399555/"
PA45_URL = "https://www.automate136.com/pa45/"

IMG = {
    "eyecatch":   HERE / "assets" / "eyecatch.png",
    "fig-layers": HERE / "assets" / "fig-layers.png",
    "fig-money":  HERE / "assets" / "fig-money.png",
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
.mb-intro{background:#f6f4fb;border:1px solid #e0d7f3;border-left:5px solid #a78bda;border-radius:10px;padding:13px 18px;margin:4px 0 30px;font-size:.9em;color:#5b4a7a;line-height:1.8;}
.mb-fig{margin:44px 0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#e7e0f5;border:1px solid #d0c4ec;border-radius:16px;padding:18px 16px 12px;box-shadow:0 2px 8px rgba(76,29,149,.08);}
.mb-fig img{width:100%;max-width:860px;height:auto;display:block;margin:0 auto;background:#fff;border-radius:10px;box-shadow:0 4px 14px rgba(91,33,182,.16);}
.mb-fig figcaption{font-size:1.02em;color:#5b4a7a;margin-top:12px;line-height:1.8;}
.mb-cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:30px 0;}
.mb-cards.c3{grid-template-columns:1fr 1fr 1fr;}
.mb-cards .cd{background:#fff;border:1px solid #e4dbf6;border-left:5px solid #8b5cf6;border-radius:12px;padding:15px 17px;box-shadow:0 2px 8px rgba(76,29,149,.07);}
.mb-cards .cd.ab{border-left-color:#2563EB;}
.mb-cards .cd.ag{border-left-color:#0d7d74;}
.mb-cards .cd .cd-t{display:block;color:#5b21b6;font-weight:800;font-size:1.02em;margin-bottom:6px;}
.mb-cards .cd.ab .cd-t{color:#1e40af;}
.mb-cards .cd.ag .cd-t{color:#0d6b68;}
.mb-cards .cd .cd-d{font-size:.9em;color:#4b5563;line-height:1.65;}
@media(max-width:700px){.mb-cards,.mb-cards.c3{grid-template-columns:1fr;}}
.mb-cmpwrap{overflow-x:auto;margin:26px 0;}
.mb-cmp{width:100%;border-collapse:collapse;font-size:.95em;min-width:620px;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(76,29,149,.07);}
.mb-cmp th,.mb-cmp td{padding:12px 15px;text-align:left;border-bottom:1px solid #ece4f9;line-height:1.7;vertical-align:top;}
.mb-cmp thead th{font-weight:800;font-size:.92em;}
.mb-cmp thead th.h-obs{background:#f5f5f7;color:#4b5563;}
.mb-cmp thead th.h-ab{background:#eaf1fd;color:#1e40af;}
.mb-cmp thead th.h-ag{background:#e9f6f4;color:#0d6b68;}
.mb-cmp thead th.h-cs{background:#f3eefc;color:#5b21b6;}
.mb-cmp tbody th{background:#fafafb;color:#4b5563;font-weight:700;font-size:.9em;white-space:nowrap;width:1%;}
.mb-cmp td.c-ag{color:#1f4f4c;}
.mb-cmp td.c-cs{color:#3b2a5a;}
.mb-cmp td .no{color:#9aa1ac;}
.mb-cmp tr:last-child td,.mb-cmp tr:last-child th{border-bottom:none;}
.mb-point{background:#f7f4fd;border-left:6px solid #8b5cf6;border-radius:8px;padding:18px 24px;margin:36px 0;line-height:2.1;}
.mb-note{background:#fffdf5;border:2px solid #ffd54f;border-radius:12px;padding:18px 24px;margin:38px 0;line-height:2.1;}
.mb-note .nt-ttl{font-weight:700;color:#e8920c;margin:0 0 14px;}
.mb-term{background:#f4f8ff;border:1px solid #cfe0f7;border-left:5px solid #3b82f6;border-radius:10px;padding:14px 20px;margin:26px 0;font-size:.94em;color:#25405e;line-height:1.9;}
.mb-term .tm{font-weight:800;color:#1e40af;margin-right:.4em;}
.mb-myth{background:#fff;border:1px solid #f0d7d0;border-left:5px solid #d9573c;border-radius:12px;padding:16px 20px;margin:20px 0;box-shadow:0 2px 8px rgba(160,60,40,.06);}
.mb-myth .my-x{font-size:.8em;font-weight:800;color:#a3341f;letter-spacing:.08em;display:block;margin-bottom:4px;}
.mb-myth .my-s{font-weight:800;font-size:1.02em;color:#2c2340;display:block;margin-bottom:8px;}
.mb-myth .my-r{font-size:.94em;color:#4b5563;line-height:1.85;}
.mb-check{border:1px solid #ddd0f2;border-radius:14px;padding:22px 26px;background:#fff;margin:40px 0;}
.mb-check .ck-ttl{margin:0 0 14px;font-weight:800;font-size:1.05em;color:#5b21b6;}
.mb-check label{display:flex;align-items:flex-start;gap:10px;line-height:1.7;font-size:1em;margin:10px 0;}
.mb-check input{margin-top:4px;width:16px;height:16px;accent-color:#7c3aed;flex-shrink:0;}
.mb-src{background:#fafafb;border:1px solid #e7e4ef;border-radius:12px;padding:18px 24px;margin:34px 0;font-size:.88em;color:#5b5470;line-height:1.9;}
.mb-src .sc-ttl{font-weight:800;color:#3f3557;margin:0 0 10px;}
.mb-src ul{margin:0;padding-left:1.3em;}
.mb-src li{margin:.35em 0;}
.mb-src a{color:#5b21b6;font-weight:700;}
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
.cs-preface{background:#eef7f1;border:1px solid #cfe8db;border-left:5px solid #5f8a6e;border-radius:10px;padding:14px 18px;margin:0 0 26px;font-size:.86em;color:#3d5647;line-height:1.85;}
.cs-preface b{color:#2f6b4f;}
.cs-preface a{color:#1d4ed8;font-weight:700;}
</style>
"""

def jp(t): return re.sub(r'。(?![」）】、\s<]|$)', '。<br>', t)

# --- 現在地バー・節ゴール・吹き出し（articles/_navkit.py 共通） ---
import sys as _sys
_sys.path.insert(0, str(ROOT / "articles"))
from _navkit import NAV_CSS, make_nav, make_bubble
NAVSTEPS = ['3つの正体', '使い分け', 'できること', 'お金', '11月の期限', 'よくある誤解']
nav, goal = make_nav(NAVSTEPS, jp)
bubble = make_bubble(jp)
CSS = CSS.replace("</style>", NAV_CSS + "</style>")

def fig(src, caption, alt=""):
    return f'\n\n<figure class="mb-fig"><img src="{src}" alt="{alt}" /><figcaption>{caption}</figcaption></figure>'
def cards(items, c3=False):
    cs = "".join(f'<div class="cd{" "+c if c else ""}"><span class="cd-t">{t}</span><span class="cd-d">{jp(d)}</span></div>' for t, d, c in items)
    return f'\n\n<div class="mb-cards{" c3" if c3 else ""}">{cs}</div>'
def cmp3(rows):
    body = "".join(f'<tr><th>{o}</th><td>{a}</td><td class="c-ag">{b}</td><td class="c-cs">{c}</td></tr>' for o, a, b, c in rows)
    return ('\n\n<div class="mb-cmpwrap"><table class="mb-cmp"><thead><tr>'
            '<th class="h-obs">観点</th><th class="h-ab">AI Builder</th>'
            '<th class="h-ag">エージェント ビルダー</th><th class="h-cs">Copilot Studio</th>'
            f'</tr></thead><tbody>{body}</tbody></table></div>')
def rate_table(rows):
    body = "".join(f'<tr><th>{a}</th><td>{b}</td><td class="c-cs">{c}</td></tr>' for a, b, c in rows)
    return ('\n\n<div class="mb-cmpwrap"><table class="mb-cmp"><thead><tr>'
            '<th class="h-obs">何をしたとき</th><th class="h-cs">消費するCopilotクレジット</th>'
            '<th class="h-cs">M365 Copilot保有者の社内利用</th>'
            f'</tr></thead><tbody>{body}</tbody></table></div>')
P  = lambda t: f"\n\n<p>{jp(t)}</p>"
PL = lambda t: f'\n\n<p class="mb-lead">{jp(t)}</p>'
H2 = lambda t: f"\n\n<h2>{t}</h2>"
NB = "\n\n&nbsp;"
def ul(items): return "\n\n<ul>" + "".join(f"\n<li>{jp(i)}</li>" for i in items) + "\n</ul>"
def point(t): return f'\n\n<div class="mb-point">{jp(t)}</div>'
def note(ttl, t): return f'\n\n<div class="mb-note"><p class="nt-ttl">{ttl}</p>{jp(t)}</div>'
def term(name, t): return f'\n\n<div class="mb-term"><span class="tm">{name}</span>{jp(t)}</div>'
def myth(said, real):
    return (f'\n\n<div class="mb-myth"><span class="my-x">よくある誤解</span>'
            f'<span class="my-s">{said}</span><span class="my-r">{jp(real)}</span></div>')
def sources(items):
    li = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a>（{d} 時点）</li>' for t, u, d in items)
    return (f'\n\n<div class="mb-src"><p class="sc-ttl">この記事で確認した公式ページ</p><ul>{li}</ul>'
            '<p style="margin:12px 0 0;">価格・無償枠・課金条件は更新が続きます。<br>見積もりの前に、上のページを開き直してご確認ください。</p></div>')
def cta_yt():
    return ('\n\n<div class="mb-cta yt"><p class="cta-ttl">&#x25b6; 動きは動画で見るのが早いです</p>'
            '<p>Power Automate や Copilot Studio の実演は、PA45の各回をYouTubeにアーカイブしています。</p>'
            f'<a class="mb-btn yt" href="{YT_URL}" target="_blank" rel="noopener">PA45のYouTubeチャンネルを見る</a></div>')
def cta_pa(ttl, body):
    return (f'\n\n<div class="mb-cta pa"><p class="cta-ttl">{ttl}</p><p>{jp(body)}</p>'
            f'<a class="mb-btn pa" href="{CP_URL}" target="_blank" rel="noopener">次回のPA45に申し込む（無料）</a>'
            '<span class="cta-sub">毎週木曜の夜・オンライン・参加無料／途中入退室OK・見るだけ参加も歓迎です</span></div>')

# ---- WP ----
state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"post_id": None, "media": {}}
U = {}
if PUSH:
    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1); env[k.strip()] = v.strip()
    WP = env["WP_URL"].rstrip("/")
    auth = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    H = {"Authorization": f"Basic {auth}"}

    def upload(key):
        if key in state["media"]:
            return state["media"][key]["url"]
        p = IMG[key]
        if not p.exists():
            print("WARN not found", p); return ""
        mh = dict(H); mh["Content-Disposition"] = f'attachment; filename="ai3way-{key}.png"'; mh["Content-Type"] = "image/png"
        r = requests.post(f"{WP}/wp-json/wp/v2/media", headers=mh, data=p.read_bytes(), timeout=180)
        r.raise_for_status(); j = r.json()
        state["media"][key] = {"id": j["id"], "url": j["source_url"]}
        print("uploaded", key, "->", j["id"]); return j["source_url"]

    for k in IMG:
        U[k] = upload(k)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
else:
    for k in IMG:
        U[k] = state["media"].get(k, {}).get("url") or ("file:///" + str(IMG[k]).replace("\\", "/"))

# ---- 本文 ----
H_ = []; a = H_.append

a('<div class="cs-preface">📝 <b>Microsoft の公式ドキュメントと価格ページを読み直して整理した記録</b>です。<br>'
  'この記事は実機の操作手順ではなく、3つの機能の違いと料金の考え方をまとめたものです。<br>'
  '機能・料金は更新が続きます。<br>最新の正確な情報は '
  '<a href="https://learn.microsoft.com/ja-jp/microsoft-copilot-studio/" target="_blank" rel="noopener">Microsoft 公式（Microsoft Learn）</a> をご確認ください。</div>')
a('\n\n<div class="mb-intro">「Power Automate の AI Builder」「Copilot のエージェント ビルダー」「Copilot Studio のエージェント」。<br>'
  '名前が似ていて、どれで作ればいいのか分かりにくい3つを、1枚に並べて整理しました。<br>'
  '料金の数字はすべて公式ページで取り直し、出典を記事の最後に載せています。</div>')

a(PL('AI で何か作ろうとすると、入口が3つ出てきます。'))
a(PL('<span class="hl-marker">AI Builder</span>、<span class="hl-marker">エージェント ビルダー</span>、<span class="hl-marker">Copilot Studio</span>。どれも Microsoft の AI で、どれも「作れます」と書いてある。'))
a(PL('比べにくい理由ははっきりしていて、<strong>この3つは同じ土俵に並ぶ製品ではない</strong>からです。役割の大きさが違うものを横一列にすると、比較軸が噛み合いません。'))

a(fig(U["fig-layers"], "▲ 3つは「部品」「軽量エージェント」「本格エージェント」という別の層にある", "AI Builder・エージェント ビルダー・Copilot Studio の位置づけ"))

a(NB)
a(nav(1))
a(H2('3つの正体'))
a(goal('それぞれが何であるかを、一言で押さえます。', 'このあとの比較表が読めるようになります。', read=True))
a(P('まず、それぞれの正体です。'))
a(cards([
 ('&#x1f527; AI Builder ＝ 部品', 'フローやアプリの途中に差し込む、入力から出力を返す AI 機能。会話はしない。請求書からデータを抜く、文章を要約する、といった単機能。', 'ab'),
 ('&#x1f4ac; エージェント ビルダー ＝ 軽量エージェント', 'Copilot Chat の中で会話しながら作る、自分と小さなチーム向けのQ&amp;A係。指示文と読ませる資料を決めるだけで作れる。', 'ag'),
 ('&#x1f3e2; Copilot Studio ＝ 本格エージェント', '専用ポータルで作る、部門・全社・社外向けのエージェント。承認や分岐、外部システムの呼び出しまで担当する。', ''),
], c3=True))

a(term('エージェントとは',
       '指示文と資料を与えておくと、人の質問に会話で答えたり、代わりに処理を進めたりするAIのこと。<strong>AI Builder が「部品」なのに対して、エージェントは「担当者」</strong>に近い存在です。'))
a(term('宣言型エージェント',
       'エージェント ビルダーで作るものの正式な呼び名。プログラムを書くのではなく、<strong>「何を根拠に、どう答えるか」を宣言する（書いて指定する）だけ</strong>で成立するタイプを指します。'))

a(P('もうひとつ、分かりにくさの原因があります。<strong>「Copilot」という言葉が3つの別物を指している</strong>ことです。'))
a(ul(['<strong>Copilot Chat</strong>＝使う場所（チャットの画面）',
      '<strong>Copilot Studio</strong>＝作る場所（専用のポータル）',
      '<strong>Copilot クレジット</strong>＝お金の単位']))
a(P('同じ文章の中でこの3つが混ざるので、読んでいて位置を見失います。<strong>出てきたら、場所の話か・お金の話かを分けて読む</strong>と整理しやすくなります。'))

a(NB)
a(bubble('3つを1つの表に並べるより、層で分けたほうが自分の中では整理がつきました。'))

a(nav(2))
a(H2('どれで作るか'))
a(goal('自分のやりたいことから、使うものを決めます。', '迷ったときに1分で選べるようになります。', read=True))
a(P('私は、この3つで判断しています。'))
a(cards([
 ('&#x1f501; 人と会話しない', '決まった入力から決まった結果が欲しいだけ。例：請求書からデータを抜く、問い合わせ文の感情を判定する。→ <strong>AI Builder</strong>', 'ab'),
 ('&#x1f5e3;&#xfe0f; 手元の資料に質問したい', '自分か数人が、社内文書に聞きたい。Teams や Copilot の中で使えれば十分。→ <strong>エージェント ビルダー</strong>', 'ag'),
 ('&#x1f3af; 業務そのものを動かしたい', '部門や社外に配る。承認・分岐・外部システムが要る。環境を分けて管理したい。→ <strong>Copilot Studio</strong>', ''),
], c3=True))
a(point('迷ったら<span class="hl-marker">軽いほうから始める</span>ほうが安全だと思っています。エージェント ビルダーで作ったものは、<strong>あとから Copilot Studio にコピーできます</strong>。作り直しにならないので、最初から重い方を選ばなくて済みます。'))

a(NB)
a(nav(3))
a(H2('できることの比較'))
a(goal('9つの観点で3つを並べます。', '自分の要件がどれに当たるか判断できます。', read=True))
a(P('横に並べると、境目がはっきりします。'))
a(cmp3([
 ('会話',       '<span class="no">しない</span>', 'する（チャットのみ）', 'する＋自律実行もできる'),
 ('主な中身',   '請求書処理・領収書処理・契約書処理・IDリーダー・名刺リーダー・テキスト認識(OCR)・感情分析・キーフレーズ抽出・言語検出・翻訳・エンティティ抽出・カテゴリ分類。カスタムはドキュメント処理・物体検出・予測',
                '指示文、ナレッジ（公開Web／SharePoint／OneDrive／Microsoft Graph）、開始プロンプト',
                'トピック、生成オーケストレーション、ツール、エージェント フロー、コネクタ、ナレッジ、音声'),
 ('外部システム', 'フロー側のコネクタに任せる', '<span class="no">つなげない</span>', '標準・プレミアム・カスタム コネクタ'),
 ('多段の処理', '<span class="no">1機能で完結（並べるのはフロー側）</span>', '<span class="no">できない</span>', '承認・分岐・複数ステップに対応'),
 ('公開先',     'フローやアプリの中', 'Copilot Chat・Teams・SharePoint（社内）', 'Webサイト・Teams・カスタム エンドポイント・社外顧客'),
 ('権限',       'フローの接続に従う', '利用者本人の Microsoft 365 権限をそのまま引き継ぐ', 'エージェント側で認証方式を設計する'),
 ('管理する場所', 'Power Platform 管理センター', 'Microsoft 365 管理センター', 'Power Platform 管理センター（環境・DLP・ALM）'),
 ('環境分離',   'あり（Power Platform の環境）', '<span class="no">なし</span>', 'あり（開発／テスト／本番、ソリューションで移送）'),
 ('向く相手',   'フローの作り手', '自分・小さなチーム', '部門・全社・社外顧客'),
]))
a(P('注目したいのは<strong>「権限」の行</strong>です。エージェント ビルダーは、利用者本人が見られる範囲しか読みません。'))
a(P('見えないはずの SharePoint サイトの中身が、エージェント経由で漏れることはない。<strong>だから情シスの承認を取りやすい</strong>、という実務上の利点があります。'))

a(NB)
a(nav(4))
a(H2('お金はどこから発生するか'))
a(goal('無料の範囲と、課金が始まる瞬間を押さえます。', '見積もりの起点が分かります。', read=True))
a(P('料金の話は、ここで一度そろえておきたいところです。<strong>課金は「どのツールを使うか」ではなく「何をしたか」で決まります</strong>。'))

a(fig(U["fig-money"], "▲ 3つとも作るのは無料。動かした内容で課金される", "3つの機能の課金の比較"))

a(term('Copilot クレジット',
       'Copilot Studio 系の共通のお金の単位。2025年9月1日に「メッセージ」から名前が変わりました。<strong>1パック＝25,000クレジットで月額29,985円（税別）</strong>、ほかに従量課金と前払いプランがあります。<strong>使い切れなかった分は翌月に繰り越されません</strong>。'))

a(P('Copilot Studio の消費レートは公開されています。'))
a(rate_table([
 ('定型の回答を返した',           '1 クレジット',            '無料'),
 ('AIが文章を生成して答えた',      '2 クレジット',            '無料'),
 ('エージェントがアクションを実行した', '5 クレジット',            '無料'),
 ('社内全体のデータを検索して答えた', '10 クレジット',           '無料'),
 ('エージェント フローを実行した',   '13 クレジット／100アクション', '無料'),
 ('資料を読み取った（コンテンツ処理）', '8 クレジット／ページ',      '無料'),
]))
a(P('右の列のとおり、<strong>Microsoft 365 Copilot ライセンス（1ユーザー月額4,497円・年間契約）を持っている人が、社内で使う分は0円扱い</strong>です。'))
a(P('社内向けに作るなら、まずここに乗るかどうかを確認しています。<strong>効き方が大きい</strong>ので、見積もりはここから始めると早いと感じます。'))

a(point('もうひとつ大事な線引きがあります。<strong>Power Automate のクラウド フローは Copilot クレジットの対象外</strong>です。<br>これまで通り Power Automate のライセンスで動きます。<span class="hl-marker">考えるところをエージェント、決まった作業をフロー</span>に寄せると、そのぶんクレジットを使いません。'))

a(NB)
a(bubble('料金表は項目が多いのですが、社内向けなら M365 Copilot の無料の列に収まるかどうかから見ています。'))

a(nav(5))
a(H2('2026年11月1日に、AI Builder の無料枠が消える'))
a(goal('期限と、そのあと何が必要になるかを確認します。', '手を打つ時期が分かります。', read=True))
a(P('AI Builder を使っている場合は、これだけは押さえておきたい変更があります。'))

a(term('シード クレジット',
       'Premium ライセンスを買うと自動的に付いてくる AI Builder の無料枠のこと。<strong>Power Automate Premium なら1ライセンスあたり月5,000クレジット、Power Apps Premium なら月500クレジット</strong>が配られていました。'))

a(note('&#x26a0;&#xfe0f; 2026年11月1日で終わること',
       '<strong>Premium ライセンスに付いてくるシード クレジットが削除されます</strong>。<br>'
       'AI Builder 容量アドオン（1つ100万クレジット）の新規販売は、すでに2025年11月1日に終了しています。<br>'
       'アクティブな契約がある場合のみ、契約が終わるまで使い続けられます。<br>'
       'それ以降も AI Builder を使うなら、<strong>Copilot クレジットを買う</strong>必要があります。'))

a(P('なお、AI Builder クレジットから Copilot クレジットへの<strong>自動変換はありません</strong>。'))
a(P('いまも消費の順番は決まっていて、<strong>まず AI Builder クレジットを使い、足りなくなったら Copilot クレジットに切り替わります</strong>。両方とも無い場合は、その AI 機能は失敗します。'))
a(P('つまり<strong>11月1日を境に、いままで無料で回っていた処理が急に止まる可能性がある</strong>ということです。フローに AI Builder を組み込んでいる場合は、それまでに消費量を確認しておくと安全です。'))

a(NB)
a(nav(6))
a(H2('よくある誤解'))
a(goal('間違えやすい4点を、公式の記述で正します。', '社内で説明するときに迷いません。', read=True))

a(myth('Copilot Studio を使うと、何をしても課金される',
       '課金は「土台」ではなく<strong>操作ごと</strong>に決まります。手作業での設定と、公開そのものは0クレジットです。<strong>Power Automate のクラウド フローも対象外</strong>で、Power Automate のライセンスで動きます。'))
a(myth('エージェント ビルダーは全部タダ',
       '無料なのは<strong>指示文と公開Webサイトだけを根拠にする場合</strong>です。SharePoint の社内文書を読ませた時点で従量課金の対象になります。しかもこのタイプは<strong>既定でオフ</strong>で、管理者が Copilot Studio のサブスクリプションか従量課金を用意しないと使えません。'))
a(myth('AI Builder と Copilot Studio の AI ツールは別物',
       '中身は同じものです。Copilot Studio 側では<strong>「テキストと生成 AI ツール」</strong>という名前で、基本・標準・プレミアム・コンテンツ処理の4段に整理されています。既存の AI Builder のモデルも、この4段のどれかに割り当てられます（感情分析は基本、エンティティ抽出は標準、など）。'))
a(myth('AI Builder を足しても、ライセンスは変わらない',
       'Power Apps は変わります。<strong>アプリに AI Builder を足すと Premium アプリ扱いになり、Premium ライセンスが必要</strong>です。アプリに埋め込んだフローに足した場合も同じです。<strong>ただし Power Automate 側では、AI Builder を足してもプレミアム フローにはなりません</strong>。ここは扱いが分かれています。'))

a(NB)
a(H2('まとめ'))
a(P('3つの違いは、結局この形に落ち着きます。'))
a(ul(['<strong>AI Builder</strong>＝フローに差し込む部品。会話しない',
      '<strong>エージェント ビルダー</strong>＝Copilot Chat の中で作る、自分と小チームのQ&amp;A係',
      '<strong>Copilot Studio</strong>＝部門・社外まで届く本格エージェント',
      '迷ったら軽いほうから。あとから Copilot Studio にコピーできる',
      'お金は「どのツールか」ではなく「何をしたか」で決まる',
      '<strong>2026年11月1日</strong>に AI Builder のシード クレジットが消える']))

a('\n\n<div class="mb-check"><p class="ck-ttl">&#x1f4cb; この記事で分かったこと</p>'
  + "".join(f'<label><input type="checkbox">{t}</label>' for t in [
    '3つは並ぶ製品ではなく、部品・軽量・本格という別の層にある',
    '会話しないなら <strong>AI Builder</strong>、手元の資料に聞くなら <strong>エージェント ビルダー</strong>',
    '承認・外部連携・社外公開なら <strong>Copilot Studio</strong>',
    'エージェント ビルダーは<strong>公開Webだけなら無料</strong>、社内データを読むと課金',
    'M365 Copilot 保有者の社内利用は0円扱い',
    '<strong>2026年11月1日</strong>にAI Builderのシードクレジットが削除される',
  ]) + '</div>')

a(sources([
 ('AI モデルとビジネス シナリオ（AI Builder）', 'https://learn.microsoft.com/ja-jp/ai-builder/model-types', '2026-01-14'),
 ('ライセンスと AI Builder クレジット', 'https://learn.microsoft.com/ja-jp/ai-builder/credit-management', '2026-01-14'),
 ('AI Builder クレジットの期間終了', 'https://learn.microsoft.com/ja-jp/ai-builder/endofaibcredits', '2026-05-14'),
 ('ライセンスと Copilot クレジット（AIツール）', 'https://learn.microsoft.com/ja-jp/ai-builder/message-management', '2026-06-16'),
 ('Microsoft 365 Copilot Chat のエージェント', 'https://learn.microsoft.com/ja-jp/copilot/agents', '2026-02-04'),
 ('エージェント ビルダーと Copilot Studio の選び方', 'https://learn.microsoft.com/ja-jp/microsoft-365-copilot/extensibility/copilot-studio-experience', '2026-06-18'),
 ('標準ハーネス ライセンス（Copilot Studio）', 'https://learn.microsoft.com/ja-jp/microsoft-copilot-studio/billing-licensing', '2026-08-03'),
 ('請求レートと管理（Copilot Studio）', 'https://learn.microsoft.com/ja-jp/microsoft-copilot-studio/requirements-messages-management', '2026-08-03'),
 ('Copilot Studio の価格（日本）', 'https://www.microsoft.com/ja-jp/microsoft-365-copilot/pricing/copilot-studio', '2026-09-04'),
]))

a(NB)
a(H2('次回のPA45で、実際にさわってみませんか'))
a(P('PA45 では、Power Automate や Copilot Studio を「45分でひとつ作る・試す」ハンズオンを、<strong>毎週木曜の夜にオンライン無料</strong>でやっています。一人だと止まりやすいところも、その場で質問しながら進められます。'))
a(cta_pa('&#x1f64c; まずは、さわってみるのがいちばん',
         'PA45は知識ゼロ・見るだけ参加も歓迎です。次回もまた、ひとつ新しいものを一緒にさわります。お申し込みは下のボタンから（無料）。'))
a(P(f'なお、PA45 がどんな勉強会かは <a href="{PA45_URL}" target="_blank" rel="noopener">PA45の紹介ページ</a> にまとめています。<strong>PA45</strong> は、筆者が運営している「Power Automate を45分で学ぶ、無料のオンライン勉強会」です（毎週木曜の夜・初心者歓迎）。'))
a(cta_yt())

a('\n\n<p style="font-size:13px;color:#888;line-height:1.9;">※ 本記事は公開日時点の情報をもとに整理しました。料金・無償枠・課金条件は変更されることがあるため、最新の状況は公式情報（Microsoft Learn）もあわせてご確認ください。記事中の数値は上記の公式ページで確認しています。</p>')
a('\n\n<p style="font-size:13px;color:#888;line-height:1.9;">※ 本記事の構成や図解の一部は、AI と壁打ちしながら作成しています。</p>')

content = CSS + '\n\n<div class="mb-body">' + "".join(H_) + '\n\n</div>'
(HERE / "article.html").write_text(content, encoding="utf-8")
print("article.html:", len(content), "chars")

if not PUSH:
    print("（ローカル生成のみ。--push でWP下書きへ反映）")
    raise SystemExit

payload = {"title": TITLE, "slug": SLUG, "status": "draft", "content": content, "categories": [CAT]}
if state["media"].get("eyecatch"):
    payload["featured_media"] = state["media"]["eyecatch"]["id"]
if state.get("post_id"):
    r = requests.post(f"{WP}/wp-json/wp/v2/posts/{state['post_id']}", headers=H, json=payload, timeout=120)
    r.raise_for_status(); pid = state["post_id"]; print("UPDATED", pid)
else:
    r = requests.post(f"{WP}/wp-json/wp/v2/posts", headers=H, json=payload, timeout=120)
    r.raise_for_status(); pid = r.json()["id"]; state["post_id"] = pid; print("CREATED", pid)
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
print("status:", r.json()["status"])
print("EDIT =", f"{WP}/wp-admin/post.php?post={pid}&action=edit")
print("PREVIEW =", f"{WP}/?p={pid}&preview=true")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""なんでもCopilot LT大会（オンライン・第3回なんコパLT大会 / #80）登壇レポート。
- automate136・.mb-* テイスト。登壇レポート＝コミュニティ運営(77)＋Power Automate実践(76)。
- 文体＝脱AI量産（文末バリエ・章の入り方を毎回変える・擬態語/大げさ反応語/ポエム/「正直」なし）。
- 「AIが書いた記事に見えないように」＝本文にCopilot執筆の但し書きを置かない（題材としてのCopilotはOK）。
- 事実は 2026-05-13 の LT スライド(LT001_Copilot_MeetingCostBot_20260428.pptx)に基づく。架空の参加者の声・盛り上がり描写なし。
- 勤務先を特定する表現は書かない（時給は一般的な例として提示）。
- 既定=ローカル生成のみ。WordPress下書きは python build_article.py --push"""
import base64, requests, pathlib, re, sys, json

ROOT  = pathlib.Path(__file__).resolve().parents[2]
HERE  = pathlib.Path(__file__).resolve().parent
STATE = HERE / "post_state.json"

TITLE = "なんでもCopilotのLT大会でオンライン登壇して ──「会議を減らせない」から生まれた“会議コストBot”の話"
SLUG  = "nandemo-copilot-lt-meeting-cost-bot"
CATS  = [77, 76]  # コミュニティ運営（PA45） / Power Automate 実践・Tips

EVENT_URL = "https://nandemo.connpass.com/event/390633/"
SLIDE_URL = "https://github.com/Haru-PowerPlatform/pa45/raw/main/assets/pa45/LT001_Copilot_MeetingCostBot_20260428.pptx"

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
.mb-fig svg{width:100%;max-width:780px;height:auto;display:block;margin:0 auto;background:#fff;border-radius:10px;padding:14px 10px;}
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
.mb-step ol li{position:relative;padding:9px 0 9px 32px;line-height:1.85;border-top:1px solid #ece4f9;}
.mb-step ol li:first-child{border-top:none;}
.mb-step ol li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:9px;width:22px;height:22px;background:#ede9fe;color:#5b21b6;border-radius:50%;font-size:.78em;font-weight:800;display:flex;align-items:center;justify-content:center;}
.mb-step ol li b{color:#4c1d95;}
.mb-point{background:#f7f4fd;border-left:6px solid #8b5cf6;border-radius:8px;padding:18px 24px;margin:36px 0;line-height:2.1;}
.mb-note{background:#fffdf5;border:2px solid #ffd54f;border-radius:12px;padding:18px 24px;margin:38px 0;line-height:2.1;}
.mb-note .nt-ttl{font-weight:700;color:#e8920c;margin:0 0 14px;}
.mb-term{background:#eef4ff;border:1px solid #c7dbff;border-left:5px solid #3b82f6;border-radius:8px;padding:13px 18px;margin:28px 0;font-size:.92em;line-height:1.95;color:#1e3a5f;}
.mb-term b{color:#1d4ed8;}
.speech-balloon{line-height:1.95;}
.mb-cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:30px 0;}
.mb-cards .cd{background:#fff;border:1px solid #e4dbf6;border-left:5px solid #8b5cf6;border-radius:12px;padding:15px 17px;box-shadow:0 2px 8px rgba(76,29,149,.07);}
.mb-cards .cd .cd-t{display:block;color:#5b21b6;font-weight:800;font-size:1.02em;margin-bottom:6px;}
.mb-cards .cd .cd-d{font-size:.9em;color:#4b5563;line-height:1.65;}
.mb-code{background:#1e1533;color:#e9e2f7;font-family:Consolas,'DM Mono',monospace;font-size:.9em;line-height:1.6;padding:14px 18px;border-radius:10px;margin:20px 0;overflow-x:auto;white-space:pre-wrap;word-break:break-all;}
.mb-disc{font-size:.82em;color:#9ca3af;line-height:1.9;margin-top:46px;padding-top:18px;border-top:1px solid #e5e7eb;}
@media(max-width:600px){.mb-cards{grid-template-columns:1fr;}}
</style>
"""

def jp(t):
    return re.sub(r'。(?![」）】、\s<]|$)', '。<br>', t)

def P(t):    return f"\n<p>{jp(t)}</p>"
def LEAD(t): return f'\n<p class="mb-lead">{jp(t)}</p>'
def H2(t):   return f"\n\n<h2>{t}</h2>"
def FIG(svg, cap): return f'\n\n<figure class="mb-fig">{svg}<figcaption>{cap}</figcaption></figure>'
def CARDS(items):
    cs="".join(f'<div class="cd"><span class="cd-t">{t}</span><span class="cd-d">{jp(d)}</span></div>' for t,d in items)
    return f'\n\n<div class="mb-cards">{cs}</div>'
def BALLOON(t):
    return ('\n\n<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">'
            '<div class="speech-person"><figure class="speech-icon">'
            '<img class="speech-icon-image" src="https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png" alt="" width="1024" height="1024" /></figure></div>'
            f'<div class="speech-balloon">{jp(t)}</div></div>')

# ---- SVG figures ---------------------------------------------------------
FLOW_SVG = """<svg viewBox="0 0 780 300" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="会議コストBotの7アクション">
<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="#8b5cf6"/></marker></defs>
<g font-family="'Segoe UI','Meiryo UI',sans-serif" text-anchor="middle">
<rect x="18" y="20" width="744" height="48" rx="10" fill="#ede9fe" stroke="#8b5cf6" stroke-width="2"/>
<text x="390" y="42" font-size="13" font-weight="800" fill="#4c1d95">トリガー：新しいイベント（Outlook）</text>
<text x="390" y="60" font-size="11" fill="#6b7280">会議が作られた瞬間に発火する</text>
<line x1="390" y1="70" x2="390" y2="88" stroke="#8b5cf6" stroke-width="2.5" marker-end="url(#ar)"/>
<g>
<rect x="18" y="92" width="180" height="56" rx="9" fill="#fff" stroke="#c4b5fd" stroke-width="1.6"/><text x="108" y="116" font-size="12" font-weight="700" fill="#4c1d95">① 必須参加者の数</text><text x="108" y="134" font-size="10.5" fill="#6b7280">split + length</text>
<rect x="206" y="92" width="180" height="56" rx="9" fill="#fff" stroke="#c4b5fd" stroke-width="1.6"/><text x="296" y="116" font-size="12" font-weight="700" fill="#4c1d95">② 任意参加者の数</text><text x="296" y="134" font-size="10.5" fill="#6b7280">split + length</text>
<rect x="394" y="92" width="180" height="56" rx="9" fill="#fff" stroke="#c4b5fd" stroke-width="1.6"/><text x="484" y="116" font-size="12" font-weight="700" fill="#4c1d95">③ 合計人数</text><text x="484" y="134" font-size="10.5" fill="#6b7280">主催者＋必須＋任意</text>
<rect x="582" y="92" width="180" height="56" rx="9" fill="#fff" stroke="#c4b5fd" stroke-width="1.6"/><text x="672" y="116" font-size="12" font-weight="700" fill="#4c1d95">④ 会議時間（分）</text><text x="672" y="134" font-size="10.5" fill="#6b7280">ticks() で差を計算</text>
</g>
<line x1="390" y1="150" x2="390" y2="168" stroke="#8b5cf6" stroke-width="2.5" marker-end="url(#ar)"/>
<rect x="150" y="172" width="480" height="56" rx="10" fill="#f7f4fd" stroke="#8b5cf6" stroke-width="2"/>
<text x="390" y="196" font-size="13" font-weight="800" fill="#5b21b6">⑤ 推定コスト = 合計人数 × 時間（分） ×（時給 ÷ 60）</text>
<text x="390" y="216" font-size="11" fill="#6b7280">その会議に、いくらぶんの人件費が乗っているか</text>
<line x1="390" y1="230" x2="390" y2="248" stroke="#8b5cf6" stroke-width="2.5" marker-end="url(#ar)"/>
<rect x="250" y="252" width="280" height="40" rx="10" fill="#ede9fe" stroke="#8b5cf6" stroke-width="2"/>
<text x="390" y="277" font-size="12.5" font-weight="800" fill="#4c1d95">⑥ Teams に通知（Flowbot）</text>
</g></svg>"""

BEFORE_AFTER_SVG = """<svg viewBox="0 0 760 232" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="聞き方を変えたら結果が変わった">
<g font-family="'Segoe UI','Meiryo UI',sans-serif">
<rect x="10" y="16" width="360" height="200" rx="14" fill="#f6f7f9" stroke="#c8ccd4" stroke-width="2"/>
<text x="190" y="46" font-size="14" font-weight="800" fill="#475569" text-anchor="middle">「会議減らして」と頼む</text>
<rect x="34" y="64" width="312" height="40" rx="8" fill="#fff" stroke="#dde1e8"/><text x="190" y="89" font-size="12" fill="#374151" text-anchor="middle">→「優先度を見直しましょう」</text>
<rect x="34" y="112" width="312" height="40" rx="8" fill="#fff" stroke="#dde1e8"/><text x="190" y="137" font-size="12" fill="#374151" text-anchor="middle">一般論が返ってくるだけ</text>
<text x="190" y="188" font-size="12" fill="#6b7280" text-anchor="middle">会議はなくならない。だから噛み合わない</text>
<rect x="390" y="16" width="360" height="200" rx="14" fill="#f7f4fd" stroke="#8b5cf6" stroke-width="2.5"/>
<text x="570" y="46" font-size="14" font-weight="800" fill="#5b21b6" text-anchor="middle">「会議のコストを可視化したい」</text>
<rect x="414" y="64" width="312" height="40" rx="8" fill="#fff" stroke="#ddd0f2"/><text x="570" y="89" font-size="12" fill="#4c1d95" text-anchor="middle">→「Power Automateで作れますよ」</text>
<rect x="414" y="112" width="312" height="40" rx="8" fill="#fff" stroke="#ddd0f2"/><text x="570" y="137" font-size="12" fill="#4c1d95" text-anchor="middle">7アクションの設計まで提案</text>
<text x="570" y="188" font-size="12" font-weight="700" fill="#5b21b6" text-anchor="middle">作りたいものを言葉にしたら、手が動き出した</text>
</g></svg>"""

# ---- body ----------------------------------------------------------------
def build():
    b = []
    b.append('<div class="mb-body">')

    b.append(LEAD("2026年5月13日。「なんでもCopilot」のLT大会に、オンラインで登壇してきました。"))
    b.append(P("持ち時間は数分のライトニングトーク。ネタは、Power AutomateとCopilotで作った「会議コストBot」です。その週、自分のカレンダーが会議で埋まっていた、という個人的な事情から生まれたBotでした。"))
    b.append(P("この記事は、そのとき話した内容の記録です。Botの中身と、Copilotにどこまで任せて、どこは自分でやったのか。そのあたりを残しておきます。"))

    b.append('\n<div class="mb-cta pa"><p class="cta-ttl">登壇したイベント</p><p>「なんでもCopilot」は、日本でも最大級のCopilotコミュニティです。<br>この回はLT大会で、オンライン開催でした。</p>'
             f'<a class="mb-btn pa" href="{EVENT_URL}" target="_blank" rel="noopener">connpassのイベントページを見る</a></div>')

    b.append(H2("広島から、オンラインで手を挙げた"))
    b.append(P("イベントそのものの話から。なんでもCopilotは、Copilot好きが集まる大きめのコミュニティで、この回はLT大会でした。登壇者が数分ずつ、順番に話していく形式です。"))
    b.append(P("オンラインなので、広島にいてもそのまま出られます。移動はゼロ。ふだんPA45という勉強会を毎週オンラインでやっているので、この距離の近さは自分向きでした。思い立ったら手を挙げられる。それがオンラインLTのいいところです。"))
    b.append(P("短い時間で1ネタだけ、という潔さも自分に合っていました。今回持ち込んだのは、直前に自分が引っかかっていた「会議だらけ問題」。等身大のまま話せそうだったので、これにしました。"))

    b.append(H2("発端は、会議42本のカレンダー"))
    b.append(P("話の入り口は、ある日の自分のカレンダーです。開いたら、その週の会議が42本ありました。隙間がほぼない。"))
    b.append(P("そこへ、追い討ちのように新しい会議の招集が届きます。中身を見ると、必須参加者70人、任意参加者0人、時間は120分。必須が70人で任意がゼロ、というのが引っかかりました。この120分、本当に全員ぶん要るんだろうか、と。"))
    b.append(BALLOON("会議そのものを否定したいわけではないんです。「これ、本当に全員いるんだっけ？」と一度だけ立ち止まりたい。その程度の話でした。"))

    b.append(H2("最初の頼み方は、失敗だった"))
    b.append(P("はじめは、思いついたままの言葉でCopilotへ頼みました。「会議を減らしたいんですけど」。"))
    b.append(P("返ってきたのは「優先度を見直して、必要な会議だけに絞りましょう」。正論です。でも、欲しかった答えではありませんでした。"))
    b.append(P("会議は、こちらの都合ではなくなりません。だから「減らせ」と言われても現場は動けない。やりたかったのは誰かを責めることではなく、「呼ぶ前にひと呼吸」を自然に挟むことでした。頼み方が、作りたいものとズレていたわけです。"))

    b.append(H2("聞き方を変えたら、手が動き出した"))
    b.append(P("そこで言い方を変えます。「会議を減らしたい」ではなく、「会議のコストを可視化したい」。"))
    b.append(P("今度は具体的な答えが返ってきました。「Power Automateで作れますよ」「Outlookのトリガーと、7つのアクションでいけます」。やりたいことを、作れる形の言葉に置き換えたら、話が前に進みました。"))
    b.append(FIG(BEFORE_AFTER_SVG, "▲ 同じ悩みでも、頼み方を変えると返ってくるものが変わった"))
    b.append('\n<div class="mb-point">「〇〇したい」で止めず、<span class="hl-marker">「何を作りたいか」まで言葉にする</span>。それだけでCopilotは設計まで手伝ってくれました。この日いちばん伝えたかったのは、たぶんここです。</div>')

    b.append(H2("中身：Outlookトリガー＋7アクションの会議コストBot"))
    b.append(P("Copilotが出してきたのは、こういう流れのフローです。会議が作られた瞬間に、その会議の推定コストを計算して、Teamsへ飛ばします。"))
    b.append(FIG(FLOW_SVG, "▲ 会議コストBotの全体像（Outlookトリガー＋7アクション）"))
    b.append('\n<div class="mb-step"><div class="st-ttl"><span class="st-no">7</span>会議コストBotのアクション</div><ol>'
             '<li><b>トリガー：新しいイベント（Outlook）</b>／会議が作られた瞬間に発火します</li>'
             '<li><b>必須参加者の数</b>を数える（split と length の組み合わせ）</li>'
             '<li><b>任意参加者の数</b>を数える（同じやり方）</li>'
             '<li><b>合計人数</b>を出す（主催者＋必須＋任意）</li>'
             '<li><b>会議時間（分）</b>を出す（ticks で開始と終了の差を計算）</li>'
             '<li><b>推定コスト</b>を出す（合計人数 × 時間 ×（時給 ÷ 60））</li>'
             '<li><b>Teamsへ通知</b>（Flowbotから自分のチャットへ）</li>'
             '</ol></div>')
    b.append(P("時給は、ここでは一般的な例として置いています。職場ごとに変わる数字ですし、狙いはあくまで「目安を見せる」こと。だから、ここは厳密でなくて構いません。"))

    b.append(H2("式が読めなくても、動く"))
    b.append(P("このBotの肝は、会議の長さを「分」に直すところです。ここでCopilotが出してきたのが、ticks を使った式でした。"))
    b.append('\n<div class="mb-term"><b>ticks() とは</b>：日時を「とても細かい単位の数値」に変換する関数です。<br>'
             '開始時刻と終了時刻をそれぞれ数値に直して引き算し、決まった数で割ると「分」に戻せます。<br>'
             'Power Automateで「時間の差」を出したいときの、定番のやり方です。</div>')
    b.append('\n<div class="mb-code">div(sub(ticks(終了), ticks(開始)), 600000000)</div>')
    b.append(P("この式、その場ではすぐに読めませんでした。それでも貼り付けたら動く。仕組みの理解は後から追いつけばよくて、まず動くものが手に入る。Copilotと作るときの感覚は、だいたいこれです。"))

    b.append(H2("会議は減らない。でも空気は変わった"))
    b.append(P("Botを動かしても、会議の数そのものは減りません。そこはそのまま話しました。"))
    b.append(P("変わったのは、会議を設定するときの空気のほうです。人数と時間から「この会議はこれくらいのコスト」と数字が出ると、「本当にこの人数？」「120分もいる？」と、招集する前に一度考える。責める言葉は一つもないのに、手が止まる瞬間が生まれます。"))
    b.append('\n<div class="mb-point">数字を見せると、人は立ち止まります。<br><span class="hl-marker">「減らせ」と言うより、コストを見せるほうが効きました。</span></div>')

    b.append(H2("自分が考える × Copilotが手伝う"))
    b.append(P("この一件で、自分とCopilotの分担がはっきりしました。全部を自分で作る必要はない。かといって、全部をCopilotに任せることもできない。境目は、意外とくっきりしていました。"))
    b.append(CARDS([
        ("自分にしかできない：気づく", "「会議が多すぎる」と肌で感じるのは、その現場にいる自分だけ"),
        ("自分にしかできない：発想", "「コストを見せたい」「呼ぶ前にひと呼吸」という発想は人間側から出ます"),
        ("Copilotが得意：式と構造", "ticks や split の組み合わせ、7アクション分の設計は、聞けばすぐ返ってきます"),
        ("Copilotが得意：説明", "読めない式も説明してくれるので、そのまま学習にもなる"),
    ]))
    b.append('\n<div class="mb-point">アイデアは現場から、実装はCopilotと。<br>このLTで、いちばん残したかったのはこの一行でした。</div>')

    b.append(H2("この日、持ち帰ったこと"))
    b.append("\n<ul>"
             "<li>Copilotは「どう作るか」だけでなく「何を作るか」も提案してくれる</li>"
             "<li>頼み方を「何を作りたいか」まで言葉にすると、設計まで返ってくる</li>"
             "<li>式が読めなくても、まず動く。理解は後から追いつけばいい</li>"
             "<li>「減らせ」と言うより、数字（コスト）を見せるほうが人は動く</li>"
             "<li>気づきは現場から、実装はCopilotと分担する</li>"
             "</ul>")
    b.append(P("オンラインのLTは、広島からでも気軽に手を挙げられます。次の機会があれば、また小さいネタを1つ持って出たいと思っています。"))

    b.append(f'\n<div class="mb-cta pa"><p class="cta-ttl">当日のLTスライド</p><p>登壇で使ったスライド（PowerPoint）を公開しています。</p>'
             f'<a class="mb-btn pa" href="{SLIDE_URL}" target="_blank" rel="noopener">LTスライドをダウンロード</a></div>')

    b.append('\n<div class="mb-cta pa"><p class="cta-ttl">毎週やっているPA45もあります</p>'
             '<p>Power Automateを45分だけ、手を動かして1つ完成させて終わる勉強会です。<br>木曜の夜にオンラインでやっています。</p>'
             '<a class="mb-btn pa" href="https://powerautomate-create.connpass.com/" target="_blank" rel="noopener">次回のPA45を見る（無料）</a>'
             '<span class="cta-sub">参加無料／途中入退室OK・見るだけ参加も歓迎です</span></div>')
    b.append('\n<p>過去回の資料やアーカイブは<a href="https://www.automate136.com/pa45/">PA45のページ</a>にまとめています。</p>')
    b.append('\n<div class="mb-cta yt"><p class="cta-ttl">&#x25b6; 講座の中身は動画でも見られます</p><p>PA45の各回は全編をYouTubeに置いています。</p>'
             '<a class="mb-btn yt" href="https://www.youtube.com/@hu3663" target="_blank" rel="noopener">PA45のYouTubeチャンネルを見る</a></div>')

    b.append('\n<p class="mb-disc">この記事は、2026年5月13日のイベントで登壇した個人の記録です。イベントの公式な記録ではありません。<br>'
             '本文中の会議コストや時給は、仕組みを説明するための一般的な例であり、特定の組織の数値ではありません。</p>')
    b.append("\n</div>")
    return CSS + "\n\n" + "".join(b)

def main():
    content = build()
    (HERE / "article.html").write_text(content, encoding="utf-8")
    n = len(re.sub(r'<[^>]+>', '', content))
    print(f"article.html written / 本文タグ除去 約{n}字")

    if "--push" not in sys.argv:
        print("（ローカル生成のみ。--push でWordPress下書き作成）")
        return

    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1); env[k.strip()] = v.strip()
    WP = env["WP_URL"].rstrip("/")
    H = {"Authorization": "Basic " + base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()}

    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    payload = {"title": TITLE, "slug": SLUG, "status": "draft", "content": content, "categories": CATS}
    if state.get("post_id"):
        r = requests.post(f"{WP}/wp-json/wp/v2/posts/{state['post_id']}", headers=H, json=payload, timeout=120)
        r.raise_for_status(); pid = state["post_id"]; print("UPDATED", pid)
    else:
        r = requests.post(f"{WP}/wp-json/wp/v2/posts", headers=H, json=payload, timeout=120)
        r.raise_for_status(); pid = r.json()["id"]; state["post_id"] = pid; print("CREATED", pid)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print("編集URL :", f"{WP}/wp-admin/post.php?post={pid}&action=edit")
    print("プレビュー:", f"{WP}/?p={pid}&preview=true")

if __name__ == "__main__":
    main()

"""
各回のアンケート結果ページを作る。

data/surveys/vol-NN.json と data/insights.json から
achievements/insights/vol-NN.html を生成する。
ページの外枠（ヘッダ・フッタ）は can-do.html から借りるので、
サイトのデザインを変えてもここは追従する。

  python scripts/build-vol-survey-pages.py          # 全回
  python scripts/build-vol-survey-pages.py 13       # 1回だけ

数字は手打ちしない。すべて JSON から計算する。
"""

import json
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURVEY = ROOT / "data" / "surveys"
INSIGHTS = ROOT / "data" / "insights.json"
OUTDIR = ROOT / "achievements" / "insights"
SHELL = OUTDIR / "can-do.html"
SITE = "https://haru-powerplatform.github.io/pa45"

E = html.escape


def shell():
    """can-do.html から <header> までと <footer> 以降を取り出す"""
    s = SHELL.read_text(encoding="utf-8")
    head = s[: s.index("</header>") + len("</header>")]
    foot = s[s.index("<footer"):]
    return head, foot


def bar(label, count, total, color="#2563eb"):
    pct = round(count / total * 100, 1) if total else 0.0
    return (
        '<div class="vs-row">'
        f'<div class="vs-lbl">{E(label)}</div>'
        f'<div class="vs-track"><span style="width:{pct}%;background:{color};"></span></div>'
        f'<div class="vs-num">{count}件<small>{pct}%</small></div>'
        "</div>")


CSS = """
.vs-wrap{max-width:860px;margin:0 auto;padding:0 18px;}
.vs-card{background:#fff;border:1px solid #e3e6eb;border-radius:14px;padding:20px 24px;margin:16px 0;
box-shadow:0 2px 10px rgba(15,23,42,.05);}
.vs-q{font-weight:800;color:#0b2a5e;margin:0 0 14px;font-size:15px;}
.vs-row{display:flex;align-items:center;gap:12px;margin:9px 0;font-size:13.5px;}
.vs-lbl{flex:0 0 40%;line-height:1.6;}
.vs-track{flex:1;height:12px;background:#eef2f7;border-radius:99px;overflow:hidden;}
.vs-track span{display:block;height:100%;border-radius:99px;}
.vs-num{flex:0 0 92px;text-align:right;font-variant-numeric:tabular-nums;font-weight:700;color:#0b2a5e;}
.vs-num small{display:block;font-weight:500;color:#64748b;font-size:11px;}
.vs-kpi{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin:18px 0;}
.vs-kpi div{background:#fff;border:1px solid #e3e6eb;border-radius:12px;padding:14px 16px;text-align:center;}
.vs-kpi b{display:block;font-size:26px;color:#1d4ed8;font-variant-numeric:tabular-nums;line-height:1.25;}
.vs-kpi span{font-size:12px;color:#64748b;}
.vs-voice{background:#f8fafc;border-left:4px solid #93c5fd;border-radius:0 10px 10px 0;
padding:12px 16px;margin:10px 0;font-size:13.5px;line-height:1.95;white-space:pre-wrap;}
.vs-nav{display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 10px;}
.vs-nav a{flex:1;min-width:190px;background:#eff4ff;border:1px solid #cfe0fb;border-radius:12px;
padding:12px 16px;text-decoration:none;color:#14528f;font-weight:700;font-size:13.5px;line-height:1.6;}
.vs-nav a small{display:block;color:#6b83a8;font-weight:500;font-size:11.5px;}
.vs-lead{font-size:14px;line-height:2;color:#334155;margin:14px 0 0;}
"""


def page(vol, sv, ses, prev_s, next_s, head, foot):
    theme = ses.get("theme", "")
    date = ses.get("date", sv.get("date", ""))
    parts = ses.get("participants") or 0
    res = sv.get("total_responses") or 0
    und = sv.get("understanding_pct")
    use = sv.get("usefulness_pct")

    kpi = "".join([
        f'<div><b>{parts}名</b><span>参加者</span></div>' if parts else "",
        f'<div><b>{res}件</b><span>アンケート回答</span></div>',
        f'<div><b>{und}%</b><span>理解できた</span></div>' if und is not None else "",
        f'<div><b>{use}%</b><span>役立ちそう</span></div>' if use is not None else "",
    ])

    def block(title, d, color):
        if not d:
            return ""
        tot = sum(d.values())
        rows = "".join(bar(k, v, tot, color) for k, v in
                       sorted(d.items(), key=lambda x: -x[1]) if v)
        return f'<div class="vs-card"><div class="vs-q">{title}</div>{rows}</div>'

    can = sv.get("can_do") or {}
    can_block = ""
    if can:
        rows = "".join(bar(k, v, res, "#16a34a") for k, v in
                       sorted(can.items(), key=lambda x: -x[1]) if v)
        can_block = (
            '<div class="vs-card"><div class="vs-q">&#x2705; この45分でできるようになったこと'
            '（複数選択・回答者数が母数）</div>' + rows +
            '<p class="vs-lead">「意味が分かった」で止まるのか、「自分で使える」まで届いたのか。'
            'ここが次の回のテーマを決める材料になります。</p></div>')

    voices = ""
    cm = [c for c in (sv.get("comments") or []) if str(c).strip()]
    if cm:
        voices = ('<p class="section-label" style="margin-top:26px;">参加者の自由記述'
                  f'（{len(cm)}件・原文のまま）</p><div class="vs-card">'
                  + "".join(f'<div class="vs-voice">{E(str(c).strip())}</div>' for c in cm)
                  + "</div>")

    nav = []
    if prev_s:
        nav.append(f'<a href="vol-{prev_s["vol"]:02d}.html"><small>&#x25c0; 前の回</small>'
                   f'第{prev_s["vol"]}回 {E(prev_s.get("theme",""))[:28]}</a>')
    if next_s:
        nav.append(f'<a href="vol-{next_s["vol"]:02d}.html"><small>次の回 &#x25b6;</small>'
                   f'第{next_s["vol"]}回 {E(next_s.get("theme",""))[:28]}</a>')
    nav_html = f'<div class="vs-nav">{"".join(nav)}</div>' if nav else ""

    body = f"""
<section class="ins-hero">
  <div class="container">
    <span class="ins-eyebrow">PA45 <b>アンケート結果</b> ｜ 第{vol}回 &#x1f4ca;</span>
    <h1 class="ins-h1">第{vol}回 アンケート結果<small>{E(theme)}</small></h1>
    <div class="ins-meta">{E(date)} 開催／回答{res}件</div>
  </div>
</section>

<section class="section"><div class="vs-wrap">
  <div class="vs-kpi">{kpi}</div>
  {block("&#x1f4d8; 今日の内容は理解できましたか", sv.get("understanding"), "#2563eb")}
  {block("&#x1f4bc; 業務に役立ちそうですか", sv.get("usefulness"), "#0ea5e9")}
  {can_block}
  {voices}
  {nav_html}
  <div class="vs-nav">
    <a href="index.html"><small>まとめ</small>全回のアンケート集計を見る</a>
    <a href="can-do.html"><small>成長の記録</small>できるようになったことランキング</a>
  </div>
</div></section>
"""
    title = f"第{vol}回 アンケート結果｜{theme}｜PA45"
    desc = (f"PA45 第{vol}回「{theme}」のアンケート結果。"
            f"回答{res}件、理解できた{und}%、役立ちそう{use}%。"
            "参加者ができるようになったことと自由記述をそのまま公開しています。")

    h = head
    h = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", h, count=1, flags=re.S)
    h = re.sub(r'(<meta name="description" content=")[^"]*(")',
               lambda m: m.group(1) + E(desc) + m.group(2), h, count=1)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
               lambda m: m.group(1) + E(title) + m.group(2), h, count=1)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
               lambda m: m.group(1) + E(desc) + m.group(2), h, count=1)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
               lambda m: m.group(1) + f"{SITE}/achievements/insights/vol-{vol:02d}.html" + m.group(2),
               h, count=1)
    h = h.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    return h + body + foot


def main():
    ins = json.loads(INSIGHTS.read_text(encoding="utf-8"))
    sessions = {s["vol"]: s for s in ins["sessions"]}
    head, foot = shell()

    only = [int(a) for a in sys.argv[1:] if a.isdigit()]
    made = 0
    vols = sorted(sessions)
    for vol in vols:
        if only and vol not in only:
            continue
        sp = SURVEY / f"vol-{vol:02d}.json"
        if not sp.exists():
            print(f"  第{vol}回: アンケートJSONなし → スキップ")
            continue
        sv = json.loads(sp.read_text(encoding="utf-8"))
        i = vols.index(vol)
        prev_s = sessions[vols[i - 1]] if i > 0 else None
        next_s = sessions[vols[i + 1]] if i + 1 < len(vols) else None
        out = OUTDIR / f"vol-{vol:02d}.html"
        out.write_text(page(vol, sv, sessions[vol], prev_s, next_s, head, foot),
                       encoding="utf-8")
        made += 1
        print(f"  [OK] {out.name}  回答{sv.get('total_responses')}件 / "
              f"自由記述{len(sv.get('comments') or [])}件")
    print(f"[OK] {made} ページ")


if __name__ == "__main__":
    main()

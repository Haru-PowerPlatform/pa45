"""
AB-730 勉強会のアンケート結果ページを作る（PA45 の回とは別扱い）。

data/surveys/ab730-NN.json から achievements/insights/ab730-NN.html を生成する。
外枠と見た目は PA45 の回別ページ（build-vol-survey-pages.py）と同じものを使う。
PA45 の回番号・累計（insights.json）には入れない。

  python scripts/build-ab730-survey-page.py          # 全回
  python scripts/build-ab730-survey-page.py 1        # 1回だけ

数字は手打ちしない。すべて JSON から計算する。
個人情報の入った回答 Excel はリポジトリに置かない（JSON は公開してよい集計と記述だけ）。
職場の困りごとの設問は個人的な内容になるので、JSON にもページにも入れない（はる 2026-11-26）。
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SURVEY = ROOT / "data" / "surveys"
OUTDIR = ROOT / "achievements" / "insights"
SITE = "https://haru-powerplatform.github.io/pa45"

_spec = importlib.util.spec_from_file_location(
    "vsp", Path(__file__).with_name("build-vol-survey-pages.py"))
vsp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vsp)
E, bar, CSS, shell = vsp.E, vsp.bar, vsp.CSS, vsp.shell

EXTRA_CSS = """
.vs-note{font-size:12px;color:#64748b;line-height:1.8;margin:8px 0 0;}
.vs-sub{font-size:12.5px;color:#475569;margin:-6px 0 12px;}
.vs-next{background:linear-gradient(135deg,#fff7ed,#ffedd5);border:2px solid #fb923c;border-radius:14px;
padding:18px 22px;margin:18px 0;text-align:center;}
.vs-next-h{font-weight:800;color:#9a3412;font-size:15.5px;margin:0 0 4px;}
.vs-next-d{font-size:14px;color:#7c2d12;margin:0 0 12px;font-variant-numeric:tabular-nums;}
.vs-next-btn{display:inline-block;background:#ea580c;color:#fff !important;font-weight:800;font-size:16px;
padding:13px 30px;border-radius:999px;text-decoration:none;box-shadow:0 4px 12px rgba(234,88,12,.35);}
.vs-next-btn:hover{background:#c2410c;}
.vs-next-s{font-size:12.5px;color:#7c2d12;margin:12px 0 0;line-height:1.9;}
.vs-next-s a{color:#9a3412;font-weight:700;}
"""

# connpass のグループ（フォローすると次回のお知らせが届く）
GROUP_URL = "https://powerautomate-create.connpass.com/"


def next_cta(sv):
    """次の回の参加登録ボタン。JSON の next（label/date/url）が無ければ出さない。
    アンケート結果のページには毎回、次の回の connpass とグループへのリンクを入れる決まり。"""
    nx = sv.get("next")
    if not nx:
        return ""
    return (
        '<div class="vs-next">'
        f'<p class="vs-next-h">次回 AB-730 勉強会 {E(nx["label"])}</p>'
        f'<p class="vs-next-d">{E(nx["date"])}（オンライン・無料）</p>'
        f'<a class="vs-next-btn" href="{E(nx["url"])}" target="_blank" rel="noopener">'
        f'connpass で{E(nx["label"])}に参加登録する</a>'
        f'<p class="vs-next-s">第1回に出ていなくても参加できます。<br>'
        f'<a href="{GROUP_URL}" target="_blank" rel="noopener">connpass のグループ</a>'
        'をフォローすると、次の回のお知らせが届きます。</p>'
        '</div>')


def block(title, d, total, color, sub=""):
    rows = "".join(bar(k, v, total, color) for k, v in d.items() if v)
    s = f'<div class="vs-sub">{sub}</div>' if sub else ""
    return f'<div class="vs-card"><div class="vs-q">{title}</div>{s}{rows}</div>'


def voices(label, items):
    if not items:
        return ""
    return (f'<p class="section-label" style="margin-top:26px;">{label}（{len(items)}件・原文のまま）</p>'
            '<div class="vs-card">'
            + "".join(f'<div class="vs-voice">{E(t)}</div>' for t in items)
            + "</div>")


def page(sv, head, foot):
    n = sv["round"]
    res = sv["total_responses"]
    und, use = sv["understanding"], sv["usefulness"]

    kpi = "".join([
        f'<div><b>{res}件</b><span>アンケート回答</span></div>',
        f'<div><b>{und["pct"]}%</b><span>理解しやすかった</span></div>',
        f'<div><b>{use["pct"]}%</b><span>役立ちそう</span></div>',
    ])
    star_sub = "★5段階の平均を％にした値（{avg}／5）。★4以上は {top2}%。"

    body = f"""
<section class="ins-hero">
  <div class="container">
    <span class="ins-eyebrow">AB-730 勉強会 <b>アンケート結果</b> ｜ 第{n}回 &#x1f4ca;</span>
    <h1 class="ins-h1">AB-730 勉強会 第{n}回 アンケート結果<small>Microsoft 365 Copilot の認定試験 AB-730 に向けた勉強会</small></h1>
    <div class="ins-meta">{E(sv["date"])} 開催／回答{res}件</div>
  </div>
</section>

<section class="section"><div class="vs-wrap">
  <p class="vs-lead">PA45（Power Automate のハンズオン）とは別に開いている勉強会です。PA45 の回数・累計には入れていません。</p>
  <div class="vs-kpi">{kpi}</div>
  {next_cta(sv)}
  {block("&#x1f4d8; 今日の内容は理解しやすかったですか", und["dist"], res, "#2563eb",
         star_sub.format(avg=und["avg"], top2=und["top2_pct"]))}
  {block("&#x1f4bc; 試験勉強や業務に役立ちそうですか", use["dist"], res, "#0ea5e9",
         star_sub.format(avg=use["avg"], top2=use["top2_pct"]))}
  {block("&#x1f4dd; AB-730 の受験予定", sv["exam_plan"], res, "#7c3aed")}
  {voices("参加者の感想", sv.get("comments"))}
  <p class="vs-note">掲載ポリシー：氏名・メールアドレスは載せていません。自由記述は感想だけを載せ、名乗りなど個人が分かる記述は外しています。職場の困りごとの設問は、個人的な内容になるため載せていません。</p>
  {next_cta(sv)}
  <div class="vs-nav">
    <a href="../index.html#ab730"><small>活動の記録</small>実績ページにもどる</a>
    <a href="index.html"><small>PA45</small>PA45 のアンケート集計を見る</a>
  </div>
</div></section>
"""
    title = f"AB-730 勉強会 第{n}回 アンケート結果｜PA45"
    desc = (f"AB-730 勉強会 第{n}回のアンケート結果。回答{res}件、"
            f"理解しやすかった{und['pct']}%、役立ちそう{use['pct']}%。"
            "受験予定と参加者の感想をそのまま公開しています。")
    url = f"{SITE}/achievements/insights/ab730-{n:02d}.html"

    h = head
    h = re.sub(r"<title>.*?</title>", f"<title>{E(title)}</title>", h, count=1, flags=re.S)
    for pat, val in [
        (r'(<meta name="description" content=")[^"]*(")', desc),
        (r'(<meta property="og:title" content=")[^"]*(")', title),
        (r'(<meta property="og:description" content=")[^"]*(")', desc),
        (r'(<meta name="twitter:title" content=")[^"]*(")', title),
        (r'(<meta name="twitter:description" content=")[^"]*(")', desc),
    ]:
        h = re.sub(pat, lambda m, v=val: m.group(1) + E(v) + m.group(2), h, count=1)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
               lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
               lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = h.replace("</head>", f"<style>{CSS}{EXTRA_CSS}</style>\n</head>", 1)
    return h + body + foot


def main():
    head, foot = shell()
    only = [int(a) for a in sys.argv[1:] if a.isdigit()]
    made = 0
    for sp in sorted(SURVEY.glob("ab730-*.json")):
        sv = json.loads(sp.read_text(encoding="utf-8"))
        if only and sv["round"] not in only:
            continue
        out = OUTDIR / f"ab730-{sv['round']:02d}.html"
        out.write_text(page(sv, head, foot), encoding="utf-8")
        made += 1
        print(f"  [OK] {out.name}  回答{sv['total_responses']}件 / 感想{len(sv.get('comments') or [])}件"
              )
    print(f"[OK] {made} ページ")


if __name__ == "__main__":
    main()

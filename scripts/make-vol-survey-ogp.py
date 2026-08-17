"""
PA45 回別アンケート結果ページの OGP画像ジェネレーター（1200x630）

data/surveys/vol-NN.json の数字をそのまま流し込むので、parse-survey.py を回したあとに
実行すれば理解度・役立ち度・回答数が最新になります。

使い方:
  python scripts/make-vol-survey-ogp.py 23
  python scripts/make-vol-survey-ogp.py 23 --title "Excelの「答え」で\nフローが分かれた？" \
      --sub "Officeスクリプトの戻り値で、フローを自動で振り分ける。" --quote "「〜」"

出力: assets/ogp/pa45-volNN-survey-ogp.png
回ごとの文言は VOL_TEXT に貯めておく（引数で上書き可）。
"""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SURVEY_DIR = ROOT / "data" / "surveys"
OUT_DIR = ROOT / "assets" / "ogp"

CHROME_CANDIDATES = [
    Path(r"C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path(r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path(r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]

# 回ごとの見出し・サブ・引用（\n で改行）
VOL_TEXT = {
    22: {
        "title": "Excelの手作業、\n自動化してどうだった？",
        "sub": "OfficeスクリプトとCopilotで、Excelの繰り返しをまるごと自動化。",
        "quote": "「実務にすぐ活かせる濃い内容でした」",
    },
    23: {
        "title": "Excelの「答え」で、\nフローは分かれたか？",
        "sub": "Officeスクリプトの戻り値を条件にして、経費を自動で振り分ける回。",
        "quote": "「今まで扱ったことが無いフローだったので，勉強になりました！」",
    },
}


def find_chrome():
    for p in CHROME_CANDIDATES:
        if p.exists():
            return p
    raise SystemExit("Chrome / Edge が見つかりません。CHROME_CANDIDATES を確認してください。")


TEMPLATE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ width:1200px; height:630px; overflow:hidden; position:relative; color:#fff;
    font-family:'Noto Sans JP','Yu Gothic UI','Meiryo',sans-serif;
    background:linear-gradient(135deg,#0a2a4d 0%,#14528f 55%,#1f6fc0 100%); }}
  .glow {{ position:absolute; border-radius:50%; background:rgba(255,255,255,.05); }}
  .g1 {{ width:560px; height:560px; right:-140px; top:-170px; }}
  .g2 {{ width:400px; height:400px; right:60px; bottom:-190px; }}
  .wrap {{ position:relative; padding:44px 56px; height:100%; display:flex; flex-direction:column; }}
  .pill {{ display:inline-flex; align-items:center; gap:10px; align-self:flex-start;
    font-size:22px; font-weight:700; letter-spacing:.02em;
    background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.32);
    padding:9px 22px; border-radius:999px; }}
  .brandmark {{ position:absolute; right:56px; top:44px; display:flex; align-items:center; gap:14px; }}
  .brandmark .ic {{ width:62px; height:62px; border-radius:16px; display:flex; align-items:center; justify-content:center;
    background:linear-gradient(135deg,#3b82f6 0%,#6366f1 100%); box-shadow:0 8px 22px rgba(0,0,0,.28); }}
  .brandmark .ic svg {{ width:32px; height:32px; }}
  .brandmark .tx b {{ display:block; font-size:30px; font-weight:900; line-height:1.1; }}
  .brandmark .tx span {{ display:block; font-size:16px; font-weight:700; color:#bcd8f5; margin-top:4px; letter-spacing:.04em; }}
  h1 {{ font-size:{tsize}px; font-weight:900; line-height:1.22; letter-spacing:-.02em; margin-top:26px; white-space:pre-line; }}
  .sub {{ font-size:25px; font-weight:700; color:#cfe3fa; margin-top:18px; line-height:1.45; }}
  .stats {{ display:flex; gap:16px; margin-top:auto; }}
  .stat {{ background:rgba(255,255,255,.13); border:1px solid rgba(255,255,255,.24);
    border-radius:18px; padding:16px 26px; min-width:186px; }}
  .stat .n {{ font-size:48px; font-weight:900; line-height:1; letter-spacing:-.02em; }}
  .stat .n i {{ font-size:24px; font-style:normal; margin-left:2px; }}
  .stat .l {{ font-size:17px; font-weight:700; color:#cfe3fa; margin-top:9px; }}
  .quote {{ border-left:4px solid #ffe08a; padding-left:16px; font-size:21px; line-height:1.5;
    color:rgba(255,255,255,.94); margin-top:26px; font-weight:500; }}
  .foot {{ display:flex; justify-content:space-between; align-items:flex-end; margin-top:24px; }}
  .foot .brand {{ font-size:24px; font-weight:900; }}
  .foot .url {{ font-size:20px; font-weight:700; color:#ffe08a; }}
</style></head>
<body>
  <div class="glow g1"></div><div class="glow g2"></div>
  <div class="brandmark">
    <div class="ic"><svg viewBox="0 0 24 24" fill="#fff"><path d="M13.5 2 4 14h6l-1.5 8L20 10h-6.5z"/></svg></div>
    <div class="tx"><b>Power Automate</b><span>PA45 コミュニティ</span></div>
  </div>
  <div class="wrap">
    <div class="pill">PA45　第{vol}回 参加者アンケート 📋</div>
    <h1>{title}</h1>
    <div class="sub">{sub}</div>
    <div class="stats">{stats}</div>
    {quote}
    <div class="foot"><div class="brand">Power Automate 45</div><div class="url">automate136.com/pa45</div></div>
  </div>
</body></html>
"""


def stat_html(n, unit, label):
    return (f'<div class="stat"><div class="n">{n}<i>{unit}</i></div>'
            f'<div class="l">{label}</div></div>')


def build(vol, title, sub, quote, tsize):
    data = json.loads((SURVEY_DIR / f"vol-{vol:02d}.json").read_text(encoding="utf-8"))
    stats = [
        (round(data["understanding_pct"]), "%", "内容が理解できた"),
        (round(data["usefulness_pct"]), "%", "業務に役立ちそう"),
        (data["total_responses"], "名", "回答"),
    ]
    return TEMPLATE.format(
        vol=vol, title=title, sub=sub, tsize=tsize,
        stats="".join(stat_html(*x) for x in stats),
        quote=f'<div class="quote">{quote}</div>' if quote else "",
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vol", type=int)
    ap.add_argument("--title")
    ap.add_argument("--sub")
    ap.add_argument("--quote")
    ap.add_argument("--tsize", type=int, default=62)
    args = ap.parse_args()

    preset = VOL_TEXT.get(args.vol, {})
    title = (args.title or preset.get("title") or f"第{args.vol}回のアンケート結果").replace("\\n", "\n")
    sub = args.sub or preset.get("sub", "")
    quote = args.quote or preset.get("quote", "")

    html = build(args.vol, title, sub, quote, args.tsize)
    out = OUT_DIR / f"pa45-vol{args.vol}-survey-ogp.png"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "ogp.html"
        src.write_text(html, encoding="utf-8")
        subprocess.run([
            str(find_chrome()), "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--window-size=1200,630",
            "--virtual-time-budget=6000", f"--screenshot={out}", src.as_uri(),
        ], check=True, capture_output=True)
    print(f"[OK] {out}")


if __name__ == "__main__":
    main()

"""
PA45 サイト全体の OGP画像ジェネレーター（1200x630）

各ページのアイキャッチを HTML → ヘッドレスChrome → PNG で書き出します。
数字は data/insights.json から読むので、新しい回を取り込んで build-insights.py を
回したあとに再実行すれば、カードの数字も自動で最新になります。

X（Twitter）にリンクを貼ったときに出るカードはページごとに違う絵にしたいので、
ページ単位でテーマ色と数字を変えています。

使い方:
  python scripts/build-insights.py
  python scripts/make-insight-ogp.py                 # 全部
  python scripts/make-insight-ogp.py numbers videos  # 指定した分だけ
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "insights.json"
OUT_DIR = ROOT / "assets" / "ogp"

CHROME_CANDIDATES = [
    Path(r"C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path(r"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"),
    Path(r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
]

# テーマ（ページのアクセント色と合わせる）
THEMES = {
    "green":  {"d": "#043a26", "m": "#0b6b46", "a": "#0e9f6e", "l": "#c9f7e2", "y": "#ffe9a8"},
    "blue":   {"d": "#0b2a5e", "m": "#1d4ed8", "a": "#2563eb", "l": "#cfe0fb", "y": "#ffe08a"},
    "amber":  {"d": "#5c2708", "m": "#9a3d0c", "a": "#b45309", "l": "#fbe3c2", "y": "#ffeeb0"},
    "purple": {"d": "#231d6b", "m": "#3f37c9", "a": "#4f46e5", "l": "#d8d5fb", "y": "#ffe9a8"},
    "red":    {"d": "#5b1010", "m": "#9f1239", "a": "#dc2626", "l": "#fcd6d6", "y": "#ffe9a8"},
    "teal":   {"d": "#062f2b", "m": "#0d6d63", "a": "#0d9488", "l": "#c3f1ea", "y": "#ffe9a8"},
    "slate":  {"d": "#0f172a", "m": "#243b56", "a": "#3f5f80", "l": "#cbd9e8", "y": "#ffe08a"},
    "sky":    {"d": "#0a3550", "m": "#0369a1", "a": "#0ea5e9", "l": "#c9e8fa", "y": "#ffe08a"},
    "rose":   {"d": "#4c0519", "m": "#9f1239", "a": "#e11d48", "l": "#fbd0dc", "y": "#ffe9a8"},
    "cyan":   {"d": "#083344", "m": "#0e7490", "a": "#06b6d4", "l": "#c5f0f8", "y": "#ffe9a8"},
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
  body {{ width:1200px; height:630px; overflow:hidden;
    font-family:'Noto Sans JP','Yu Gothic UI','Meiryo',sans-serif; color:#fff;
    background:linear-gradient(135deg,{d} 0%,{m} 55%,{a} 100%); position:relative; }}
  .glow {{ position:absolute; border-radius:50%; background:rgba(255,255,255,.06); }}
  .g1 {{ width:520px; height:520px; right:-120px; top:-160px; }}
  .g2 {{ width:360px; height:360px; right:120px; bottom:-180px; }}
  .wrap {{ position:relative; padding:46px 56px; height:100%; display:flex; flex-direction:column; }}
  .pill {{ display:inline-flex; align-items:center; gap:10px; align-self:flex-start;
    font-size:22px; font-weight:700; letter-spacing:.02em;
    background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.32);
    padding:9px 22px; border-radius:999px; }}
  .pill b {{ color:{y}; }}
  h1 {{ font-size:{tsize}px; font-weight:900; line-height:1.2; letter-spacing:-.02em; margin-top:24px; }}
  .sub {{ font-size:26px; font-weight:700; color:{l}; margin-top:14px; line-height:1.45; }}
  .stats {{ display:flex; gap:16px; margin-top:auto; }}
  .stat {{ background:rgba(255,255,255,.13); border:1px solid rgba(255,255,255,.24);
    border-radius:18px; padding:16px 24px; min-width:184px; }}
  .stat .n {{ font-size:46px; font-weight:900; line-height:1; letter-spacing:-.02em; }}
  .stat .n i {{ font-size:24px; font-style:normal; margin-left:2px; }}
  .stat .l {{ font-size:17px; font-weight:700; color:{l}; margin-top:9px; }}
  .quote {{ border-left:4px solid {y}; padding-left:16px; font-size:21px; line-height:1.55;
    color:rgba(255,255,255,.94); margin-top:24px; font-weight:500; }}
  .foot {{ display:flex; justify-content:space-between; align-items:flex-end; margin-top:22px; }}
  .brand {{ font-size:24px; font-weight:900; letter-spacing:.01em; }}
  .url {{ font-size:20px; font-weight:700; color:{y}; }}
</style></head>
<body>
  <div class="glow g1"></div><div class="glow g2"></div>
  <div class="wrap">
    <div class="pill">PA45 <b>{eyebrow}</b></div>
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


def build_specs(d):
    s = d["summary"]
    det = {r["label"]: r for r in d["can_do_detail"]}
    meaning = det["今日のアクションの意味が分かった"]
    use = det["今日のアクションを自分で使えるようになった"]
    t = d["time_preference_pcts"]
    first_slot = d["time_preference"][0][0]

    return {
        "numbers": {
            "out": "insights-numbers.png",
            "theme": "green",
            "eyebrow": f"第1回〜第{s['sessions']}回のデータ 📊",
            "title": "数字で見るPA45",
            "tsize": 76,
            "sub": f"毎週木曜45分のハンズオンを{s['sessions']}回。全部そのまま出します。",
            "stats": [
                (s["sessions"], "回", "開催回数"),
                (s["participants_total"], "名", "のべ参加登録"),
                (s["understanding_avg"], "%", "内容が理解できた"),
                (s["usefulness_avg"], "%", "業務に役立ちそう"),
            ],
            "quote": f"アンケート回答 {s['responses_total']}件 ／ 1回あたり平均 {s['participants_avg']}名",
        },
        "can-do": {
            "out": "insights-can-do.png",
            "theme": "blue",
            "eyebrow": "できるようになったこと ✅",
            "title": "45分で届くのは、どこまでか",
            "tsize": 68,
            "sub": "アンケートの複数選択を19回・233件分あつめました。",
            "stats": [
                (meaning["rate"], "%", "意味が分かった"),
                (use["rate"], "%", "自分で使えるようになった"),
                (s["responses_total"], "件", "アンケート回答"),
            ],
            "quote": "「分かった」と「使える」のあいだには、はっきり差がある。",
        },
        "voices": {
            "out": "insights-voices.png",
            "theme": "amber",
            "eyebrow": "参加者の声 💬",
            "title": "「苦手」が消えた瞬間",
            "tsize": 72,
            "sub": "JSON、式、実行履歴。つまずいた人が、そのあと何と言ったか。",
            "stats": [
                (s["responses_total"], "件", "アンケート回答"),
                (s["sessions"], "回", "第1回〜第19回"),
                (s["participants_total"], "名", "のべ参加登録"),
            ],
            "quote": "「JSONはよく分からないなぁっと勝手に苦手意識を持っていましたが…」（第14回）",
        },
        "design": {
            "out": "insights-design.png",
            "theme": "purple",
            "eyebrow": "時間の設計 ⏱",
            "title": "なぜ45分・木曜20:15なのか",
            "tsize": 62,
            "sub": "希望開催時間のアンケートに、思ったよりはっきり答えが出ていました。",
            "stats": [
                (t[first_slot], "%", "20:15〜21:00 を希望"),
                (45, "分", "1回あたりの長さ"),
                (s["participants_avg"], "名", "1回あたり平均参加"),
            ],
            "quote": "「45分という時間が長すぎず短すぎず良い感じでした」（第1回）",
        },

        # ───── サイト各ページのカード ─────
        "top": {
            "out": "og-top.png",
            "theme": "green",
            "eyebrow": "毎週木曜 20:15 ｜ オンライン・無料 ⚡",
            "title": "Power Automateを、45分ずつ",
            "tsize": 64,
            "sub": "さわったことがない人が、最初の一歩を踏み出すための勉強会です。",
            "stats": [
                (s["sessions"], "回", "開催してきました"),
                (s["participants_total"], "名", "のべ参加登録"),
                (s["usefulness_avg"], "%", "業務に役立ちそう"),
            ],
            "quote": "初参加歓迎 ／ 見るだけ参加OK ／ 過去回の録画とスライドも公開",
        },
        "survey": {
            "out": "og-survey.png",
            "theme": "rose",
            "eyebrow": "受講者アンケート 📋",
            "title": "結果は、毎回そのまま出しています",
            "tsize": 58,
            "sub": "理解度・役立ち度のスコアと、コメント原文。回ごとに読めます。",
            "stats": [
                (s["responses_total"], "件", "アンケート回答"),
                (s["understanding_avg"], "%", "内容が理解できた"),
                (s["usefulness_avg"], "%", "業務に役立ちそう"),
            ],
            "quote": "「少し難しかった」も「まだイメージがついていない」も消していません。",
        },
        "learn": {
            "out": "og-learn.png",
            "theme": "cyan",
            "eyebrow": "学習ハブ 📚",
            "title": "関数と考え方を、1枚ずつ",
            "tsize": 66,
            "sub": "Power Automateの関数や概念を、カテゴリ別に整理して置いています。",
            "stats": [
                (s["sessions"], "回", "分の講座から"),
                (45, "分", "1回の長さ"),
                (0, "円", "登録なしで閲覧"),
            ],
            "quote": "「式」も「JSON」も、苦手なところから順番に崩していきます。",
        },
        "videos": {
            "out": "og-videos.png",
            "theme": "red",
            "eyebrow": "動画アーカイブ ▶",
            "title": "過去回の録画を、選んですぐ見る",
            "tsize": 62,
            "sub": "テーマで絞って、気になる回だけその場で再生できます。",
            "stats": [
                (s["archive_videos"], "本", "公開中の録画"),
                (45, "分", "1本あたり"),
                (s["sessions"], "回", "これまでの開催"),
            ],
            "quote": "「作業が追い付かないことが多くなったので、動画見て復習しております」（第10回）",
        },
        "sessions": {
            "out": "og-sessions.png",
            "theme": "teal",
            "eyebrow": "毎週木曜 20:15 ｜ 参加無料 📅",
            "title": "45分だけ、一緒に手を動かす",
            "tsize": 66,
            "sub": "Power Automateをさわったことがない人向けのオンラインハンズオンです。",
            "stats": [
                (s["sessions"], "回", "開催してきました"),
                (s["participants_total"], "名", "のべ参加登録"),
                (s["understanding_avg"], "%", "内容が理解できた"),
            ],
            "quote": "初参加歓迎 ／ 見るだけ参加OK ／ connpassから申し込み",
        },
        "slides": {
            "out": "og-slides.png",
            "theme": "sky",
            "eyebrow": "解説スライド 📄",
            "title": "全19回のスライドを置いています",
            "tsize": 60,
            "sub": "その場で追いつけなくても、あとから同じ手順をたどれるように。",
            "stats": [
                (s["sessions"], "回", "分のスライド"),
                (s["archive_videos"], "本", "録画とセットで"),
                (0, "円", "登録なしで閲覧"),
            ],
            "quote": "「資料も公表してもらえて復習に大変ありがたいです」（第9回）",
        },
        "achievements": {
            "out": "og-achievements.png",
            "theme": "green",
            "eyebrow": "活動の記録 📋",
            "title": "PA45がやってきたこと、全部",
            "tsize": 64,
            "sub": "開催実績・アンケート・登壇・記事。数字も声も、そのまま出しています。",
            "stats": [
                (s["sessions"], "回", "ハンズオン開催"),
                (s["participants_total"], "名", "のべ参加登録"),
                (s["responses_total"], "件", "アンケート回答"),
            ],
            "quote": "毎週木曜20:15から45分・オンライン・無料でやっています。",
        },
        "talks": {
            "out": "og-talks.png",
            "theme": "slate",
            "eyebrow": "登壇・LT資料 🎤",
            "title": "外でも話しています",
            "tsize": 68,
            "sub": "Copilotコミュニティや広島のPower Platform勉強会で発表した資料です。",
            "stats": [
                (2, "本", "公開中のLT資料"),
                (s["sessions"], "回", "PA45の開催"),
                (s["participants_total"], "名", "のべ参加登録"),
            ],
            "quote": "スライドはそのまま配布しています。使ってもらってかまいません。",
        },
        "method": {
            "out": "og-method.png",
            "theme": "purple",
            "eyebrow": "講座設計の話 ⚙",
            "title": "なぜ45分で、なぜ1回1粒なのか",
            "tsize": 56,
            "sub": "非ITの初心者が最初の一歩を踏み出せることに全振りした設計の話。",
            "stats": [
                (45, "分", "1回の長さ"),
                (1, "粒", "1回で扱うテーマ"),
                (s["understanding_avg"], "%", "内容が理解できた"),
            ],
            "quote": "詰め込まないほうが、結局そのあと手が動く。",
        },
        "start-here": {
            "out": "og-start-here.png",
            "theme": "blue",
            "eyebrow": "はじめての方へ 🚩",
            "title": "何も分からない状態で来て大丈夫です",
            "tsize": 52,
            "sub": "必要なもの、当日の流れ、つまずいたときの逃げ道をまとめました。",
            "stats": [
                (s["participants_total"], "名", "のべ参加登録"),
                (s["usefulness_avg"], "%", "業務に役立ちそう"),
                (0, "円", "参加費"),
            ],
            "quote": "「とっかかりがなくて。これをきっかけに触ってみたいなと」（第8回）",
        },
    }


def render(spec, chrome):
    th = THEMES[spec["theme"]]
    html = TEMPLATE.format(
        d=th["d"], m=th["m"], a=th["a"], l=th["l"], y=th["y"],
        eyebrow=spec["eyebrow"], title=spec["title"], tsize=spec["tsize"], sub=spec["sub"],
        stats="".join(stat_html(*x) for x in spec["stats"]),
        quote=f'<div class="quote">{spec["quote"]}</div>' if spec.get("quote") else "",
    )
    out = OUT_DIR / spec["out"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "ogp.html"
        src.write_text(html, encoding="utf-8")
        subprocess.run([
            str(chrome), "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--window-size=1200,630",
            "--virtual-time-budget=6000", f"--screenshot={out}", src.as_uri(),
        ], check=True, capture_output=True)
    print(f"[OK] {out}")


def main():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    specs = build_specs(d)
    wanted = sys.argv[1:] or list(specs)
    chrome = find_chrome()
    for key in wanted:
        if key not in specs:
            print(f"[SKIP] 不明なキー: {key}（{', '.join(specs)}）")
            continue
        render(specs[key], chrome)


if __name__ == "__main__":
    main()

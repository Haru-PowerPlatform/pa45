"""受注ページ（work/index.html）の、データから決まる部分を最新に書き替える。

- 登壇・運営の実績（TALKS 配列）… data/activities/*.json の type=="Event" かつ public
  表記は各ファイルの "work" {event, role, note} を使う。無ければ title / impact から作る
- PA45 の数字・回ごとのグラフ … data/insights.json
- ブログの公開記事数 … automate136 の WP REST（取れなければ前の値のまま）

冪等。中身が変わったときだけ書き込み、フッターの更新日も今日にする。
夜間ジョブ（scripts/nightly-site-refresh.ps1）から呼ぶ。
"""
import glob
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "work" / "index.html"
TODAY = date.today()
JP_DATE = f"{TODAY.year}年{TODAY.month}月{TODAY.day}日"


def jp(d):
    y, m, dd = d.split("-")
    return f"{int(y)}年{int(m)}月{int(dd)}日"


def talk_row(a):
    w = a.get("work") or {}
    title = a.get("title", "")
    head, _, tail = title.partition("：")
    event = w.get("event") or re.sub(r"(で|を)(LT登壇|登壇|運営|主催|ゲスト出演)$", "", head).strip("「」 ")
    role = w.get("role")
    if not role:
        role = next((k for k in ("LT登壇", "ゲスト出演", "主催", "運営", "登壇") if k in head), "登壇")
    note = w.get("note")
    if note is None:
        note = tail or (a.get("impact") or {}).get("scale", "")
    ev = a.get("evidence") or {}
    url = ev.get("event") or ev.get("connpass") or ev.get("slide") or ev.get("blog") or ""
    ym = a["date"][:7].replace("-", ".")
    return [ym, event, role, note, url]


def build_talks():
    rows = []
    for f in sorted(glob.glob(str(ROOT / "data" / "activities" / "2*.json"))):
        a = json.load(open(f, encoding="utf-8"))
        if a.get("type") == "Event" and a.get("public", True) and a.get("date", "") <= TODAY.isoformat():
            rows.append((a["date"], talk_row(a)))
    rows.sort(key=lambda r: r[0], reverse=True)
    js = ",\n".join(" " + json.dumps(r, ensure_ascii=False) for _, r in rows)
    return "const TALKS=[\n" + js + ",\n];", len(rows)


def blog_total():
    try:
        req = urllib.request.Request(
            "https://www.automate136.com/wp-json/wp/v2/posts?per_page=1&status=publish&_fields=id",
            headers={"User-Agent": "pa45-build-work-page"},
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            return int(r.headers.get("X-WP-Total"))
    except Exception as e:  # ネットに出られない夜は前の値のまま
        print("blog total: skip", e)
        return None


def sub1(pat, rep, s, label):
    s2, n = re.subn(pat, rep, s, count=1, flags=re.S)
    if n == 0:
        print(f"WARN: {label} が見つからない", file=sys.stderr)
    return s2


def main():
    src = PAGE.read_text(encoding="utf-8")
    s = src

    talks, n_talks = build_talks()
    s = sub1(r"const TALKS=\[.*?\n\];", lambda m: talks, s, "TALKS")

    ins = json.load(open(ROOT / "data" / "insights.json", encoding="utf-8"))
    sm = ins["summary"]
    N, P, U, F, R = sm["sessions"], sm["participants_total"], sm["understanding_avg"], sm["usefulness_avg"], sm["responses_total"]
    last = jp(sm["last_date"])
    Pc = f"{P:,}"

    s = sub1(r'<b>\d+(<small style="font-size:\.5em">回</small>)', rf"<b>{N}\1", s, "回数")
    s = sub1(r'<b>[\d,]+(<small style="font-size:\.5em">名</small>)', rf"<b>{Pc}\1", s, "参加者")
    s = sub1(r'<b>[\d.]+(<small style="font-size:\.5em">%</small></b><span>「理解)', rf"<b>{U}\1", s, "理解度")
    s = sub1(r'<b>[\d.]+(<small style="font-size:\.5em">%</small></b><span>「役立)', rf"<b>{F}\1", s, "役立ち度")
    s = sub1(r"\d{4}年\d+月\d+日時点。第1回〜第\d+回の実測値。(.*?)（回答\d+件）の平均。",
             rf"{last}時点。第1回〜第{N}回の実測値。\1（回答{R}件）の平均。", s, "出典")
    s = re.sub(r"毎週・全\d+回", f"毎週・全{N}回", s)
    s = re.sub(r"全\d+回のアンケート結果", f"全{N}回のアンケート結果", s)
    s = re.sub(r"PA45 全\d+回の講座アーカイブ", f"PA45 全{N}回の講座アーカイブ", s)
    s = re.sub(r"第1回〜第\d+回で回答は\d+件です", f"第1回〜第{N}回で回答は{R}件です", s)
    s = re.sub(r"回答\d+件の内訳", f"回答{R}件の内訳", s)
    s = re.sub(r"第1回から第\d+回までの", f"第1回から第{N}回までの", s)
    s = re.sub(r"上の実績の [\d.]+%・[\d.]+% は、この\d+回分の平均です",
               f"上の実績の {U}%・{F}% は、この{N}回分の平均です", s)
    s = re.sub(r"PA45 を\d+回主催・のべ[\d,]+名", f"PA45 を{N}回主催・のべ{Pc}名", s)

    order_u = ["とても理解できた", "理解できた", "普通", "少し難しかった", "難しかった"]
    order_f = ["役立ちそう", "少し役立ちそう", "まだイメージがついていない"]
    du, df = dict(ins["understanding"]), dict(ins["usefulness"])
    D = {
        "rows": [[x["vol"], x["responses"], x["understanding_pct"], x["usefulness_pct"]]
                 for x in sorted(ins["sessions"], key=lambda x: x["vol"]) if x.get("responses")],
        "u": [[k, du.get(k, 0)] for k in order_u],
        "f": [[k, df.get(k, 0)] for k in order_f],
    }
    s = sub1(r"const D=\{.*?\};", lambda m: "const D=" + json.dumps(D, ensure_ascii=False) + ";", s, "グラフ")

    bt = blog_total()
    if bt:
        s = sub1(r"（公開記事 \d+ 本・\d{4}年\d+月\d+日時点）", f"（公開記事 {bt} 本・{JP_DATE}時点）", s, "ブログ本数") \
            if not re.search(rf"（公開記事 {bt} 本・", s) else s

    if s != src:
        s = re.sub(r"更新日：\d{4}年\d+月\d+日", f"更新日：{JP_DATE}", s)
        PAGE.write_text(s, encoding="utf-8", newline="")
        print(f"updated: talks={n_talks} sessions={N} participants={Pc} blog={bt}")
    else:
        print(f"no change: talks={n_talks} sessions={N}")


if __name__ == "__main__":
    main()

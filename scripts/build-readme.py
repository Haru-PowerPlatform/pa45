"""README.md（リポジトリの表紙）と flows/README.md・slides/README.md を data/ から冪等に生成する。

GitHub でリポジトリを開いた人が、何が公開されていて誰の役に立つのかを
最初の画面で把握できるようにするためのもの。数字はすべて data/ から取り直す。

入力：
  data/insights.json                … 開催回数・参加者・アンケート（build-insights.py の出力）
  data/config/links-index.json      … 各回のタイトル（参加者が得られることを書いた版）
  data/config/upcoming-event.json   … 次回
  data/activities/*.json            … 講座以外のコミュニティ活動
  git ls-files                      … 実際に公開されているフローZIP・スライド
  slides/index.html                 … 技術Tipsスライドの枚数

⚠ 公開リポジトリ。社名・申請関係の語・個人情報を出さない。
⚠ 生成物なので README.md を直接編集しない。文言はこのスクリプトを直す。
"""
from __future__ import annotations

import datetime as dt
import glob
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://haru-powerplatform.github.io/pa45"
CONNPASS_GROUP = "https://powerautomate-create.connpass.com/"
BLOG = "https://www.automate136.com/"
X_URL = "https://x.com/isamu_Automate"

# 講座以外の活動として README に載せる type と、載せない id
EXTERNAL_TYPES = {"Event", "Support", "Feedback"}
SKIP_IDS = {"2025-11-15-ppec-itsukushima"}  # 公開URLの証跡が無い
# 活動レコードにあるが、開くと404になるリンク（2026-09-15に確認）。記事が公開されたら外す
DEAD_LINKS = {"https://www.automate136.com/ippo-fumidasete-tv-ep25/"}


def load(path: str):
    with open(ROOT / path, encoding="utf-8") as f:
        return json.load(f)


def tracked(prefix: str) -> list[str]:
    out = subprocess.run(
        ["git", "-c", "core.quotepath=false", "ls-files", prefix],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    return [l for l in out.splitlines() if l]


def md_escape(s: str) -> str:
    return s.replace("|", "｜").replace("\n", " ").strip()


def fmt_date(iso: str) -> str:
    return iso.replace("-", "/")


def write_if_changed(path: Path, text: str) -> None:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text:
        print(f"  変更なし: {path.relative_to(ROOT)}")
        return
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"  更新: {path.relative_to(ROOT)}")


# ───────── データ収集 ─────────
ins = load("data/insights.json")
summ = ins["summary"]
sessions = sorted(ins["sessions"], key=lambda r: r["vol"])

titles = {r["vol"]: r for r in load("data/config/links-index.json")}

flow_zips: dict[int, list[str]] = {}
for p in tracked("flows"):
    m = re.match(r"flows/vol-(\d+)/[^/]+\.zip$", p)
    if m:
        flow_zips.setdefault(int(m.group(1)), []).append(p)

slide_vols = {int(m.group(1)) for p in tracked("slides")
              if (m := re.match(r"slides/vol-(\d+)/index\.html$", p))}
hub_vols = {int(m.group(1)) for p in tracked("slides")
            if (m := re.match(r"slides/vol-(\d+)/links\.html$", p))}
survey_vols = {int(m.group(1)) for p in tracked("achievements/insights")
               if (m := re.match(r"achievements/insights/vol-(\d+)\.html$", p))}

gallery = (ROOT / "slides/index.html").read_text(encoding="utf-8")
x_slides = gallery.count('class="x-card"')

videos = sum(1 for r in sessions if r.get("youtube"))

first5 = [r["participants"] or 0 for r in sessions[:5]]
last5 = [r["participants"] or 0 for r in sessions[-5:]]
avg = lambda xs: round(sum(xs) / max(len(xs), 1), 1)

upcoming = None
try:
    u = load("data/config/upcoming-event.json")
    if u.get("date_iso") and u["date_iso"] > summ["last_date"]:
        upcoming = u
except FileNotFoundError:
    pass

external = []
for f in sorted(glob.glob(str(ROOT / "data/activities/*.json"))):
    name = os.path.basename(f)
    if name.startswith("_") or name == "index.json":
        continue
    j = json.load(open(f, encoding="utf-8"))
    if j.get("type") not in EXTERNAL_TYPES or not j.get("public") or j.get("id") in SKIP_IDS:
        continue
    if not j.get("evidence"):
        continue
    external.append(j)
external.sort(key=lambda j: j["date"])


def session_title(r) -> str:
    t = titles.get(r["vol"], {}).get("title") or r["theme"]
    return md_escape(t)


def link(label: str, url: str | None) -> str:
    return f"[{label}]({url})" if url else "―"


def para(sink, text: str) -> None:
    """句点ごとに改行する。行末のバックスラッシュでハード改行にする（日本語の文の間に空白が入らないように）。"""
    parts = re.findall(r"[^。]+。?", text)
    for i, x in enumerate(parts):
        sink(x + ("\\" if i < len(parts) - 1 else ""))


def slide_cell(v: int) -> str:
    # 第1〜11回はHTMLスライド化の前でPPTX配布。回ごとの資料ページ（links.html）へ飛ばす
    if v in slide_vols:
        return link("開く", f"{SITE}/slides/vol-{v:02d}/")
    if v in hub_vols:
        return link("資料", f"{SITE}/slides/vol-{v:02d}/links.html")
    return "―"


# ───────── README.md ─────────
L: list[str] = []
w = L.append

w("# PA45 ― Power Automate 45分ハンズオン")
w("")
para(w, "Power Automate を初めて触る人が、45分で1本のフローを作り終えるオンライン講座です。週1回、無料で開催しています。")
w("")
para(w, "講座で使ったスライド、完成したフローのZIP、録画、アンケートの集計は、このリポジトリと公開サイトですべて無料で公開しています。参加していない人でも、同じ手順をあとから再現できる形で残しています。")
w("")
w(f"- 公開サイト：{SITE}/")
w(f"- 参加申込（connpass）：{CONNPASS_GROUP}")
w(f"- 運営：Haru（X [@isamu_Automate]({X_URL})／ブログ [automate136.com]({BLOG})）")
w("")
w("> **About (English)** ― PA45 is a free, weekly, 45-minute hands-on online workshop that helps "
  "business users with no IT background build their first Power Automate cloud flow. "
  "Slides, importable flow solutions (ZIP), recordings and aggregated survey results for every session "
  "are published openly in this repository.")
w("")

w("## 目次")
w("")
w("- [数字で見る PA45](#数字で見る-pa45)")
w("- [公開している教材](#公開している教材)")
w("- [全回の一覧](#全回の一覧)")
w("- [講座以外のコミュニティ活動](#講座以外のコミュニティ活動)")
w("- [フローZIPの使い方](#フローzipの使い方)")
w("- [リポジトリの構成](#リポジトリの構成)")
w("")

w("## 数字で見る PA45")
w("")
w(f"第{sessions[0]['vol']}回（{fmt_date(summ['first_date'])}）〜第{sessions[-1]['vol']}回（{fmt_date(summ['last_date'])}）の集計です。")
w("")
w("| 項目 | 値 |")
w("|---|---|")
w(f"| 開催回数 | {summ['sessions']}回 |")
w(f"| 延べ参加者 | {summ['participants_total']:,}名 |")
w(f"| 1回あたりの参加者 | 平均 {summ['participants_avg']}名／最多 {summ['participants_max']}名 |")
w(f"| 参加者の推移 | 第1〜5回の平均 {avg(first5)}名 → 直近5回の平均 {avg(last5)}名 |")
w(f"| アンケート回答 | {summ['responses_total']:,}件 |")
w(f"| 理解度スコア（全回平均） | {summ['understanding_avg']}% |")
w(f"| 役立ち度スコア（全回平均） | {summ['usefulness_avg']}% |")
w(f"| 録画を公開した回 | {videos}回 |")
w(f"| 公開しているフローZIP | {sum(len(v) for v in flow_zips.values())}本 |")
w(f"| 技術Tipsスライド | {x_slides}本 |")
w("")
w("- 参加者数は connpass の参加者数、スコアは各回のアンケートから集計しています（`data/insights.json`）。")
w("- 理解度スコア＝5択（とても理解できた100／理解できた75／普通50／少し難しかった25／難しかった0）の回答数による加重平均。")
w("- 役立ち度スコア＝3択（役立ちそう100／少し役立ちそう50／まだイメージがついていない0）の加重平均。")
w(f"- 回ごとの内訳と自由記述は [アンケート結果]({SITE}/achievements/insights/) にあります。")
w("")

w("## 公開している教材")
w("")
w("| 教材 | 中身 | 場所 |")
w("|---|---|---|")
w(f"| 講座スライド | 各回のHTMLスライド。ブラウザで開けば、そのまま手順を追える | [全回の目次]({SITE}/slides/links.html)／[`slides/`](slides/) |")
w(f"| フローのZIP | 講座で作ったフローの完成品。自分の環境にインポートして動きを確認できる | [ダウンロードページ]({SITE}/flows/)／[`flows/`](flows/) |")
w(f"| 録画 | 講座当日の録画（YouTube） | [動画アーカイブ]({SITE}/videos/) |")
w(f"| アンケート結果 | 回ごとの理解度・役立ち度・自由記述 | [アンケート結果]({SITE}/achievements/insights/) |")
w(f"| 技術Tipsスライド | Power Automate／Copilot Studio の小技を1テーマ1枚にまとめたスライド | [スライド一覧]({SITE}/slides/) |")
w(f"| 初参加ガイド | 参加前に用意するもの、当日の流れ | [初めての方へ]({SITE}/start-here/) |")
w(f"| 講座の設計 | 45分に収める理由、1回1テーマに絞る理由 | [PA45 Method]({SITE}/method/) |")
w(f"| 登壇資料 | 外部のコミュニティイベントで話したときのスライド | [登壇・LT資料]({SITE}/talks/) |")
w("")

w("## 全回の一覧")
w("")
if upcoming:
    w(f"次回は **第{upcoming['vol']}回 {md_escape(upcoming['theme'])}**"
      f"（{upcoming.get('date_label', fmt_date(upcoming['date_iso']))} {upcoming.get('time_range', '')}）です。"
      f"申込は [connpass]({upcoming['connpass_url']}) から。")
    w("")
w("| 回 | 開催日 | テーマ | 参加 | スライド・資料 | フロー | 録画 | アンケート | レポート |")
w("|---:|---|---|---:|:---:|:---:|:---:|:---:|:---:|")
for r in reversed(sessions):
    v = r["vol"]
    slide = slide_cell(v)
    zips = flow_zips.get(v, [])
    flow = " ".join(link("ZIP", f"{SITE}/{z}") for z in zips) if zips else "―"
    video = link("見る", r.get("youtube"))
    survey = link("結果", f"{SITE}/achievements/insights/vol-{v:02d}.html") if v in survey_vols else "―"
    report = link("記事", r.get("blog"))
    w(f"| {v} | {fmt_date(r['date'])} | {session_title(r)} | {r['participants'] or '―'}名 "
      f"| {slide} | {flow} | {video} | {survey} | {report} |")
w("")
w("「―」は、その回の公開物をまだこのリポジトリに置いていないことを表します。")
w("")

w("## 講座以外のコミュニティ活動")
w("")
w("PA45 の外で、Power Platform／Copilot のコミュニティに関わった記録です。")
w("")
w("| 日付 | 内容 | 役割 | 規模 | リンク |")
w("|---|---|---|---|---|")
EV_LABEL = {"connpass": "connpass", "event": "connpass", "blog": "レポート", "slide": "スライド",
            "talks": "登壇資料", "idea": "公開ページ", "thread": "スレッド"}
for j in external:
    ev = j.get("evidence") or {}
    links = " ／ ".join(f"[{EV_LABEL.get(k, k)}]({u})" for k, u in ev.items() if u and u not in DEAD_LINKS)
    impact = j.get("impact") or {}
    scale = md_escape(impact.get("scale", "")) or "―"
    role = j.get("role") or {"Support": "回答者", "Feedback": "報告者"}.get(j["type"])
    if not role:
        role = "ゲスト出演" if "ゲスト出演" in j["title"] else "登壇"
    role = md_escape(role)
    w(f"| {fmt_date(j['date'])} | {md_escape(j['title'])} | {role} | {scale} | {links} |")
w("")
w(f"すべての記録は [`data/activities/`](data/activities/) に1件1ファイルで置いています。"
  f"サイト上では [活動の記録]({SITE}/achievements/) で見られます。")
w("")

w("## フローZIPの使い方")
w("")
para(w, "ZIPは Power Automate の「ソリューション」形式です。展開せずにそのままインポートします。")
w("")
w("1. [フローのダウンロードページ](" + SITE + "/flows/) から、使いたい回のZIPを保存する")
w("2. make.powerautomate.com の左メニュー「ソリューション」→「インポート」→「ソリューションのインポート」でZIPを選ぶ")
w("   - ソリューション形式にしているのは、フロー本体と接続の設定をまとめて持ち運べるため")
w("3. インポートしたフローを開き、接続が必要と表示されたアクションに自分のアカウントで接続する")
w("   - 接続は作った人のアカウントに紐づくため、インポートした側で付け直す必要がある")
w("4. 保存してフローをオンにし、講座スライドの手順に沿って動かす")
w("")
para(w, "組織の環境によっては、ソリューションのインポート権限が無いことがあります。その場合は環境の管理者への確認が要ります。")
w("")

w("## リポジトリの構成")
w("")
para(w, "このリポジトリは GitHub Pages で公開サイトとしてそのまま配信しています。URLを変えないため、フォルダはサイトの階層と一致させています。")
w("")
w("**講座の教材（誰でも使えるもの）**")
w("")
w("| フォルダ | 中身 |")
w("|---|---|")
w("| [`slides/`](slides/) | 各回の講座スライド（`vol-NN/`）と技術Tipsスライドの一覧 |")
w("| [`flows/`](flows/) | 各回のフローのZIP（`vol-NN/`） |")
w("| [`sessions/`](sessions/) | 次回の案内と過去回のアーカイブ |")
w("| [`videos/`](videos/) | 録画の一覧 |")
w("| [`achievements/`](achievements/) | アンケート結果と活動の記録 |")
w("| [`talks/`](talks/) | 外部イベントでの登壇資料 |")
w("| [`start-here/`](start-here/)・[`method/`](method/)・[`about/`](about/) | 初参加ガイド、講座の設計、運営者の紹介 |")
w("| [`assets/x/html/`](assets/x/html/) | 技術Tipsスライドの元HTML |")
w("")
w("**サイトを動かす仕組み**")
w("")
w("| フォルダ | 中身 |")
w("|---|---|")
w("| [`data/`](data/) | アンケート（`surveys/`）、活動記録（`activities/`）、集計結果（`insights.json`）など、サイトの数字の元データ |")
w("| [`scripts/`](scripts/) | 集計・一覧ページ・この README を生成するスクリプト |")
w("| [`.github/workflows/`](.github/workflows/) | 開催後の集計や一覧の更新を自動で回す GitHub Actions |")
w("")
w("上記以外のフォルダ（`admin/` `tools/` `sites/` `articles/` `outputs/` など）は運営者の作業用・個人用で、講座の教材には含まれません。")
w("")
w("---")
w("")
para(w, "この README は `scripts/build-readme.py` が `data/` から生成しています。数字は開催のたびに更新されます。"
        "Microsoft、Power Automate、Copilot Studio、Microsoft Teams、SharePoint は Microsoft Corporation の商標です。"
        "PA45 は個人が運営するコミュニティ講座で、Microsoft とは関係ありません。")
w("")

write_if_changed(ROOT / "README.md", "\n".join(L))


# ───────── flows/README.md ─────────
F: list[str] = []
f = F.append
f("# flows ― 講座で作ったフローのZIP")
f("")
para(f, "PA45 の各回で作ったフローの完成品です。Power Automate の「ソリューション」形式なので、展開せずにそのままインポートできます。"
      f"手順つきのダウンロードページは {SITE}/flows/ にあります。")
f("")
f("| 回 | テーマ | ZIP | 講座スライド |")
f("|---:|---|---|:---:|")
by_vol = {r["vol"]: r for r in sessions}
for v in sorted(flow_zips, reverse=True):
    r = by_vol.get(v)
    title = session_title(r) if r else md_escape(titles.get(v, {}).get("title", ""))
    zips = "<br>".join(f"[{Path(z).name}]({Path(z).relative_to('flows').as_posix()})" for z in flow_zips[v])
    slide = slide_cell(v)
    f(f"| {v} | {title} | {zips} | {slide} |")
f("")
f("- 一覧に無い回は、完成品のZIPをこのフォルダに置いていない回です。手順は各回の講座スライドにあります。")
f("- インポート後は、接続が必要と表示されたアクションに自分のアカウントで接続し直す必要があります。接続は作った人のアカウントに紐づくためです。")
f("- `PA45Handson_1_0_0_*.zip` は、複数回のフローを1つのソリューションにまとめた旧版のパックです。")
f("")
f("この README は `scripts/build-readme.py` が生成しています。")
f("")
write_if_changed(ROOT / "flows/README.md", "\n".join(F))


# ───────── slides/README.md ─────────
S: list[str] = []
s = S.append
s("# slides ― 講座スライド")
s("")
para(s, "PA45 の各回で使ったスライドです。1回ぶんが1つのHTMLで完結しているので、ブラウザで開けばそのまま手順を追えます。"
      f"回ごとの配布物（スライド・ZIP・アンケート）をまとめた目次は {SITE}/slides/links.html にあります。")
s("")
s("| 回 | 開催日 | テーマ | スライド |")
s("|---:|---|---|:---:|")
for v in sorted(slide_vols, reverse=True):
    r = by_vol.get(v)
    if r:
        date, title = fmt_date(r["date"]), session_title(r)
    elif upcoming and upcoming["vol"] == v:
        date, title = fmt_date(upcoming["date_iso"]) + "（予定）", md_escape(upcoming["theme"])
    else:
        t = titles.get(v, {})
        date, title = fmt_date(t.get("date", "")), md_escape(t.get("title", ""))
    s(f"| {v} | {date} | {title} | [開く]({SITE}/slides/vol-{v:02d}/) |")
s("")
s(f"- `index.html` は技術Tipsスライド（{x_slides}本）の一覧です。元HTMLは `assets/x/html/` にあります。")
s("- `links.html` は全回の目次です。どちらも `scripts/` のスクリプトで生成しています。")
s("")
s("この README は `scripts/build-readme.py` が生成しています。")
s("")
write_if_changed(ROOT / "slides/README.md", "\n".join(S))

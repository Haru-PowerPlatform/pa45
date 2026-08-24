r"""
X投稿ボード生成スクリプト

Documents\pa45-x-drafts.html を組み立てます。タブは2枚:
  - PA45（切り口ローテ）… data/drafts/x-pa45-rotation.md から
  - X技術Tips          … data/x-tips-board.json から（スライドPNG2枚つき）

どちらも「本文をコピー」と「Xの下書きを開く（本文入りでcomposerが開く）」ボタンつき。
技術Tipsは画像2枚のパスをまとめてコピーできるので、Xのファイル選択に貼れば2枚同時に選べます。

使い方:
  python scripts/build-x-board.py
"""

import html
import io
import json
import re
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ビルド時刻（JST）。「開いている板が最新か」を一目で分かるようにする。
BUILT_AT = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M")

ROOT = Path(__file__).resolve().parent.parent          # ...\Documents\pa45
OUT = ROOT.parent / "pa45-x-drafts.html"               # ...\Documents\pa45-x-drafts.html
OGP_BASE = "https://haru-powerplatform.github.io/pa45/assets/ogp/"


def x_len(body: str) -> int:
    """Xの重み付き文字数（上限280）。URLは一律23、半角は1、日本語などは2で数える。"""
    s = re.sub(r"https?://\S+", "x" * 23, body)
    n = 0
    for ch in s:
        c = ord(ch)
        light = (c <= 0x10FF or 0x2000 <= c <= 0x200A or 0x2028 <= c <= 0x202F
                 or 0x2060 <= c <= 0x206F)
        n += 1 if light else 2
    return n


def intent(body: str) -> str:
    return "https://x.com/intent/post?text=" + urllib.parse.quote(body)


# LinkedInは本文の事前入力ができないので、composerを開くだけ（コピー→貼付運用）
LI_COMPOSE = "https://www.linkedin.com/feed/?shareActive=true"


def c140(body: str) -> int:
    """告知ツイート用の文字数（URLは23、それ以外は1文字＝1で数える。上限140）。"""
    s = re.sub(r"https?://\S+", "x" * 23, body)
    return len(s)


# ── タブ1：PA45 切り口ローテ ────────────────────────────────
def _insight_tokens():
    """data/insights.json の集計値を {{...}} トークンとして返す。
    rotation.md の累計数字はハードコードせずこのトークンで書き、ビルド時に流し込む
    ＝毎週 build-insights.py が走れば、ボードの数字は自動で最新になる。"""
    f = ROOT / "data" / "insights.json"
    if not f.exists():
        return {}
    s = json.loads(f.read_text(encoding="utf-8")).get("summary", {})
    tp = json.loads(f.read_text(encoding="utf-8")).get("time_preference_pcts", {})
    slot = tp.get("20:15～21:00") or tp.get("20:15〜21:00") or 0
    def d1(x):  # 小数1桁（例 91.0）
        return f"{float(x):.1f}"
    return {
        "{{N}}":    str(s.get("sessions", "")),
        "{{PT}}":   str(s.get("participants_total", "")),
        "{{RT}}":   str(s.get("responses_total", "")),
        "{{UND}}":  d1(s.get("understanding_avg", 0)),
        "{{USE}}":  d1(s.get("usefulness_avg", 0)),
        "{{AVG}}":  d1(s.get("participants_avg", 0)),
        "{{AVGI}}": str(round(float(s.get("participants_avg", 0)))),
        "{{MAX}}":  str(s.get("participants_max", "")),
        "{{TIME}}": str(round(float(slot))),
        "{{VID}}":  str(s.get("archive_videos", "")),
    }


def _apply_tokens(text, tokens):
    for k, v in tokens.items():
        text = text.replace(k, v)
    return text


def load_pa45():
    src = (ROOT / "data" / "drafts" / "x-pa45-rotation.md").read_text(encoding="utf-8")
    src = _apply_tokens(src, _insight_tokens())
    titles = re.findall(r"\n## (.+)", src)
    bodies = re.findall(r"\n```\n(.*?)```", src, re.S)
    rows = re.findall(r"\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", src)
    ogp = {int(r[0]): r[3].strip() for r in rows if r[0].isdigit()}
    out = []
    for i, (t, b) in enumerate(zip(titles, bodies), 1):
        out.append({
            "no": i,
            "title": t.split(". ", 1)[-1],
            "body": b.rstrip("\n"),
            "ogp": ogp.get(i, ""),
        })
    return out


def card_pa45(p):
    thumb = (f'<img class="og" src="{OGP_BASE}{p["ogp"]}" alt="" loading="lazy">'
             if p["ogp"].endswith(".png")
             else '<div class="og yt">▶ YouTubeのサムネイルが出ます</div>')
    return f'''
<article class="card">
  <div class="head"><span class="no">{p['no']:02d}</span><h2>{html.escape(p['title'])}</h2>
    <span class="len">{x_len(p['body'])}</span></div>
  {thumb}
  <pre class="body" id="p{p['no']}">{html.escape(p['body'])}</pre>
  <div class="acts">
    <button class="btn copy" data-t="p{p['no']}">本文をコピー</button>
    <a class="btn go" href="{html.escape(intent(p['body']))}" target="_blank" rel="noopener">Xの下書きを開く →</a>
  </div>
  <label class="done-row"><input type="checkbox" class="donebox" data-k="pa45-{p['no']}"> 投稿済みにする</label>
</article>'''


# ── タブ2：X技術Tips ───────────────────────────────────────
STATUS = {
    "draft_saved": ("下書き保存済", "st-done"),
    "ready":       ("下書きまだ", "st-todo"),
    "posted":      ("投稿済", "st-posted"),
}


SERIES = {
    "tips":    ("#", "tips", "時短ワザ"),
    "copasta": ("コパスタ #", "cs", "コパスタ入門"),
}


def card_tips(it):
    prefix, key, sname = SERIES.get(it.get("series", "tips"), SERIES["tips"])
    f = it["folder"]
    img1 = ROOT / "assets" / "x" / "html" / f / f"{f.replace('-', '')}.png"
    rel1 = f"pa45/assets/x/html/{f}/{img1.name}"
    # 2枚目は「同じフォルダ(vol-NN/…b.png)」を優先。無ければ旧構成(vol-NNb/…)にフォールバック
    img2_same = ROOT / "assets" / "x" / "html" / f / f"{f.replace('-', '')}b.png"
    img2_old = ROOT / "assets" / "x" / "html" / f"{f}b" / f"{f.replace('-', '')}b.png"
    if img2_same.exists():
        img2 = img2_same
        rel2 = f"pa45/assets/x/html/{f}/{img2.name}"
    else:
        img2 = img2_old
        rel2 = f"pa45/assets/x/html/{f}b/{img2.name}"
    # 3枚目・4枚目（4枚組Tips対応）。同フォルダの …c.png / …d.png があれば追加。
    extra_shots = ""
    extra_btns = ""
    for suf, lbl in (("c", "3枚目"), ("d", "4枚目")):
        same = ROOT / "assets" / "x" / "html" / f / f"{f.replace('-', '')}{suf}.png"
        sep = ROOT / "assets" / "x" / "html" / f"{f}{suf}" / f"{f.replace('-', '')}{suf}.png"
        if same.exists():
            imgx, relx = same, f"pa45/assets/x/html/{f}/{same.name}"
        elif sep.exists():
            imgx, relx = sep, f"pa45/assets/x/html/{f}{suf}/{sep.name}"
        else:
            continue
        extra_shots += f'\n    <a href="{relx}" target="_blank"><img src="{relx}" alt="{lbl}" loading="lazy"></a>'
        extra_btns += f'\n    <button class="btn copyp" data-p="{html.escape(str(imgx))}">{lbl}パス</button>'
    label, cls = STATUS.get(it["status"], ("―", "st-todo"))
    miss = "" if img1.exists() and img2.exists() else '<div class="warn">PNGが見つかりません</div>'

    # LinkedIn用の詳しい本文（作り方をXより丁寧に）。あればコピー用の隠しpreと専用ボタンを出す。
    li_body = it.get("li_body")
    li_pre = li_copy = ""
    li_flag = ""
    if li_body:
        liid = f"li{key}{it['vol']}"
        li_pre = (f'<pre class="body libody" id="{liid}">'
                  f'{html.escape(li_body)}</pre>')
        li_copy = f'<button class="btn copy li" data-t="{liid}">LinkedIn用をコピー</button>'
        li_flag = '<span class="badge st-li">LinkedIn詳細あり</span>'
    return f'''
<article class="card">
  <div class="head"><span class="no">{prefix}{it['vol']}</span><h2>{html.escape(it['title'])}</h2>
    <span class="badge {cls}">{label}</span>{li_flag}<span class="len">{x_len(it['body'])}</span></div>
  <div class="sub">{html.escape(it['sub'])}</div>
  <div class="shots">
    <a href="{rel1}" target="_blank"><img src="{rel1}" alt="1枚目" loading="lazy"></a>
    <a href="{rel2}" target="_blank"><img src="{rel2}" alt="2枚目" loading="lazy"></a>{extra_shots}
  </div>
  {miss}
  <pre class="body" id="{key}{it['vol']}">{html.escape(it['body'])}</pre>
  {li_pre}
  <div class="acts">
    <button class="btn copy" data-t="{key}{it['vol']}">X用をコピー</button>
    <button class="btn copyp" data-p="{html.escape(str(img1))}">1枚目パス</button>
    <button class="btn copyp" data-p="{html.escape(str(img2))}">2枚目パス</button>{extra_btns}
    <a class="btn go" href="{html.escape(intent(it['body']))}" target="_blank" rel="noopener">Xの下書きを開く →</a>
    {li_copy}<a class="btn li" href="{LI_COMPOSE}" target="_blank" rel="noopener">LinkedInを開く →</a>
  </div>
  <label class="done-row"><input type="checkbox" class="donebox" data-k="{key}-{it['vol']}"> 投稿済みにする</label>
</article>'''


# ── タブ4：ブログ（automate136.com）────────────────────────
BSTATUS = {
    "draft":   ("下書き", "st-todo"),
    "pending": ("下書き（確認待ち）", "st-todo"),
    "future":  ("予約投稿ずみ", "st-done"),
    "publish": ("公開済み", "st-done"),
    "idea":    ("ネタ（未着手）", "st-posted"),
    "private": ("非公開", "st-posted"),
}


# ブログ記事を「PA（Power Automate）」と「コパスタ（Copilot Studio）」に振り分ける。
# blog-board.json の項目に "series": "pa" / "cs" があればそれを最優先（手動で直せる逃げ道）。
# 無いときはスラッグ→タイトルの順で判定する。
#   ・スラッグに copilot-studio / copilotstudio / -cs- が入っていれば コパスタ
#   ・タイトルに "Copilot Studio" / "コパスタ" が入っていれば コパスタ
#   ・それ以外は PA（Copilot単体の記事・Cowork記事・書評などは PA 側に置く）
CS_SLUG_RE = re.compile(r"copilot[-_]?studio|(?:^|[-_])cs[-_]", re.I)
CS_TITLE_RE = re.compile(r"copilot\s*studio|コパスタ", re.I)


def blog_series(b):
    s = str(b.get("series") or "").lower()
    if s in ("pa", "cs"):
        return s
    if CS_SLUG_RE.search(b.get("slug") or ""):
        return "cs"
    if CS_TITLE_RE.search(b.get("title") or ""):
        return "cs"
    return "pa"


def card_blog(b):
    label, cls = BSTATUS.get(b["status"], (b["status"], "st-posted"))
    meta = []
    if b.get("chars"):
        meta.append(f'{b["chars"]:,}字')
    if b.get("modified"):
        meta.append(f'更新 {b["modified"]}')
    if b.get("post_id"):
        meta.append(f'ID {b["post_id"]}')
    if b.get("scheduled"):
        meta.append(f'公開予定 {b["scheduled"]}')

    acts = []
    if b.get("edit_url"):
        verb = "公開記事を編集" if b["status"] == "publish" else "WordPressの下書きを開く"
        acts.append(f'<a class="btn go" href="{html.escape(b["edit_url"])}" target="_blank" '
                    f'rel="noopener">{verb} →</a>')
    if b.get("preview_url") and b["status"] != "publish":
        acts.append(f'<a class="btn" href="{html.escape(b["preview_url"])}" target="_blank" '
                    f'rel="noopener">プレビュー</a>')
    if b["status"] == "publish" and b.get("public_url"):
        acts.append(f'<a class="btn" href="{html.escape(b["public_url"])}" target="_blank" '
                    f'rel="noopener">公開ページ</a>')
    if not acts:
        acts.append('<span class="btn" style="opacity:.5;cursor:default;">WordPress未作成</span>')
    if b.get("folder"):
        acts.append(f'<button class="btn copy3" data-p="{html.escape(str(ROOT / b["folder"][5:]))}">'
                    f'記事フォルダのパス</button>')

    # 仕上げチェック：★＝直さないと出せない／△＝できれば直したい
    todos = b.get("todos") or []
    n_must = sum(1 for t in todos if t.startswith("★"))
    n_nice = len(todos) - n_must
    if b["status"] in ("draft", "pending", "future"):
        if todos:
            lis = "".join(
                f'<li class="{"t-must" if t.startswith("★") else "t-nice"}">{html.escape(t[1:])}</li>'
                for t in todos)
            head = (f'直すところ {n_must}件（要）' if n_must else 'あと少し（任意）')
            todo_html = f'<div class="todo"><b>{head}</b><ul>{lis}</ul></div>'
        else:
            todo_html = '<div class="todo ok"><b>チェックOK — 読み直して予約投稿へ</b></div>'
    else:
        todo_html = ""

    return f'''
<article class="card blogcard" data-mod="{b.get("modified") or ""}" data-chars="{b.get("chars") or 0}"
  data-must="{n_must}" data-nice="{n_must * 100 + n_nice}" data-pid="{b.get("post_id") or 0}">
  <div class="head"><span class="badge {cls}">{label}</span>
    <h2>{html.escape(b["title"])}</h2></div>
  <div class="sub">{" ／ ".join(meta) if meta else "WordPressにはまだ作っていません"}</div>
  <pre class="body">{html.escape(b["summary"] or "（内容メモなし）")}</pre>
  {todo_html}
  <div class="acts">{"".join(acts)}</div>
  <div class="slug">{html.escape(b["slug"])}</div>
</article>'''


# ── タブ：PA45 開催告知（1回につき4本を自動生成）──────────────
# ① 前回終了直後に出す「次回の案内」
# ② 開催週の月曜に出す「リマインド」
# ③ 当日の昼に出す「今夜です」
# ④ 開催15分前に出す「まもなく」
# それぞれ connpass URL を必ず入れる（貼るとOGPカードが出る）＆140字以内。
# PA45＝Power Automateを45分で学ぶハンズオン講座、と毎回わかるようにする。
# 本文でPower Automateを明記するので #PowerAutomate ハッシュタグは付けない（重複回避＆字数確保）。
ANN_SLOTS = [
    {
        "n": 1, "when": "① 前回終了直後", "hint": "前回の回が終わった直後（約1週間前）に",
        "tpl": ("【PA45 第{vol}回】{md}（{wd}）{time}〜\n"
                "PA45＝Power Automateの45分ハンズオン講座。\n"
                "テーマは「{topic}」。{line}\n"
                "見るだけ参加もOK。申込はこちら👇\n{url}"),
    },
    {
        "n": 2, "when": "② 開催週の月曜", "hint": "開催週の月曜あたりに",
        "tpl": ("今週{wd}曜 {time}〜、PA45 第{vol}回です。\n"
                "PA45＝Power Automateの45分ハンズオン講座。\n"
                "テーマは「{topic}」。{line}\n"
                "実際の画面を見ながら進めます。詳細は👇\n{url}"),
    },
    {
        "n": 3, "when": "③ 当日の昼", "hint": "開催当日の昼に",
        "tpl": ("本日 {time}〜、PA45 第{vol}回です。\n"
                "PA45＝Power Automateの45分ハンズオン講座。\n"
                "テーマは「{topic}」。\n"
                "見るだけ参加もOK。申込はこちら👇\n{url}"),
    },
    {
        "n": 4, "when": "④ 開催15分前", "hint": "開催15分前（20:00ごろ）に",
        "tpl": ("まもなく {time}〜、PA45 第{vol}回です。\n"
                "PA45＝Power Automateの45分ハンズオン講座。\n"
                "テーマは「{topic}」。\n"
                "オンライン開催、参加はこちら👇\n{url}"),
    },
]


def ann_bodies(ev):
    m, d = ev["date"].split("-")[1:]
    md = f"{int(m)}/{int(d)}"
    ctx = {
        "vol": ev["vol"], "md": md, "wd": ev.get("wd", "木"),
        "time": ev.get("time", "20:15"), "topic": ev["topic"],
        "line": ev.get("line", ""), "url": ev["connpass_url"],
    }
    return [(s, s["tpl"].format(**ctx)) for s in ANN_SLOTS]


def cards_announce(ev):
    if ev.get("og_image"):
        thumb = f'<img class="og" src="{html.escape(ev["og_image"])}" alt="" loading="lazy">'
    else:
        thumb = '<div class="og yt">connpassのOGPカードが出ます</div>'
    cards = []
    for slot, body in ann_bodies(ev):
        n = c140(body)
        over = ' style="color:#b3261e"' if n > 140 else ""
        key = f"ann-{ev['vol']}-{slot['n']}"
        cards.append(f'''
<article class="card">
  <div class="head"><span class="no">{slot['when']}</span>
    <span class="len len140"{over}>{n}</span></div>
  <div class="sub">{html.escape(slot['hint'])}投稿</div>
  {thumb}
  <pre class="body" id="{key}">{html.escape(body)}</pre>
  <div class="acts">
    <button class="btn copy" data-t="{key}">本文をコピー</button>
    <a class="btn go" href="{html.escape(intent(body))}" target="_blank" rel="noopener">Xの下書きを開く →</a>
  </div>
  <label class="done-row"><input type="checkbox" class="donebox" data-k="{key}"> 投稿済みにする</label>
</article>''')
    return cards


def group_announce(ev):
    m, d = ev["date"].split("-")[1:]
    md = f"{int(m)}/{int(d)}"
    return f'''
<div class="evgroup">
  <div class="evhead"><b>第{ev['vol']}回</b>
    <span class="th">{md}（{ev.get('wd','木')}）{ev.get('time','20:15')}〜 ／ {html.escape(ev['topic'])}</span>
    <a href="{html.escape(ev['connpass_url'])}" target="_blank" rel="noopener">connpassを開く →</a></div>
  <div class="grid">{"".join(cards_announce(ev))}</div>
</div>'''


# ── タブ：LinkedIn（切り口ローテ）─────────────────────────────
# これまでの活動を少しずつ、いろんな角度で投稿するための在庫。
# LinkedInは本文の事前入力ができないため、「本文をコピー」→「LinkedInを開く」→貼り付け。
# 文字数上限は3000（Xの280とは別物）。
def card_linkedin(p):
    n = len(p["body"])
    over = ' style="color:#b3261e"' if n > 3000 else ""
    key = f"li-{p['no']}"
    return f'''
<article class="card">
  <div class="head"><span class="no">LI-{p['no']:02d}</span><h2>{html.escape(p['title'])}</h2>
    <span class="ser ser-li">{html.escape(p.get('angle', ''))}</span>
    <span class="len len3000"{over}>{n}</span></div>
  <pre class="body" id="{key}">{html.escape(p['body'])}</pre>
  <div class="acts">
    <button class="btn copy go" data-t="{key}">本文をコピー</button>
    <a class="btn" href="{LI_COMPOSE}" target="_blank" rel="noopener">LinkedInを開く →</a>
  </div>
  <label class="done-row"><input type="checkbox" class="donebox" data-k="{key}"> 投稿済みにする</label>
</article>'''


# ── タブ：アンケート考察（開催後の振り返り。ネガも正直に＋運営の改善視点）──
def card_insight(p, idx):
    key = f"ins-{p['vol']}-{idx}"
    n = x_len(p["body"])
    angle = html.escape(p.get("angle", ""))
    return f'''
<article class="card">
  <div class="head"><span class="no">第{p['vol']}回</span><h2>{html.escape(p['title'])}</h2>
    {f'<span class="ser ser-li">{angle}</span>' if angle else ''}
    <span class="len">{n}</span></div>
  <pre class="body" id="{key}">{html.escape(p['body'])}</pre>
  <div class="acts">
    <button class="btn copy" data-t="{key}">本文をコピー</button>
    <a class="btn go" href="{html.escape(intent(p['body']))}" target="_blank" rel="noopener">Xの下書きを開く →</a>
  </div>
  <label class="done-row"><input type="checkbox" class="donebox" data-k="{key}"> 投稿済みにする</label>
</article>'''


CSS = """
:root{--bg:#f6f7f9;--card:#fff;--tx:#15202b;--mu:#5b6b7b;--ln:#e3e9f0;--ac:#1d9bf0;--li:#0a66c2;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Noto Sans JP","Yu Gothic UI",sans-serif;background:var(--bg);color:var(--tx);
  line-height:1.7;padding:26px 16px 60px}
.wrap{max-width:1180px;margin:0 auto}
h1{font-size:24px;font-weight:900;margin-bottom:4px}
.lead{font-size:13px;color:var(--mu)}
.tabs{display:flex;gap:8px;margin:18px 0 14px;border-bottom:1px solid var(--ln)}
.tab{font-size:14px;font-weight:700;color:var(--mu);background:none;border:none;cursor:pointer;
  padding:11px 18px;border-bottom:3px solid transparent;font-family:inherit}
.tab.on{color:var(--ac);border-bottom-color:var(--ac)}
.tab .c{font-size:11px;color:var(--mu);font-family:ui-monospace,monospace;margin-left:6px}
.note{font-size:12px;color:var(--mu);background:#fff;border-left:3px solid var(--ac);
  padding:12px 14px;border-radius:8px;margin-bottom:20px}
.pane{display:none}.pane.on{display:block}
.subtabs{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}
.subtab{font-size:13.5px;font-weight:700;color:var(--mu);background:#fff;border:1px solid var(--ln);
  border-radius:999px;padding:7px 16px;cursor:pointer;line-height:1.4}
.subtab.on{color:#fff;background:var(--ac);border-color:var(--ac)}
.subtab .c{font-size:11px;font-family:ui-monospace,monospace;margin-left:7px;color:var(--mu)}
.subtab.on .c{color:rgba(255,255,255,.85)}
.subpane{display:none}.subpane.on{display:block}
.sortbar{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:0 0 16px;
  background:#eef3f8;border-radius:10px;padding:9px 14px;font-size:13px;font-weight:700}
.sortbar select{font:inherit;font-weight:700;padding:5px 10px;border:1px solid #cbd5e1;
  border-radius:8px;background:#fff;color:var(--tx)}
.sortbar .th{color:var(--mu);font-weight:500;font-size:12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--ln);border-radius:14px;padding:14px;
  display:flex;flex-direction:column;gap:10px}
.head{display:flex;align-items:center;gap:8px}
.no{font-family:ui-monospace,monospace;font-size:11px;background:#eef3f8;color:var(--mu);
  padding:2px 7px;border-radius:6px;white-space:nowrap}
.head h2{font-size:14px;font-weight:700;flex:1}
.len{font-size:11px;color:var(--mu);font-family:ui-monospace,monospace;white-space:nowrap}
.len::after{content:"/280";opacity:.55}
.sub{font-size:11.5px;color:var(--mu);margin-top:-4px}
.badge{font-size:10px;font-weight:700;padding:2px 8px;border-radius:999px;margin-left:4px;white-space:nowrap}
.st-todo{background:#fff3d6;color:#8a5a00}.st-done{background:#e2f7ee;color:#0b7a4b}
.st-posted{background:#eceff3;color:#5b6b7b}
.og{width:100%;border-radius:10px;border:1px solid var(--ln);display:block}
.og.yt{background:#111;color:#bbb;font-size:12px;text-align:center;padding:34px 8px}
.shots{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.shots img{width:100%;border-radius:8px;border:1px solid var(--ln);display:block}
.warn{font-size:11px;color:#b3261e}
.todo{font-size:12px;background:#fffaf0;border:1px solid #f0e0c0;border-radius:10px;padding:9px 11px}
.todo b{display:block;font-size:11.5px;color:#8a5a00;margin-bottom:5px}
.todo ul{margin:0;padding-left:16px}
.todo li{margin:2px 0;line-height:1.6}
.todo li.t-must{color:#b3261e}
.todo li.t-nice{color:#5b6b7b}
.todo.ok{background:#f2fbf6;border-color:#cfe9dc}
.todo.ok b{color:#0b7a4b;margin:0}
.bgroup{margin-bottom:28px}
.bhead{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;background:#eef3f8;
  border-radius:10px;padding:9px 12px;margin-bottom:12px}
.bhead b{font-size:15px}
.bhead .th{color:var(--mu);font-size:12px}
.body{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;font-family:inherit;
  font-size:13px;background:#fafbfc;border:1px solid var(--ln);border-radius:10px;padding:11px 12px;flex:1}
.acts{display:flex;gap:8px;flex-wrap:wrap}
.btn{font-size:12.5px;font-weight:700;border-radius:9px;padding:9px 12px;border:1px solid var(--ln);
  background:#fff;color:var(--tx);cursor:pointer;text-decoration:none;text-align:center;font-family:inherit}
.btn.go{background:var(--ac);border-color:var(--ac);color:#fff;flex:1;min-width:140px}
.btn.li{background:var(--li);border-color:var(--li);color:#fff}
.btn.done{background:#0e9f6e;border-color:#0e9f6e;color:#fff}
.done-row{font-size:11.5px;color:var(--mu);display:flex;align-items:center;gap:6px;cursor:pointer;
  user-select:none;margin-top:-2px}
.card.posted{opacity:.42}
.card.posted .og,.card.posted .shots{filter:grayscale(1)}
.filter{display:flex;align-items:center;gap:14px;margin-bottom:14px;font-size:12.5px;color:var(--mu)}
.filter label{display:flex;align-items:center;gap:6px;cursor:pointer;user-select:none}
.filter .cnt{font-family:ui-monospace,monospace}
body.hide-posted .card.posted{display:none}
.blogcard .head{align-items:flex-start}
.blogcard .head h2{font-size:13.5px;line-height:1.5}
.blogcard .body{font-size:12px;color:var(--mu);max-height:150px;overflow:auto}
.slug{font-family:ui-monospace,monospace;font-size:10px;color:#9db0c2}
.ser{font-size:10px;font-weight:700;padding:1px 7px;border-radius:5px;margin-right:6px}
.ser-tips{background:#e8f1fb;color:#0b3e72}
.ser-cs{background:#efeafd;color:#4b31a8}
.ser-li{background:#e5eff9;color:#0a66c2}
.st-li{background:#e5eff9;color:#0a66c2}
.libody{background:#f2f7fc;border-color:#cfe0f2}
.libody::before{content:"LinkedIn用（作り方くわしめ）";display:block;font-size:10.5px;font-weight:800;
  color:#0a66c2;margin:-2px 0 6px}
.len140::after{content:"/140"}
.len3000::after{content:"/3000";opacity:.55}
.evgroup{margin-bottom:28px}
.evhead{display:flex;flex-wrap:wrap;align-items:center;gap:10px;background:#eef3f8;
  border-radius:10px;padding:10px 14px;margin-bottom:12px;font-size:13px}
.evhead b{font-size:15px}
.evhead .th{color:var(--mu)}
.evhead a{margin-left:auto;color:var(--ac);font-weight:700;font-size:12px;text-decoration:none;white-space:nowrap}
"""

JS = """
function show(pane){
  document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('on', x.dataset.pane===pane));
  document.querySelectorAll('.pane').forEach(x=>x.classList.toggle('on', x.id===pane));
}
const HASH={'pane-pa45':'#pa45','pane-announce':'#announce','pane-tips':'#tips','pane-cs':'#cs','pane-blog':'#blog','pane-linkedin':'#linkedin','pane-insight':'#insight'};
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
  show(t.dataset.pane);
  history.replaceState(null,'', HASH[t.dataset.pane]||'#pa45');
}));
for(const [pane,h] of Object.entries(HASH)){ if(location.hash===h) show(pane); }

// localStorage が使えない開き方（data: URL など）でも他の機能を巻き込まないように包む
function lsGet(k){try{return localStorage.getItem(k)}catch(e){return null}}
function lsSet(k,v){try{localStorage.setItem(k,v)}catch(e){}}

// ── ブログタブ：PA／コパスタのサブタブ ──────────────────────
document.querySelectorAll('.subtab').forEach(t=>t.addEventListener('click',()=>{
  document.querySelectorAll('.subtab').forEach(x=>x.classList.toggle('on',x===t));
  document.querySelectorAll('.subpane').forEach(x=>x.classList.toggle('on',x.id===t.dataset.sub));
  lsSet('pa45-blog-sub',t.dataset.sub);
}));
(function(){
  const saved=lsGet('pa45-blog-sub');
  if(saved){const t=document.querySelector('.subtab[data-sub="'+saved+'"]'); if(t)t.click();}
})();

// ── ブログタブ：並び順（各グループの中を並べ替える）─────────────
const BSORT={
  rec:(a,b)=>(+a.dataset.nice - +b.dataset.nice) || (a.dataset.mod<b.dataset.mod?1:-1),
  newest:(a,b)=>(a.dataset.mod<b.dataset.mod?1:(a.dataset.mod>b.dataset.mod?-1:0)),
  oldest:(a,b)=>(a.dataset.mod>b.dataset.mod?1:(a.dataset.mod<b.dataset.mod?-1:0)),
  short:(a,b)=>(+a.dataset.chars - +b.dataset.chars),
  long:(a,b)=>(+b.dataset.chars - +a.dataset.chars),
  pid:(a,b)=>(+a.dataset.pid - +b.dataset.pid)
};
(function(){
  const sel=document.getElementById('bsort');
  if(!sel) return;
  function apply(){
    const f=BSORT[sel.value]||BSORT.rec;
    document.querySelectorAll('#pane-blog .bgroup .grid').forEach(g=>{
      Array.from(g.children).sort(f).forEach(c=>g.appendChild(c));
    });
    lsSet('pa45-blog-sort',sel.value);
  }
  const saved=lsGet('pa45-blog-sort');
  if(saved&&BSORT[saved]) sel.value=saved;
  sel.addEventListener('change',apply);
  apply();
})();
function flash(b,msg){const o=b.textContent;b.textContent=msg;b.classList.add('done');
  setTimeout(()=>{b.textContent=o;b.classList.remove('done')},1500);}
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{
  await navigator.clipboard.writeText(document.getElementById(b.dataset.t).textContent);
  flash(b,'コピーしました');
}));
document.querySelectorAll('.copy3,.copyp').forEach(b=>b.addEventListener('click',async()=>{
  await navigator.clipboard.writeText(b.dataset.p);
  flash(b,'パスをコピー');
}));

// 投稿済みチェック（このPCのブラウザに保存。35本を数ヶ月かけて回すための進捗管理）
const KEY='pa45-x-posted';
const posted=new Set(JSON.parse(localStorage.getItem(KEY)||'[]'));
function count(){
  const n=[...document.querySelectorAll('.donebox')].filter(c=>!c.checked).length;
  document.getElementById('remain').textContent=n;
}
document.querySelectorAll('.donebox').forEach(cb=>{
  const card=cb.closest('.card');
  if(posted.has(cb.dataset.k)){cb.checked=true;card.classList.add('posted');}
  cb.addEventListener('change',()=>{
    card.classList.toggle('posted',cb.checked);
    cb.checked?posted.add(cb.dataset.k):posted.delete(cb.dataset.k);
    localStorage.setItem(KEY,JSON.stringify([...posted]));
    count();
  });
});
document.getElementById('hideposted').addEventListener('change',e=>{
  document.body.classList.toggle('hide-posted',e.target.checked);
});
count();
"""


def main():
    pa45 = load_pa45()
    tips = json.loads((ROOT / "data" / "x-tips-board.json").read_text(encoding="utf-8"))["items"]

    tips_data = json.loads((ROOT / "data" / "x-tips-board.json").read_text(encoding="utf-8"))
    snote = tips_data.get("series_note", {})
    pa_tips = [t for t in tips if t.get("series", "tips") == "tips"]
    # 表示順：order（小さいほど上＝保存したくなる実務ネタを前に）→ 無ければ vol 降順で後ろに
    pa_tips.sort(key=lambda t: (t.get("order", 10000), -t["vol"]))
    cs = [t for t in tips if t.get("series") == "copasta"]

    bf = ROOT / "data" / "blog-board.json"
    blog = json.loads(bf.read_text(encoding="utf-8"))["items"] if bf.exists() else []
    n_draft = sum(1 for b in blog if b["status"] in ("draft", "pending"))

    # 仕上げ→予約投稿の進み具合で4つに分ける
    def _must(b):
        return sum(1 for t in (b.get("todos") or []) if t.startswith("★"))

    # まず直近1か月ぶんを片付ける運用なので、それより古い下書きは別枠にまとめる
    CUT = (datetime.now(timezone(timedelta(hours=9))) - timedelta(days=31)).strftime("%Y-%m-%d")

    def _recent(b):
        return (b.get("modified") or "") >= CUT

    def bgroup(title, note, rows):
        if not rows:
            return ""
        return (f'<div class="bgroup"><div class="bhead"><b>{title}</b>'
                f'<span class="th">{note}</span>'
                f'<span class="th">{len(rows)}本</span></div>'
                f'<div class="grid">{"".join(card_blog(b) for b in rows)}</div></div>')

    def blog_pane(rows):
        """1つのシリーズぶんのブログ一覧HTMLと、直近の本数を返す。"""
        b_future = [b for b in rows if b["status"] == "future"]
        drafts = [b for b in rows if b["status"] in ("draft", "pending")]
        b_ready = [b for b in drafts if _recent(b) and not _must(b)]
        b_fix = [b for b in drafts if _recent(b) and _must(b)]
        b_old = [b for b in drafts if not _recent(b)]
        b_rest = [b for b in rows if b["status"] not in ("draft", "pending", "future")]
        b_old.sort(key=lambda b: b.get("modified") or "", reverse=True)
        b_ready.sort(key=lambda b: b.get("modified") or "", reverse=True)
        b_fix.sort(key=lambda b: (_must(b), -int((b.get("modified") or "0").replace("-", ""))))
        h = (
            bgroup("予約投稿ずみ", "あとは日時が来るのを待つだけ", b_future)
            + bgroup("仕上げれば出せる", "機械チェックは通過。読み直して予約投稿へ", b_ready)
            + bgroup("直しが要る", "赤い項目を消してから予約投稿", b_fix)
            + bgroup("旧い下書き（1か月以上前）", "今の運用の対象外。手を付けるならタイトル・スラッグから", b_old)
            + bgroup("ネタ・公開済み", "参考", b_rest)
        )
        return h or '<p class="lead">この区分の記事はありません。</p>', len(b_ready), len(b_fix)

    blog_pa = [b for b in blog if blog_series(b) == "pa"]
    blog_cs = [b for b in blog if blog_series(b) == "cs"]
    pa_html, pa_ready, pa_fix = blog_pane(blog_pa)
    cs_html, cs_ready, cs_fix = blog_pane(blog_cs)

    af = ROOT / "data" / "announce-events.json"
    ann = json.loads(af.read_text(encoding="utf-8"))["events"] if af.exists() else []
    ann.sort(key=lambda e: e["vol"])
    n_ann = len(ann) * 4

    lif = ROOT / "data" / "linkedin-board.json"
    lidata = json.loads(lif.read_text(encoding="utf-8")) if lif.exists() else {}
    linkedin = lidata.get("items", [])
    li_note = lidata.get("note", "")

    inf = ROOT / "data" / "insight-posts.json"
    insdata = json.loads(inf.read_text(encoding="utf-8")) if inf.exists() else {}
    ins_posts = insdata.get("items", [])
    # 新しい回を上に。回の中は元の並び（考察A→B→C→D）を保つ
    ins_posts = sorted(enumerate(ins_posts), key=lambda t: (-int(t[1]["vol"]), t[0]))
    ins_posts = [x[1] for x in ins_posts]
    ins_cards = "".join(card_insight(p, i) for i, p in enumerate(ins_posts))

    page = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>PA45 X投稿ボード</title>
<style>{CSS}</style></head><body><div class="wrap">
<h1>X投稿ボード</h1>
<p class="lead">切り口ローテと技術Tipsの在庫。投稿ボタンを押すのは自分。<br>
<b>ビルド: {BUILT_AT}</b>　※この時刻が古いときは <b>Ctrl+Shift+R</b> で再読み込み。</p>

<div class="tabs">
  <button class="tab on" data-pane="pane-pa45">PA45（切り口）<span class="c">{len(pa45)}本</span></button>
  <button class="tab" data-pane="pane-announce">開催告知<span class="c">{n_ann}本</span></button>
  <button class="tab" data-pane="pane-tips">X技術Tips<span class="c">{len(pa_tips)}本</span></button>
  <button class="tab" data-pane="pane-cs">コパスタ<span class="c">{len(cs)}本</span></button>
  <button class="tab" data-pane="pane-blog">ブログ<span class="c">PA {pa_ready + pa_fix}／コパスタ {cs_ready + cs_fix}</span></button>
  <button class="tab" data-pane="pane-linkedin">LinkedIn<span class="c">{len(linkedin)}本</span></button>
  <button class="tab" data-pane="pane-insight">考察<span class="c">{len(ins_posts)}本</span></button>
</div>

<div class="filter">
  <span>未投稿 <b class="cnt" id="remain">-</b> 本</span>
  <label><input type="checkbox" id="hideposted"> 投稿済みを隠す</label>
</div>

<section class="pane on" id="pane-pa45">
  <div class="note">
    <b>「Xの下書きを開く」</b>で本文入りの投稿画面が開きます。そのまま投稿するか、<b>Escape →「保存」</b>で下書きへ。<br>
    リンク先は全ページ専用OGPを設定済みなので、貼るとカードが出ます。週2本くらい、同じ切り口が続かないように混ぜる。開催週は16（募集）を必ず1本。
  </div>
  <div class="grid">{"".join(card_pa45(p) for p in pa45)}</div>
</section>

<section class="pane" id="pane-announce">
  <div class="note">
    <b>PA45 各回の開催告知。</b>1回につき4本（<b>①前回終了直後 → ②開催週の月曜 → ③当日の昼 → ④開催15分前</b>）を用意しています。<br>
    どれも<b>connpassのイベントURL入り</b>なので、貼るとOGPカード（サムネイル）が自動で出ます。全部140字以内。<br>
    新しい回は connpass でイベントを作ったら <code>data/announce-events.json</code> に1件足して <code>python scripts/build-x-board.py</code>。
  </div>
  {"".join(group_announce(e) for e in ann) or '<p class="lead">告知対象の回がありません。data/announce-events.json に追加してください。</p>'}
</section>

<section class="pane" id="pane-tips">
  <div class="note">
    Power Automateの時短ワザ（#PowerAutomate）。画像2枚を1ツイートに添付します。<br>
    <b>「Xの下書きを開く」→ 画像ボタン → ファイル選択の枠に「画像2枚のパス」を貼り付け</b>で2枚同時に選べます。貼り付け順＝添付順（概念 → 作り方）。<br>
    <b>LinkedInにも同じ内容を出せます</b>（自分の投稿の再利用はOK）。<b>本文をコピー →「LinkedInを開く」→ 貼り付け → 画像で同じ2枚を添付</b>。<br>
    Vol番号＝フォルダ番号（Vol.69以降が一致）。
  </div>
  <div class="grid">{"".join(card_tips(t) for t in pa_tips)}</div>
</section>

<section class="pane" id="pane-cs">
  <div class="note">{snote.get("copasta", "Copilot Studio（コパスタ）シリーズ。画像2枚を1ツイートに一緒に添付します。")}</div>
  <div class="grid">{"".join(card_tips(c) for c in cs)}</div>
</section>

<section class="pane" id="pane-blog">
  <div class="note">
    automate136.com の投稿状況。<b>状態はWordPressから直接取得</b>しているので、ここが今の実態です。<br>
    <b>Power Automate と コパスタ（Copilot Studio）でタブを分けています。</b>まず PA から、上から順に1本ずつ仕上げて、WordPressの「公開」→<b>日時を指定して予約投稿</b>していく用。<br>
    <b>並び順</b>は下のプルダウンで変えられます（どのグループの中も同じ順に並べ替わります）。
    対象は<b>直近1か月に書いた下書き</b>。それより古いものは各タブの「旧い下書き」にまとめてあります。
    <span style="color:#b3261e">赤い項目＝直さないと出せないもの</span>（アイキャッチ・スラッグ・免責・禁止語など）、グレー＝できれば直したいもの。<br>
    最新にするには <code>python scripts/fetch-blog-status.py</code> → <code>python scripts/build-x-board.py</code>。
    <b>予約投稿の設定は必ずプレビュー確認のうえ自分で。</b>
    振り分けが違うときは <code>data/blog-board.json</code> のその記事に <code>"series": "pa"</code> か <code>"cs"</code> を書けば固定できます。
  </div>

  <div class="subtabs">
    <button class="subtab on" data-sub="bp-pa">Power Automate<span class="c">直近{pa_ready + pa_fix}本・出せる{pa_ready}本</span></button>
    <button class="subtab" data-sub="bp-cs">コパスタ（Copilot Studio）<span class="c">直近{cs_ready + cs_fix}本・出せる{cs_ready}本</span></button>
  </div>

  <div class="sortbar">
    <label for="bsort">並び順</label>
    <select id="bsort">
      <option value="rec">仕上げやすい順（直しが少ない順）</option>
      <option value="newest">更新が新しい順</option>
      <option value="oldest">更新が古い順</option>
      <option value="short">文字数が少ない順</option>
      <option value="long">文字数が多い順</option>
      <option value="pid">記事ID順（古い記事から）</option>
    </select>
    <span class="th">上から順に片付けていく用。選んだ順番はこのブラウザに残ります。</span>
  </div>

  <div class="subpane on" id="bp-pa">{pa_html}</div>
  <div class="subpane" id="bp-cs">{cs_html}</div>
</section>

<section class="pane" id="pane-linkedin">
  <div class="note">
    {li_note or "LinkedIn投稿の在庫（切り口ローテ）。"}<br>
    切り口が続かないよう、週1本くらいのペースで混ぜて出すのがおすすめ。追加は <code>data/linkedin-board.json</code> に1件足して <code>python scripts/build-x-board.py</code>。
  </div>
  <div class="grid">{"".join(card_linkedin(p) for p in linkedin)}</div>
</section>

<section class="pane" id="pane-insight">
  <div class="note">
    <b>各回のアンケート考察。</b>その回の結果（理解度・役立ち度・自由コメント）から、<b>良かった点だけでなく難しかった点も正直に</b>拾い、<b>「伝える側としてどう改善するか」</b>を1本ずつ短くまとめたもの。全部140字以内。<br>
    盛らない・脚色しない。新しい回は週次タスクが <code>data/insight-posts.json</code> に足して自動生成します（手で足すときは1件書いて <code>python scripts/build-x-board.py</code>）。
  </div>
  <div class="grid">{ins_cards or '<p class="lead">考察の下書きがありません。data/insight-posts.json に追加してください。</p>'}</div>
</section>

</div><script>{JS}</script></body></html>'''

    OUT.write_text(page, encoding="utf-8")
    print(f"[OK] {OUT}")
    print(f"  PA45 {len(pa45)}本 / 開催告知 {n_ann}本（{len(ann)}回×4）"
          f" / X技術Tips {len(pa_tips)}本 / コパスタ {len(cs)}本"
          f" / ブログ {len(blog)}本（下書き{n_draft}｜PA {len(blog_pa)}・コパスタ {len(blog_cs)}）"
          f" / LinkedIn {len(linkedin)}本")
    for e in ann:
        for slot, body in ann_bodies(e):
            print(f"    第{e['vol']}回 {slot['when']}: {c140(body)}字")


if __name__ == "__main__":
    main()

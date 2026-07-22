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
from pathlib import Path

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


# ── タブ1：PA45 切り口ローテ ────────────────────────────────
def load_pa45():
    src = (ROOT / "data" / "drafts" / "x-pa45-rotation.md").read_text(encoding="utf-8")
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


def card_tips(it, prefix="#", key="tips"):
    f = it["folder"]
    img1 = ROOT / "assets" / "x" / "html" / f / f"{f.replace('-', '')}.png"
    img2 = ROOT / "assets" / "x" / "html" / f"{f}b" / f"{f.replace('-', '')}b.png"
    rel1 = f"pa45/assets/x/html/{f}/{img1.name}"
    rel2 = f"pa45/assets/x/html/{f}b/{img2.name}"
    paths = f'"{img1}" "{img2}"'
    label, cls = STATUS.get(it["status"], ("―", "st-todo"))
    miss = "" if img1.exists() and img2.exists() else '<div class="warn">PNGが見つかりません</div>'
    return f'''
<article class="card">
  <div class="head"><span class="no">{prefix}{it['vol']}</span><h2>{html.escape(it['title'])}</h2>
    <span class="badge {cls}">{label}</span><span class="len">{x_len(it['body'])}</span></div>
  <div class="sub">{html.escape(it['sub'])}</div>
  <div class="shots">
    <a href="{rel1}" target="_blank"><img src="{rel1}" alt="1枚目" loading="lazy"></a>
    <a href="{rel2}" target="_blank"><img src="{rel2}" alt="2枚目" loading="lazy"></a>
  </div>
  {miss}
  <pre class="body" id="{key}{it['vol']}">{html.escape(it['body'])}</pre>
  <div class="acts">
    <button class="btn copy" data-t="{key}{it['vol']}">本文をコピー</button>
    <button class="btn copy2" data-p='{html.escape(paths)}'>画像2枚のパス</button>
    <a class="btn go" href="{html.escape(intent(it['body']))}" target="_blank" rel="noopener">Xの下書きを開く →</a>
  </div>
  <label class="done-row"><input type="checkbox" class="donebox" data-k="{key}-{it['vol']}"> 投稿済みにする</label>
</article>'''


# ── タブ4：ブログ（automate136.com）────────────────────────
BSTATUS = {
    "draft":   ("下書き", "st-todo"),
    "publish": ("公開済み", "st-done"),
    "idea":    ("ネタ（未着手）", "st-posted"),
    "private": ("非公開", "st-posted"),
}


def card_blog(b):
    label, cls = BSTATUS.get(b["status"], (b["status"], "st-posted"))
    meta = []
    if b.get("chars"):
        meta.append(f'{b["chars"]:,}字')
    if b.get("modified"):
        meta.append(f'更新 {b["modified"]}')
    if b.get("post_id"):
        meta.append(f'ID {b["post_id"]}')

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
    acts.append(f'<button class="btn copy3" data-p="{html.escape(str(ROOT / b["folder"][5:]))}">'
                f'記事フォルダのパス</button>')

    return f'''
<article class="card blogcard">
  <div class="head"><span class="badge {cls}">{label}</span>
    <h2>{html.escape(b["title"])}</h2></div>
  <div class="sub">{" ／ ".join(meta) if meta else "WordPressにはまだ作っていません"}</div>
  <pre class="body">{html.escape(b["summary"] or "（内容メモなし）")}</pre>
  <div class="acts">{"".join(acts)}</div>
  <div class="slug">{html.escape(b["slug"])}</div>
</article>'''


CSS = """
:root{--bg:#f6f7f9;--card:#fff;--tx:#15202b;--mu:#5b6b7b;--ln:#e3e9f0;--ac:#1d9bf0;}
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
.body{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;font-family:inherit;
  font-size:13px;background:#fafbfc;border:1px solid var(--ln);border-radius:10px;padding:11px 12px;flex:1}
.acts{display:flex;gap:8px;flex-wrap:wrap}
.btn{font-size:12.5px;font-weight:700;border-radius:9px;padding:9px 12px;border:1px solid var(--ln);
  background:#fff;color:var(--tx);cursor:pointer;text-decoration:none;text-align:center;font-family:inherit}
.btn.go{background:var(--ac);border-color:var(--ac);color:#fff;flex:1;min-width:140px}
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
"""

JS = """
function show(pane){
  document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('on', x.dataset.pane===pane));
  document.querySelectorAll('.pane').forEach(x=>x.classList.toggle('on', x.id===pane));
}
const HASH={'pane-pa45':'#pa45','pane-tips':'#tips','pane-cs':'#cs','pane-blog':'#blog'};
document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
  show(t.dataset.pane);
  history.replaceState(null,'', HASH[t.dataset.pane]||'#pa45');
}));
for(const [pane,h] of Object.entries(HASH)){ if(location.hash===h) show(pane); }
function flash(b,msg){const o=b.textContent;b.textContent=msg;b.classList.add('done');
  setTimeout(()=>{b.textContent=o;b.classList.remove('done')},1500);}
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',async()=>{
  await navigator.clipboard.writeText(document.getElementById(b.dataset.t).textContent);
  flash(b,'コピーしました');
}));
document.querySelectorAll('.copy3').forEach(b=>b.addEventListener('click',async()=>{
  await navigator.clipboard.writeText(b.dataset.p);
  flash(b,'パスをコピー');
}));
document.querySelectorAll('.copy2').forEach(b=>b.addEventListener('click',async()=>{
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

    csf = ROOT / "data" / "x-copasta-board.json"
    cs_data = json.loads(csf.read_text(encoding="utf-8")) if csf.exists() else {"items": [], "note_html": ""}
    cs = cs_data["items"]

    bf = ROOT / "data" / "blog-board.json"
    blog = json.loads(bf.read_text(encoding="utf-8"))["items"] if bf.exists() else []
    n_draft = sum(1 for b in blog if b["status"] == "draft")

    page = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PA45 X投稿ボード</title>
<style>{CSS}</style></head><body><div class="wrap">
<h1>X投稿ボード</h1>
<p class="lead">切り口ローテと技術Tipsの在庫。投稿ボタンを押すのは自分。</p>

<div class="tabs">
  <button class="tab on" data-pane="pane-pa45">PA45（切り口）<span class="c">{len(pa45)}本</span></button>
  <button class="tab" data-pane="pane-tips">X技術Tips<span class="c">{len(tips)}本</span></button>
  <button class="tab" data-pane="pane-cs">コパスタ<span class="c">{len(cs)}本</span></button>
  <button class="tab" data-pane="pane-blog">ブログ<span class="c">下書き{n_draft}本</span></button>
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

<section class="pane" id="pane-tips">
  <div class="note">
    画像2枚つきなので手順が1つ増えます。<b>「Xの下書きを開く」→ 画像ボタン → ファイル選択の枠に「画像2枚のパス」を貼り付け</b>で2枚同時に選べます。<br>
    貼り付け順＝添付順（概念 → 作り方）。Vol番号＝フォルダ番号（Vol.69以降）。
  </div>
  <div class="grid">{"".join(card_tips(t) for t in tips)}</div>
</section>

<section class="pane" id="pane-cs">
  <div class="note">{cs_data.get("note_html") or "Copilot Studio（コパスタ）シリーズ。画像2枚を1ツイートに一緒に添付します。"}</div>
  <div class="grid">{"".join(card_tips(c, prefix="コパスタ #", key="cs") for c in cs)}</div>
</section>

<section class="pane" id="pane-blog">
  <div class="note">
    automate136.com の投稿状況。<b>状態はWordPressから直接取得</b>しているので、ここが今の実態です。<br>
    最新にするには <code>python scripts/fetch-blog-status.py</code> → <code>python scripts/build-x-board.py</code>。
    <b>公開は必ずプレビュー確認のうえ手動で。</b>
  </div>
  <div class="grid">{"".join(card_blog(b) for b in blog)}</div>
</section>

</div><script>{JS}</script></body></html>'''

    OUT.write_text(page, encoding="utf-8")
    print(f"[OK] {OUT}")
    print(f"  PA45 {len(pa45)}本 / 技術Tips {len(tips)}本 / コパスタ {len(cs)}本 / ブログ {len(blog)}本（下書き{n_draft}）")


if __name__ == "__main__":
    main()

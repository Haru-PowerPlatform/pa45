#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
各回の「資料リンク集」ページ(slides/vol-NN/links.html)を生成し、
受講生向けサイト sessions/index.html の各カード＋次回枠に
「資料リンク集」ボタンを差し込む。
既存カードのURL(スライド/ZIP/ブログ/YouTube)を再利用するので壊れリンクは出ない。
"""
import re, os, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESS = os.path.join(ROOT, "sessions", "index.html")

SITE   = "https://haru-powerplatform.github.io/pa45/"
MAKE   = "https://make.powerautomate.com/"
GROUP  = "https://powerautomate-create.connpass.com/"
SURVEY = "https://forms.cloud.microsoft/r/mVzhNWH6JE"

EVENT = {1:386395,2:386742,3:387593,4:388691,5:389833,6:390451,7:391508,8:391996,
         9:392423,10:393267,11:393551,12:394484,13:395416,14:395861,15:397133,
         16:397828,17:398546,18:399388,24:403818}

VOL17_EXCEL = "https://github.com/Haru-PowerPlatform/pa45/raw/main/flows/vol-17/タスク一覧.xlsx"

def classify(hrefs):
    d = {"slide":None,"zip":None,"blog":None,"youtube":None}
    for h in hrefs:
        if "youtu" in h and not d["youtube"]: d["youtube"]=h
        elif ".zip" in h and "/flows/vol-" in h and not d["zip"]: d["zip"]=h
        elif "automate136.com" in h and not d["blog"]: d["blog"]=h
        elif ("/slides/vol-" in h or "/assets/pa45/" in h) and not d["slide"]: d["slide"]=h
    return d

CARD_CSS = ('*{box-sizing:border-box}body{margin:0;background:linear-gradient(160deg,#eaf2fc 0%,#f5f8fc 40%,#fff 100%);'
 'font-family:"Meiryo UI","Yu Gothic UI","Segoe UI",sans-serif;color:#1f2937;min-height:100vh;padding:28px 16px 60px}'
 '.wrap{max-width:820px;margin:0 auto}header{text-align:center;margin-bottom:8px}'
 '.eyebrow{display:inline-block;background:#2a7dd4;color:#fff;font-weight:700;font-size:13px;letter-spacing:.06em;padding:5px 16px;border-radius:20px}'
 'h1{font-size:28px;font-weight:800;color:#14528f;margin:14px 0 6px;line-height:1.3}'
 'h1 small{display:block;font-size:15px;color:#475569;font-weight:600;margin-top:6px}'
 '.meta{color:#475569;font-size:14px;margin-bottom:22px;text-align:center}'
 '.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:640px){.grid{grid-template-columns:1fr}}'
 '.card{display:flex;gap:14px;align-items:flex-start;text-decoration:none;color:inherit;background:#fff;border:1px solid #e2e8f0;'
 'border-radius:14px;padding:18px;box-shadow:0 2px 8px rgba(20,82,143,.06);transition:transform .12s,box-shadow .12s,border-color .12s}'
 '.card:hover{transform:translateY(-3px);box-shadow:0 10px 22px rgba(20,82,143,.16);border-color:#2a7dd4}'
 '.card .ico{flex:0 0 46px;width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;background:#eaf2fc}'
 '.card .body{flex:1;min-width:0}.card .t{font-size:16px;font-weight:800;color:#14528f;margin:0 0 3px;line-height:1.35}'
 '.card .d{font-size:13px;color:#475569;line-height:1.6;margin:0}'
 '.card .go{display:inline-block;margin-top:9px;font-size:12px;font-weight:700;color:#fff;background:#2a7dd4;padding:5px 14px;border-radius:16px}'
 '.card.primary{border:2px solid #f59e0b;background:#fffbeb}.card.primary .ico{background:#fef3c7}.card.primary .t{color:#92400e}.card.primary .go{background:#f59e0b}'
 '.tag{display:inline-block;font-size:11px;font-weight:700;color:#92400e;background:#fef3c7;border-radius:10px;padding:2px 9px;margin-left:6px;vertical-align:middle}'
 '.soon{opacity:.6}.soon .go{background:#94a3b8}'
 '.back{display:inline-block;margin-bottom:18px;color:#2a7dd4;text-decoration:none;font-size:13px;font-weight:700}'
 '.note{margin-top:22px;font-size:12.5px;color:#475569;text-align:center;line-height:1.8}'
 'footer{margin-top:28px;text-align:center;color:#94a3b8;font-size:12px}')

def card(ico, title, desc, href, go="開く →", primary=False, tag=""):
    cls = "card primary" if primary else "card"
    tagh = f' <span class="tag">{tag}</span>' if tag else ""
    return (f'    <a class="{cls}" href="{href}" target="_blank" rel="noopener">'
            f'<div class="ico">{ico}</div><div class="body">'
            f'<p class="t">{title}{tagh}</p><p class="d">{desc}</p>'
            f'<span class="go">{go}</span></div></a>')

def soon_card(ico, title, desc, tag="準備中"):
    return (f'    <span class="card soon"><div class="ico">{ico}</div><div class="body">'
            f'<p class="t">{title} <span class="tag">{tag}</span></p>'
            f'<p class="d">{desc}</p><span class="go">近日公開</span></div></span>')

def build_page(vol, title, date, links, upcoming=False):
    cards = []
    ev = EVENT.get(vol)
    if ev:
        cards.append(card("🎫","connpass イベントページ",
            "参加登録・当日入室（Teams会議リンク）。" if upcoming else "この回のイベント概要（アーカイブ）。",
            f"{GROUP}event/{ev}/"))
    if links.get("handson"):
        cards.append(card("🛠️","ハンズオン手順（当日これを見ながら作る）",
            "手順どおりに進めれば、👍で出欠が集まるフローが完成します。", links["handson"],
            go="手順を開く →", primary=True, tag="まずコレ"))
    if upcoming and vol==17:
        cards.append(card("📥","ハンズオンExcel素材",
            "タスク一覧.xlsx（テーブルTaskTable・サンプル5件）。クリックでDL。",
            VOL17_EXCEL, go="ダウンロード →", primary=True, tag="まずコレ"))
        cards.append(card("🤖","Power Automate を開く","make.powerautomate.com。一緒に作ります。", MAKE))
    if links.get("slide"):
        web = "/slides/vol-" in links["slide"]
        cards.append(card("📄","解説スライド" + ("（Web）" if web else "（PPTX）"),
            "全スライド。復習用に見返せます。", links["slide"],
            go=("開く →" if web else "ダウンロード →")))
    if links.get("zip"):
        cards.append(card("📦","完成フローZIP","作ったフローのソリューション。インポートして動かせます。",
            links["zip"], go="ダウンロード →"))
    if links.get("blog"):
        cards.append(card("📖","スライド解説ブログ","automate136.com の詳しい解説記事。", links["blog"]))
    if links.get("youtube"):
        cards.append(card("▶","YouTube動画","当日の録画。あとから見られます。", links["youtube"]))
    if upcoming:
        cards.append(card("📝","アンケート（Special Gift）","2分で完了。回答者に参加バッジ。", SURVEY, go="回答する →"))
    cards.append(card("🌐","参加者向けサイト（全回）","過去回のスライド・配布フローまとめ。", SITE))
    if upcoming:
        cards.append(card("📅","次回の開催をチェック","PA45グループの connpass。", GROUP))
        cards.append(soon_card("📦","完成フローZIP","今日作るフローのソリューションZIP。開催後に追加します。"))
    grid = "\n".join(cards)
    sub = html.escape(title)
    kind = "HANDS-ON" if upcoming else "ARCHIVE"
    return (f'<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'<title>PA45 第{vol}回 資料リンク集</title>\n<style>{CARD_CSS}</style>\n</head>\n<body>\n'
        f'<div class="wrap">\n  <a class="back" href="{SITE}sessions/">&#8592; PA45 資料アーカイブへ戻る</a>\n'
        f'  <header>\n    <span class="eyebrow">PA45 第{vol}回｜{kind}</span>\n'
        f'    <h1>第{vol}回 資料リンク集<small>{sub}</small></h1>\n  </header>\n'
        f'  <div class="meta">{date} ／ この回の資料リンクをまとめています</div>\n'
        f'  <div class="grid">\n{grid}\n  </div>\n'
        f'  <div class="note">※ リンクはログイン不要で開けます（配布ZIPを除く）。</div>\n'
        f'  <footer>Power Automate 45（PA45）／ 第{vol}回</footer>\n</div>\n</body>\n</html>\n')

def main():
    sess = open(SESS, encoding="utf-8").read()
    voldata={}
    blocks = re.findall(r'<!--\s*★第(\d+)回\s*-->(.*?)(?=<!--\s*★第\d+回\s*-->|</section>)', sess, re.S)
    for num, body in blocks:
        v=int(num)
        num_t=re.search(r'past-num">([^<]+)</', body)
        date_t=re.search(r'past-date">([^<·]+)', body)
        hrefs=re.findall(r'href="([^"]+)"', body)
        voldata[v]={"title":(num_t.group(1) if num_t else f"第{v}回"),
                    "date":(date_t.group(1).strip() if date_t else ""),
                    "links":classify(hrefs)}
    up=json.load(open(os.path.join(ROOT,"data","config","upcoming-event.json"),encoding="utf-8"))
    uv=int(up["vol"])
    up_links={}
    _vd=os.path.join(ROOT,"slides",f"vol-{uv:02d}")
    if os.path.exists(os.path.join(_vd,"handson.html")):
        up_links["handson"]=f"{SITE}slides/vol-{uv:02d}/handson.html"
    if os.path.exists(os.path.join(_vd,"index.html")):
        up_links["slide"]=f"{SITE}slides/vol-{uv:02d}/"
    voldata[uv]={"title":f"第{uv}回：{up['theme']}","date":up["date"],
                 "links":up_links,"upcoming":True}

    made=[]
    for v,dd in sorted(voldata.items()):
        outdir=os.path.join(ROOT,"slides",f"vol-{v:02d}")
        os.makedirs(outdir,exist_ok=True)
        target=os.path.join(outdir,"links.html")
        if v==17 and os.path.exists(target):
            made.append((v,"skip(既存)")); continue
        pg=build_page(v,dd["title"],dd["date"],dd["links"],dd.get("upcoming",False))
        open(target,"w",encoding="utf-8").write(pg)
        made.append((v,"生成"))
    for v,s in made: print(f"  第{v}回 links.html … {s}")

    # ボタン差し込み（past-card 単位）
    def inject(m):
        vol=int(m.group("vol")); block=m.group(0)
        if "資料リンク集" in block: return block
        url=f"{SITE}slides/vol-{vol:02d}/links.html"
        btn=(f'<a href="{url}" target="_blank" rel="noopener" class="btn-slide">'
             f'📎 資料リンク集（必要リンクまとめ）→</a>\n          ')
        return re.sub(r'(<a[^>]*class="btn-slide")', btn+r'\1', block, count=1)
    new = re.sub(r'<div class="past-card" data-vol="(?P<vol>\d+)">.*?\n      </div>', inject, sess, flags=re.S)
    if "slides/vol-17/links.html" not in new:
        nb=(f'\n  <a href="{SITE}slides/vol-17/links.html" target="_blank" rel="noopener" '
            f'class="btn-connpass" style="margin-top:8px;background:#14528f;">📎 資料リンク集（必要リンクまとめ）→</a>')
        new=new.replace('    connpassで参加登録する →\n  </a>', '    connpassで参加登録する →\n  </a>'+nb,1)
    if new!=sess:
        open(SESS,"w",encoding="utf-8").write(new)
    print(f"sessions/index.html: 資料リンク集 出現数 {new.count('資料リンク集')}")

if __name__=="__main__":
    main()

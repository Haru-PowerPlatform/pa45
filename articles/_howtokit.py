#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""手順記事の共通キット（2026-11-12 はる依頼）。

依頼の中身：
  ・最初の方と途中に、Microsoft のアイコンを使った構成図を入れる（横に大きくてよい）
  ・どこをクリックしてその画面にたどり着くかを、実画面のスクショで1手ずつ示す
  ・記事を見れば同じものが作れるところまで手順を書く
1本目＝articles/2026-11-cs-scheduled-notify（Post 2710）。

入っているもの：
  CSS / jp P H2 H3 UL term note warn why step link bubble   … 本文の部品
  Shots(here, src_dir, k)   … 実画面の加工（切り抜き・ぼかし・赤枠）。座標は「見えている大きさ」で書き、k で元画像へ換算
  Article(here, pid, slug)  … 画像のアップロード（sha でキャッシュ）と WP 本文の更新
        既存 Post は status・タイトル・スラッグ・カテゴリを変えない（content と excerpt だけ更新）。更新前の本文は backup/ に控える
実画面の撮影は articles/_shots/navlib.py（Edge を --remote-debugging-port=9333 で起動して Playwright でつなぐ）。
"""
import base64, hashlib, html, json, pathlib, re, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "articles"))
from _navkit import NAV_CSS, make_nav, make_bubble  # noqa: E402,F401
from _workcta import work_cta  # noqa: E402
import _shots  # noqa: E402

CSS = """<style>
.mb-body > p{margin:1.9em 0!important;line-height:2.05!important;}
.mb-body > h2{margin-top:2.8em!important;}
.mb-body > h3{margin-top:2.2em!important;}
.mb-body > ul{margin:1.7em 0!important;line-height:2.0;}
.mb-body > ul li{margin:.55em 0;}
.cs-preface{background:#eef7f1;border:1px solid #cfe8db;border-left:5px solid #5f8a6e;border-radius:10px;padding:14px 18px;margin:0 0 26px;font-size:.86em;color:#3d5647;line-height:1.85;}
.cs-preface a{color:#1d4ed8;font-weight:700;}
.mb-learn{background:#f7f5fc;border:1px solid #e4dcf7;border-left:5px solid #7c3aed;border-radius:12px;padding:16px 22px;margin:8px 0 32px;}
.mb-learn .lt{font-weight:800;color:#5b21b6;margin:0 0 6px;}
.mb-learn ol{margin:0;padding-left:1.4em;line-height:1.9;}
.mb-fig{margin:38px 0;display:flex;flex-direction:column;align-items:center;background:#e7e0f5;border:1px solid #d0c4ec;border-radius:16px;padding:12px 10px 12px;box-shadow:0 2px 8px rgba(76,29,149,.08);}
.mb-fig a{display:block;width:100%;}
.mb-fig img{width:100%;max-width:100%;height:auto;display:block;margin:0 auto;background:#fff;border-radius:10px;}
.mb-fig figcaption{font-size:.95em;color:#5b4a7a;margin-top:12px;line-height:1.8;}
@media(max-width:600px){.mb-fig{margin-left:-10px;margin-right:-10px;padding:6px 4px 10px;}}
.mb-shot{margin:40px 0;background:#eceef2;border:1px solid #d9dce3;border-radius:16px;padding:16px 16px 13px;box-shadow:0 3px 12px rgba(15,23,42,.09);display:flex;flex-direction:column;align-items:center;}
.mb-shot .sh-tag{align-self:flex-start;display:inline-flex;font-size:12.5px;font-weight:800;color:#475569;background:#dde1e9;border-radius:999px;padding:5px 14px;margin-bottom:12px;}
.mb-shot .sh-tag b{color:#7c3aed;margin-right:8px;}
.mb-shot img{max-width:100%;height:auto;display:block;border-radius:10px;border:1px solid #c7cad3;box-shadow:0 6px 18px rgba(15,23,42,.14);}
.mb-shot figcaption{font-size:1.02em;font-weight:500;color:#334155;margin-top:14px;line-height:1.8;align-self:flex-start;}
.mb-note{background:#fffdf5;border:2px solid #ffd54f;border-radius:12px;padding:18px 24px;margin:36px 0;line-height:2.1;}
.mb-note .nt-ttl{font-weight:700;color:#b26a00;margin:0 0 10px;}
.mb-warn{background:#fff6f6;border-left:6px solid #e57373;border-radius:8px;padding:18px 24px;margin:36px 0;line-height:2.1;}
.mb-warn .wt{font-weight:800;color:#c0392b;display:block;margin-bottom:8px;}
.mb-why{background:#f1f9f4;border:1px solid #cfe8db;border-left:6px solid #2f855a;border-radius:8px;padding:14px 22px;margin:26px 0;line-height:2.0;}
.mb-why .wy{font-weight:800;color:#276749;display:block;margin-bottom:4px;font-size:.92em;}
.mb-term{background:#f2f7fd;border:2px solid #b8d3ef;border-radius:12px;padding:14px 20px;margin:28px 0;line-height:1.9;font-size:.95em;}
.mb-term .tt{display:inline-block;font-weight:800;color:#14528f;background:#e1edfa;border-radius:999px;padding:2px 12px;font-size:.85em;margin-bottom:6px;}
.mb-step{background:#f7f4fd;border:2px solid #ddd0f2;border-radius:14px;padding:18px 22px 6px;margin:34px 0;}
.mb-step .st-ttl{display:flex;align-items:center;gap:12px;font-weight:800;color:#5b21b6;font-size:1.06em;margin-bottom:6px;}
.mb-step .st-no{flex:none;min-width:32px;height:32px;padding:0 8px;border-radius:999px;background:#7c3aed;color:#fff;display:flex;align-items:center;justify-content:center;}
.mb-step ol{margin:6px 0 14px;padding-left:0;list-style:none;counter-reset:s;}
.mb-step ol li{position:relative;padding:8px 0 8px 30px;line-height:1.8;border-top:1px solid #ece4f9;}
.mb-step ol li:first-child{border-top:none;}
.mb-step ol li::before{counter-increment:s;content:counter(s);position:absolute;left:0;top:11px;width:22px;height:22px;background:#ede9fe;color:#5b21b6;border-radius:50%;font-size:.78em;font-weight:800;display:flex;align-items:center;justify-content:center;}
.mb-tbl{width:100%;border-collapse:collapse;font-size:.93em;margin:24px 0;}
.mb-tbl th,.mb-tbl td{border:1px solid #e4dcf7;padding:9px 11px;vertical-align:top;text-align:left;line-height:1.7;}
.mb-tbl th{background:#f3eefc;color:#5b21b6;}
.mb-code{background:#1e1b2e;color:#f1eefc;border-radius:10px;padding:14px 18px;margin:20px 0;line-height:1.8;font-size:.95em;white-space:pre-wrap;}
.mb-link{background:#eef5ff;border:1px solid #cfe0f7;border-radius:12px;padding:16px 20px;margin:34px 0;line-height:1.9;}
.mb-link a{color:#1d4ed8;font-weight:700;}
.mb-disc{font-size:13px;color:#888;line-height:1.9;margin-top:36px;}
.speech-balloon{line-height:1.95;}
</style>"""
CSS = CSS.replace("</style>", NAV_CSS + "</style>")
CSS = re.sub(r"\s*\n\s*", "", CSS)   # WP が <style> 内の改行を <br> に変えるので1行にまとめる


def jp(t):
    return re.sub(r'。(?![」）】、\s<]|$)', '。<br>', t)


def P(t):
    return f"\n\n<p>{jp(t)}</p>"


def H2(t):
    return f"\n\n<h2>{t}</h2>"


def H3(t):
    return f"\n\n<h3>{t}</h3>"


def UL(items):
    return "\n\n<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def term(name, body):
    return f'\n\n<div class="mb-term"><span class="tt">用語</span><br><b>{name}</b>：{jp(body)}</div>'


def note(title, body):
    return f'\n\n<div class="mb-note"><p class="nt-ttl">※ {title}</p>{jp(body)}</div>'


def warn(title, body):
    return f'\n\n<div class="mb-warn"><span class="wt">{title}</span>{jp(body)}</div>'


def why(body):
    return f'\n\n<div class="mb-why"><span class="wy">なぜそうするか</span>{jp(body)}</div>'


def step(no, title, items):
    lis = "".join(f"<li>{i}</li>" for i in items)
    return (f'\n\n<div class="mb-step"><div class="st-ttl"><span class="st-no">{no}</span>{title}</div>'
            f'<ol>{lis}</ol></div>')


def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'\n\n<table class="mb-tbl"><tr>{h}</tr>{b}</table>'


def link(body):
    return f'\n\n<div class="mb-link">{body}</div>'


bubble = make_bubble(jp)


# ---------------------------------------------------------------- 実画面の加工
class Shots:
    """raw（撮ったままの画面）→ 記事用（切り抜き・ぼかし・赤枠）。

    座標は Read で画像を見たときの大きさで書き、k（元画像の幅 ÷ 見えている幅）で元画像の px に直す。
    赤枠は _shots.snap_box で文字にかからない位置へ寄せ、寄せられない枠は problems に残す（--push を止める）。
    """
    MAXW = 1600

    def __init__(self, here, src_dir, k=1.0, common_mask=()):
        self.here = pathlib.Path(here)
        self.src = pathlib.Path(src_dir)
        self.k = k
        self.common_mask = list(common_mask)
        self.out = self.here / "assets"
        self.out.mkdir(exist_ok=True)
        self.items = {}
        self.problems = []

    def _s(self, b):
        return [round(v * self.k) for v in b]

    def make(self, name, src, crop=None, mask=(), boxes=(), ack=False):
        from PIL import Image
        im = Image.open(self.src / f"{src}.png").convert("RGB")
        for m in list(mask) + self.common_mask:
            x0, y0, x1, y1 = self._s(m)
            reg = im.crop((x0, y0, x1, y1))
            w, h = reg.size
            reg = reg.resize((max(1, w // 12), max(1, h // 12)), Image.BILINEAR).resize((w, h), Image.NEAREST)
            im.paste(reg, (x0, y0))
        fixed = []
        for b in boxes:
            sb = self._s(b)
            if ack:
                fixed.append(sb)
                continue
            nb, bad = _shots.snap_box(im, sb, 1.0)
            if bad:
                self.problems.append(f"{name} {list(b)}: 辺 {','.join(bad)} が文字にかかる")
            fixed.append(nb)
        ox = oy = 0
        if crop:
            c = self._s(crop)
            c = [max(0, c[0]), max(0, c[1]), min(im.width, c[2]), min(im.height, c[3])]
            ox, oy = c[0], c[1]
            im = im.crop(tuple(c))
        im = im.convert("RGBA")
        sc = min(1.0, self.MAXW / im.width)
        if sc < 1.0:
            im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
        for (x0, y0, x1, y1) in fixed:
            _shots._rounded_outline(im, [round((x0 - ox) * sc), round((y0 - oy) * sc),
                                         round((x1 - ox) * sc), round((y1 - oy) * sc)])
        out = self.out / f"shot-{name}.png"
        im.convert("RGB").save(out, optimize=True)
        self.items[name] = im.size
        return out


# ---------------------------------------------------------------- WordPress
def _env():
    d = {}
    for l in open(ROOT / ".env", encoding="utf8"):
        l = l.strip()
        if "=" in l and not l.startswith("#"):
            k, v = l.split("=", 1)
            d[k.strip()] = v.strip().strip('"').strip("'")
    return d


def _req(method, path, data=None, raw=None, headers=None):
    e = _env()
    h = {"Authorization": "Basic " + base64.b64encode(f"{e['WP_USER']}:{e['WP_PASS']}".encode()).decode(),
         "User-Agent": "Mozilla/5.0"}
    if raw is None:
        h["Content-Type"] = "application/json"
        body = json.dumps(data).encode() if data is not None else None
    else:
        body = raw
    h.update(headers or {})
    r = urllib.request.Request(e["WP_URL"].rstrip("/") + path, method=method, headers=h, data=body)
    return json.load(urllib.request.urlopen(r, timeout=180))


class Article:
    def __init__(self, here, pid, prefix, state_name="post_state.json"):
        self.here = pathlib.Path(here)
        self.pid = pid
        self.prefix = prefix
        self.state_f = self.here / state_name
        self.state = json.loads(self.state_f.read_text(encoding="utf8")) if self.state_f.exists() else {"post_id": pid, "media": {}}
        self.push = "--push" in sys.argv
        self.sizes = {}

    def _save(self):
        self.state_f.write_text(json.dumps(self.state, ensure_ascii=False, indent=1), encoding="utf8")

    def url(self, name):
        """assets/{name}.png の URL。--push のときだけアップロードし、ふだんはローカルの相対パスを返す。"""
        f = self.here / "assets" / f"{name}.png"
        sha = hashlib.sha1(f.read_bytes()).hexdigest()
        from PIL import Image
        self.sizes[name] = Image.open(f).size
        rec = self.state["media"].get(name)
        if rec and rec["sha"] == sha:
            return rec["url"]
        if not self.push:
            return f"assets/{name}.png"
        j = _req("POST", "/wp-json/wp/v2/media", raw=f.read_bytes(),
                 headers={"Content-Type": "image/png",
                          "Content-Disposition": f'attachment; filename="{self.prefix}-{name}.png"'})
        self.state["media"][name] = {"id": j["id"], "url": j["source_url"], "sha": sha}
        self._save()
        return j["source_url"]

    def shot(self, name, cap, alt=None, tag=""):
        """実画面。tag に「手順 2-1」のような番号を入れると、本文の手順と画像の対応が見える。"""
        u = self.url(f"shot-{name}")
        w, h = self.sizes[f"shot-{name}"]
        a = html.escape(alt or re.sub(r"<[^>]+>|▲\s*", "", cap)[:90], quote=True)
        t = f"<b>{tag}</b>" if tag else ""
        return (f'\n\n<figure class="mb-shot"><span class="sh-tag">{t}実際の画面（押すと拡大）</span>'
                f'<a href="{u}" target="_blank" rel="noopener"><img src="{u}" alt="{a}" width="{w}" height="{h}" loading="lazy" /></a>'
                f'<figcaption>{cap}</figcaption></figure>')

    def fig(self, name, alt, cap, wide=True):
        u = self.url(f"fig-{name}")
        w, h = self.sizes[f"fig-{name}"]
        return (f'\n\n<figure class="mb-fig{" wide" if wide else ""}"><a href="{u}" target="_blank" rel="noopener">'
                f'<img src="{u}" alt="{html.escape(alt, quote=True)}" width="{w}" height="{h}" /></a>'
                f'<figcaption>{cap}。図を押すと大きく表示される</figcaption></figure>')

    def cta(self):
        return "\n\n" + work_cta(str(self.pid))

    def finish(self, body_html, excerpt=None, tail=""):
        """article.html を書き、--push なら WP の本文だけを更新する（status などは触らない）。"""
        out = CSS + "\n" + body_html + tail
        (self.here / "article.html").write_text(out, encoding="utf8")
        print("article.html", len(out), "chars | img", out.count("<img"), "| shot", out.count('class="mb-shot"'))
        if not self.push:
            return
        cur = _req("GET", f"/wp-json/wp/v2/posts/{self.pid}?context=edit")
        bk = self.here / "backup"
        bk.mkdir(exist_ok=True)
        (bk / f"{self.pid}-{time.strftime('%Y%m%d-%H%M%S')}.html").write_text(cur["content"]["raw"], encoding="utf8")
        payload = {"content": out}
        if excerpt:
            payload["excerpt"] = excerpt
        _req("POST", f"/wp-json/wp/v2/posts/{self.pid}", payload)
        j = _req("GET", f"/wp-json/wp/v2/posts/{self.pid}?context=edit")
        c, r = j["content"]["raw"], j["content"]["rendered"]
        st = "".join(re.findall(r"<style.*?</style>", r, flags=re.S))
        print("UPDATED", self.pid, "status:", j["status"], "(was", cur["status"] + ")", "| slug:", j["slug"],
              "| img:", c.count("<img"), "| empty <p>:", len(re.findall(r"<p>\s*</p>", r)),
              "| style broken:", ("<br" in st or "<p" in st), "| excerpt:", bool(j["excerpt"]["raw"]))

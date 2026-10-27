# -*- coding: utf-8 -*-
"""Vol.145〜154（2026-10-27 作り直し）のスライド生成部品。
1枚目＝コンセプト（回ごとに手書きの stage）／2枚目＝作り方（列の定義から生成）／
3枚目＝実際のフロー全体（キャンバスの実画面＋番号）／4枚目＝要の設定画面（実画面を切り出し、赤枠と注記）。
実画面の元は pa45/assets/x/html/_shots/<vol>/（PIIはモザイク済み）。"""
import os
from PIL import Image

HTML = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(HTML, "_shots")
A = "../../pptx/_assets/"
ICON = {
    "outlook": A + "icons/pa_outlook.png", "teams": A + "icons/pa_teams.png", "sp": A + "icons/pa_sharepoint.png",
    "od": A + "icons/pa_onedrive.png", "rec": A + "icons/pa_schedule.png", "data": A + "icons/pa_dataoperation.png",
    "ctrl": A + "icons/pa_control.png", "cond": A + "icons/pa_condition.png", "pa": A + "icons/pa_logo.png",
    "forms": A + "icons/ms/forms.svg", "excel": A + "icons/ms/excel.svg", "copilot": A + "icons/ms/copilot.png",
    "lists": A + "icons/ms/lists.svg", "weather": "../_base/msn-weather.svg", "var": "../_base/var.svg",
}
SVGW = lambda p, sw=2.4: f'<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'
P_WARN = '<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>'
P_BULB = '<path d="M9 18h6M10 22h4M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"/>'
P_ARROW = '<path d="M5 12h14M13 6l6 6-6 6"/>'
P_CAM = '<path d="M3 8a2 2 0 0 1 2-2h2l2-2h6l2 2h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="13" r="4"/>'


def page(folder, vol_label, doc_title, title_html, chara, concl, stage, bottom, style="", src="出典：Microsoft Learn"):
    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1280, initial-scale=1">
<title>X技術Tips {vol_label} {doc_title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&family=Roboto+Mono:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../_base/tips-base.css">
<link rel="stylesheet" href="../_base/x145.css">
<style>
{style}
</style>
</head>
<body>
<div id="slide">
  <div class="titlebar">
    <div class="vol-pill">{vol_label}</div>
    <img class="vol-logo" src="{A}icons/pa_logo.png" alt="">
    <div class="title-text">{title_html}</div>
    <img class="title-chara" src="{A}chara/chara_{chara}.png" alt="">
  </div>
  <div class="concl">
    <div class="chip">{SVGW(P_BULB, 2.2)}</div>
    <div class="txt">{concl}</div>
  </div>
  <div class="stage">
{stage}
  </div>
{bottom}
  <div class="src">{src}</div>
</div>
</body>
</html>
'''
    d = os.path.join(HTML, folder)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


def next_bar(text):
    return f'  <div class="next"><span class="na">{SVGW(P_ARROW, 2.6)}</span><span>{text}</span></div>'


def warn_bar(items):
    sp = "".join(f"<span>{t}</span>" for t in items)
    return f'  <div class="warnbar"><span class="na">{SVGW(P_WARN)}</span><span class="ws">{sp}</span></div>'


def uses_bar(label, items):
    sp = "".join(f'<span class="u">{t}</span>' for t in items)
    return f'  <div class="next" style="padding:7px 16px"><span class="uses"><span class="ul">{label}</span>{sp}</span></div>'


# ── 2枚目：作り方 ───────────────────────────────────
def howto_cols(cols):
    """cols=[{t:見出し, acts:[(icon, アクション名, [(k, v, hot)], why)], cap:補足}]"""
    out = []
    for i, c in enumerate(cols, 1):
        rows = []
        for icon, name, fields, why in c["acts"]:
            rows.append(f'<div class="act"><img src="{ICON[icon]}" alt="">{name}</div>')
            for k, v, hot in fields:
                rows.append(f'<span class="fi{" hot" if hot else ""}"><span class="k">{k}</span>{v}</span>')
            if why:
                rows.append(f'<div class="why">{why}</div>')
        if c.get("ex"):
            rows.append(f'<div class="ex"><div class="exh">結果の例</div><div class="exb">{c["ex"]}</div></div>')
        out.append(f'''    <div class="col info">
      <div class="ch2"><span class="n">{i}</span>{c["t"]}</div>
      <div class="body"><div class="card"><div class="cardb">{"".join(rows)}</div></div></div>
      <div class="cap">{c["cap"]}</div>
    </div>''')
    return "\n".join(out)


# ── 実画面の切り出し ─────────────────────────────────
def compose(vol, name, segs, frames, out_folder, out_name):
    """segs=[(y0,y1)] を縦に連結。frames=[(x0,y0,x1,y1,label)]（元画像の座標）→ 連結後の座標に直して返す"""
    im = Image.open(os.path.join(SHOTS, str(vol), name + ".png")).convert("RGB")
    w = im.width
    parts, offs, y = [], [], 0
    for y0, y1 in segs:
        y1 = min(y1, im.height)
        parts.append(im.crop((0, y0, w, y1)))
        offs.append((y0, y1, y))
        y += (y1 - y0) + (6 if len(segs) > 1 else 0)
    H = y - (6 if len(segs) > 1 else 0)
    out = Image.new("RGB", (w, H), (226, 232, 240))
    for p, (y0, y1, oy) in zip(parts, offs):
        out.paste(p, (0, oy))
    d = os.path.join(HTML, out_folder)
    os.makedirs(d, exist_ok=True)
    out.save(os.path.join(d, out_name + ".png"))
    nf = []
    for x0, fy0, x1, fy1, lb in frames:
        for y0, y1, oy in offs:
            if y0 <= fy0 < y1:
                nf.append((x0, fy0 - y0 + oy, x1, min(fy1, y1) - y0 + oy, lb))
                break
    return out_name + ".png", w, H, nf


def shot_html(title, icon, src, w, h, frames, box_w, box_h, badge_x=None, badges=None):
    s = min(box_w / w, box_h / h)
    dw, dh = round(w * s), round(h * s)
    fr = "".join(
        f'<div class="fr" style="left:{x0*s-4:.0f}px;top:{y0*s-4:.0f}px;width:{(x1-x0)*s+8:.0f}px;height:{(y1-y0)*s+8:.0f}px"><span class="tg">{lb}</span></div>'
        for x0, y0, x1, y1, lb in (frames or []))
    bd = "".join(
        f'<span class="bd" style="left:{badge_x*s-15:.0f}px;top:{by*s-15:.0f}px">{i}</span>'
        for i, by in enumerate(badges or [], 1))
    ic = f'<img src="{ICON[icon]}" alt="">' if icon else ""
    return (f'<div class="shot"><div class="sh">{ic}{title}<span class="real">実画面</span></div>'
            f'<div class="imgw"><div class="in" style="width:{dw}px;height:{dh}px">'
            f'<img class="ss" src="{src}" style="width:{dw}px;height:{dh}px" alt="">{fr}{bd}</div></div></div>')


# ── 3枚目：フロー全体 ────────────────────────────────
def flow_stage(vol, folder, canvas_badges, badge_x, steps, flow_title, box_w=330, box_h=418):
    """steps=[(icon, アクション名, 説明, hot)]。canvas_badges の数だけ番号を振る"""
    src, w, h, _ = compose(vol, "canvas", [(0, 10000)], [], folder, "canvas")
    left = shot_html(flow_title, "pa", src, w, h, [], box_w, box_h, badge_x, canvas_badges)
    items = []
    n = 0
    for icon, name, desc, hot in steps:
        if icon == "bulb":
            badge = f'<span class="ib" style="color:#D97706">{SVGW(P_BULB, 2.2)}</span>'
        else:
            n += 1
            badge = f'<span class="bd">{n}</span><span class="ib"><img src="{ICON[icon]}" alt=""></span>'
        items.append(f'<div class="sti{" hot" if hot else ""}">{badge}<div class="tx"><div class="an">{name}</div><div class="ds">{desc}</div></div></div>')
    return f'    <div style="flex:0 0 auto;display:flex">{left}</div>\n    <div class="steps">{"".join(items)}</div>'


# ── 4枚目：要の設定画面 ──────────────────────────────
def settings_stage(vol, folder, shots, layout="side", box_h=400, col_w=None):
    """shots=[{name, segs, frames, title, icon, notes:[(label, html)]}]"""
    cols = []
    n = len(shots)
    for i, sp in enumerate(shots):
        src, w, h, nf = compose(vol, sp["name"], sp["segs"], sp["frames"], folder, f"s{i+1}")
        if layout == "side":
            bw = col_w or (1248 - 11 * (n - 1)) / n - 24
        else:
            bw = col_w or 700
        sh = shot_html(sp["title"], sp.get("icon"), src, w, h, nf, bw, sp.get("box_h", box_h))
        notes = "".join(f'<div class="note"><span class="bd">{lb}</span><div class="nt">{t}</div></div>' for lb, t in sp["notes"])
        cols.append(f'<div class="shotcol">{sh}<div class="notes">{notes}</div></div>')
    if layout == "side":
        return "\n".join("    " + c for c in cols)
    return "    " + "".join(cols)

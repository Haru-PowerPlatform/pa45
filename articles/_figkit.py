#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""記事の図（横長1660px・Microsoft の製品アイコン入り）の共通部品。1本目の figs.py（Post 2710）から切り出した。
  ms(name)          … アイコンの data URI（assets-icons/ms と、記事フォルダの assets/ms）
  doc(body, extra)  … 1枚ぶんの HTML
  route(...)        … 「画面のたどり方」の図（押す場所を左から右へ）
  render(html, out) … PNG に書き出す
"""
import base64, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _archkit import render_html, icon  # noqa: E402

AC = "#7c3aed"
W = 1660
MS_LOCAL = [HERE / "2026-11-cs-case-hr-rules-help" / "assets" / "ms", HERE / "2026-11-cs-scheduled-notify" / "assets"]


def ms(name):
    for d in MS_LOCAL:
        for f in (d / f"{name}.png", d / f"ic-{name}.png"):
            if f.exists():
                return "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode()
    return icon(name)


BASE = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;background:#fff;font-family:'Noto Sans JP','Yu Gothic UI','Meiryo',sans-serif;color:#1f2937}}
.wrap{{margin:8px;padding:30px 34px 30px;border:3px solid {AC}33;border-radius:26px;background:linear-gradient(180deg,#fff,#faf8ff)}}
h1{{font-size:36px;font-weight:800;color:{AC};display:flex;align-items:center;gap:14px;line-height:1.35;margin-bottom:6px}}
h1:before{{content:"";flex:none;width:10px;height:40px;border-radius:5px;background:{AC}}}
.lead{{font-size:25px;color:#475569;margin:0 0 22px 24px;line-height:1.6}}
.band{{border:3px solid {AC};border-radius:24px;background:#fff;padding:20px 22px 24px;position:relative}}
.bandt{{display:inline-flex;align-items:center;gap:12px;font-size:27px;font-weight:800;color:#fff;background:{AC};border-radius:999px;padding:6px 24px 6px 10px;margin-bottom:18px}}
.bandt img{{width:46px;height:46px;background:#fff;border-radius:50%;padding:4px}}
.row{{display:flex;align-items:stretch;justify-content:space-between}}
.nd{{flex:1;min-width:0;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:16px 14px 18px;text-align:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.nd.hl{{border-color:{AC}}}
.num{{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:50%;background:{AC};color:#fff;font-size:27px;font-weight:800;margin-bottom:8px}}
.nd img.ic{{width:84px;height:84px;display:block;margin:0 auto 8px}}
.nm{{font-size:27px;font-weight:800;line-height:1.35}}
.ac{{white-space:nowrap;font-size:21px;color:#334155;line-height:1.5;margin-top:8px;background:#f1f5f9;border-radius:12px;padding:8px 8px}}
.tx{{white-space:nowrap;font-size:23px;color:#475569;line-height:1.55;margin-top:8px}}
.ar{{flex:none;width:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 4px}}
.ar .lb{{white-space:nowrap;font-size:21px;font-weight:800;color:{AC};text-align:center;line-height:1.35;margin-bottom:6px;min-height:58px;display:flex;align-items:flex-end}}
.ar svg{{width:100%;height:26px;display:block}}
.ar line{{stroke:{AC};stroke-width:5}}
.ar polygon{{fill:{AC}}}
.below{{display:flex;justify-content:space-between;margin-top:0}}
.bl{{flex:1;display:flex;flex-direction:column;align-items:center}}
.gap{{flex:none;width:150px}}
.stem{{width:4px;height:30px;background:repeating-linear-gradient(180deg,#94a3b8 0 6px,transparent 6px 11px)}}
.att{{display:flex;align-items:center;gap:12px;background:#f8fafc;border:2.5px dashed #cbd5e1;border-radius:18px;padding:12px 14px;width:100%;text-align:left}}
.att img{{flex:none;width:56px;height:56px}}
.att b{{white-space:nowrap;display:block;font-size:22px;line-height:1.35}}
.att span{{white-space:nowrap;display:block;font-size:19px;color:#64748b;line-height:1.45}}
.notes{{margin-top:22px;padding:16px 20px;background:#f1f5f9;border-radius:18px;display:flex;flex-wrap:wrap;align-items:center;gap:12px}}
.notes b{{font-size:24px;color:#0f172a;margin-right:6px}}
.chip{{display:inline-flex;align-items:center;gap:10px;background:#fff;border:1.5px solid #cbd5e1;border-radius:999px;padding:6px 18px 6px 10px;font-size:23px;font-weight:700}}
.chip img{{width:38px;height:38px}}
.chip.t{{padding-left:18px}}
"""
ARROW = '<svg viewBox="0 0 100 26" preserveAspectRatio="none"><line x1="0" y1="13" x2="84" y2="13"/><polygon points="80,2 100,13 80,24"/></svg>'


def doc(body, extra=""):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE}{extra}</style></head><body><div class="wrap">{body}</div></body></html>'


ROUTE_CSS = f"""
.rt{{display:flex;align-items:stretch}}
.st{{flex:1;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:16px 12px 16px;text-align:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.st .where{{font-size:21px;font-weight:800;color:#475569;background:#e2e8f0;border-radius:999px;display:inline-block;padding:3px 14px;margin-bottom:10px}}
.st .do{{font-size:26px;font-weight:800;line-height:1.4}}
.st .do em{{font-style:normal;color:{AC}}}
.st .res{{font-size:22px;color:#475569;line-height:1.5;margin-top:10px}}
.ar2{{flex:none;width:54px;display:flex;align-items:center;justify-content:center}}
.ar2 svg{{width:44px;height:26px}}
.ar2 line{{stroke:{AC};stroke-width:5}}
.ar2 polygon{{fill:{AC}}}
.sec{{display:flex;margin-top:14px}}
.sec div{{flex:1;text-align:center;font-size:22px;font-weight:800;color:{AC}}}
.sec .sp{{flex:none;width:54px}}
"""
A2 = '<div class="ar2"><svg viewBox="0 0 44 26"><line x1="0" y1="13" x2="30" y2="13"/><polygon points="26,2 44,13 26,24"/></svg></div>'


def route(title, lead, steps, secs, product="copilotstudio"):
    """steps=[(どの画面, 押すもの（<em>で強調）, 押した結果)]、secs=[各ステップの下に出す節の番号]"""
    b = (f'<h1><img src="{ms(product)}" style="width:52px;height:52px">{title}</h1>'
         f'<div class="lead">{lead}</div><div class="rt">')
    for i, (w, d, r) in enumerate(steps):
        b += f'<div class="st"><div class="where">{w}</div><div class="do">{d}</div><div class="res">{r}</div></div>'
        if i < len(steps) - 1:
            b += A2
    b += '</div><div class="sec">' + '<div class="sp"></div>'.join(f"<div>{x}</div>" for x in secs) + '</div>'
    return doc(b, ROUTE_CSS)


def render(html, out, height=900):
    return render_html(html, out, width=W, height=height)

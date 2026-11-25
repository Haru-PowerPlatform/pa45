#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AB-730 勉強法の記事で使う実画面。

元画像＝talks/ab730-prep/0N/shots/real/（2026-10-27〜29 に AB-730 合格対策シリーズの資料づくりで撮ったもの。
テナント plug136・チャット履歴・名前・アバターは撮影時に加工済み、赤枠もそのとき付けたもの）。
ここでは切り抜きと縮小だけをする。

  python shots.py
"""
import pathlib, sys
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _howtokit import Shots  # noqa: E402

SRC = pathlib.Path(r"C:\Users\isamu\Documents\talks\ab730-prep")
S = Shots(HERE, SRC)

# 名前 ← 元画像（0N/shots/real/xxx）、crop は元画像の px
ITEMS = [
    ("exam", "01/shots/real/learn-exam", [0, 110, 1920, 1080]),
    ("guide", "01/shots/real/guide-d1", [0, 108, 1920, 1270]),
    ("model", "03/shots/real/copilot-model", None),
    ("edp", "01/shots/real/copilot-edp", None),
    ("answer", "02/shots/real/answer", None),
    ("sources", "02/shots/real/sources", None),
    ("save", "03/shots/real/save", None),
    ("saved", "03/shots/real/saved-prompts-c", None),
    ("schedule", "03/shots/real/schedule", None),
    ("answer-menu", "05/shots/real/answer-menu-crop", None),
    ("nb-new", "03/shots/real/nb-new", None),
    ("nb-add", "03/shots/real/nb-add", None),
    ("word", "04/shots/real/word-draft", None),
    ("excel", "04/shots/real/excel-answer", None),
    ("agents", "06/shots/real/copilot-agents", None),
    ("researcher", "06/shots/real/researcher", None),
]


def workiq():
    """Work IQ のオフとオンで、入力欄の上の候補がどう変わるかを1枚に並べる。"""
    r = SRC / "01/shots/real"
    rows = [("Work IQ オフ", "workiq-off-btn", "workiq-off-chips"), ("Work IQ オン", "workiq-on-btn", "workiq-on-chips")]
    f = ImageFont.truetype(r"C:\Windows\Fonts\meiryob.ttc", 34)
    W, H = 1960, 2 * 200 + 40
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    y = 20
    for lb, b, c in rows:
        d.rounded_rectangle([20, y, W - 20, y + 180], 18, fill="#f8fafc", outline="#e2e8f0", width=3)
        d.text((50, y + 68), lb, font=f, fill="#334155")
        bi = Image.open(r / f"{b}.png").convert("RGB")
        bi = bi.crop((0, 0, 360, 110))
        im.paste(bi, (290, y + 35))
        ci = Image.open(r / f"{c}.png").convert("RGB")
        ci = ci.crop((0, 20, 1140, 150))
        ci = ci.resize((round(ci.width * 0.95), round(ci.height * 0.95)))
        im.paste(ci, (700, y + 28))
        y += 200
    out = HERE / "assets" / "shot-workiq.png"
    im.save(out, optimize=True)
    S.items["workiq"] = im.size
    return out


if __name__ == "__main__":
    for name, src, crop in ITEMS:
        print(S.make(name, src, crop=crop))
    print(workiq())
    # 元が小さい画面は、記事の幅いっぱいに広がると文字だけ大きく見えるので縮める
    for n, w in (("sources", 560), ("answer-menu", 460), ("model", 760), ("edp", 1000)):
        f = HERE / "assets" / f"shot-{n}.png"
        im = Image.open(f)
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            im.save(f, optimize=True)
            S.items[n] = im.size
    for k, v in S.items.items():
        print(k, v)

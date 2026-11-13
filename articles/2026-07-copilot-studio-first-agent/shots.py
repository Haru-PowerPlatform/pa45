#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2583 の実画面（2026-11-13 に今の日本語表示の画面で撮り直し）。
元画像＝articles/_shots/raw-2583/*.png（2838x1552）。座標は幅2576で見たときの値。
  python shots.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _howtokit import Shots  # noqa: E402


def build():
    s = Shots(HERE, HERE.parent / "_shots" / "raw-2583", k=2838 / 2576)
    m = s.make
    m("home", "01-home", crop=(0, 0, 2576, 1150), boxes=[(16, 232, 446, 304)])
    m("list", "02-agents-list", crop=(0, 0, 2576, 640),
      mask=[(1490, 462, 1700, 640), (1820, 462, 2040, 640)],
      boxes=[(2104, 262, 2512, 340)])
    m("options", "03-create-options", crop=(1100, 180, 2576, 1060),
      mask=[(1500, 470, 1652, 1060)], boxes=[(1676, 448, 2482, 604)])
    m("new", "04-new-agent", boxes=[(366, 220, 1768, 310), (144, 490, 1768, 946), (1830, 132, 2554, 1114)], ack=True)
    m("instructions", "06-instructions", crop=(120, 0, 2576, 900),
      boxes=[(358, 212, 1150, 302), (138, 486, 1790, 666)], ack=True)
    m("saved", "08-saved", crop=(120, 0, 2576, 420), boxes=[(2096, 90, 2156, 148)])
    m("preview", "09-preview-nocredit", crop=(120, 70, 2576, 1380), mask=[(1205, 502, 2045, 548), (640, 552, 815, 596)],
      boxes=[(1116, 90, 1310, 148), (666, 1150, 2028, 1254)])
    for k, v in s.items.items():
        print("shot", k, v)
    if s.problems:
        print("!! 赤枠を直す:\n  " + "\n  ".join(s.problems))
    return s


if __name__ == "__main__":
    build()

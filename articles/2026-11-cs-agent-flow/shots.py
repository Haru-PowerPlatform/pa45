#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2675 の実画面（2026-11-13 に今の日本語表示の画面で撮り直し）。
元画像＝articles/_shots/raw-2675/*.png（2838x1552）。座標は幅2576で見たときの値。
  python shots.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _howtokit import Shots  # noqa: E402

AV = (26, 1262, 90, 1328)
MAIL = (1898, 446, 2148, 486)
PANEL = (1810, 155, 2545, 1380)


def build():
    s = Shots(HERE, HERE.parent / "_shots" / "raw-2675", k=2838 / 2576)
    m = s.make
    m("list", "01-workflows-list", crop=(0, 0, 2576, 640),
      mask=[(1630, 462, 1900, 640), (1960, 462, 2200, 640), AV], boxes=[(2114, 258, 2512, 348)], ack=True)
    m("trigger-types", "02-trigger-types", crop=(1810, 155, 2545, 930), boxes=[(1860, 806, 2494, 892)], ack=True)
    m("trigger", "03-agent-trigger", crop=(600, 140, 2576, 900))
    m("input-types", "04-input-types", crop=(1810, 155, 2545, 1260))
    m("input", "06-input-filled", crop=(1810, 155, 2545, 1150), boxes=[(1850, 572, 2512, 644)], ack=True)
    m("search", "07-search-add-row", crop=(560, 110, 2016, 900), boxes=[(598, 428, 1272, 538)], ack=True)
    m("picker", "10-question-picker", crop=(1810, 155, 2545, 1100), boxes=[(1912, 516, 2502, 600)], ack=True)
    m("expr", "12-expression-mode", crop=(1810, 155, 2545, 1100), boxes=[(1930, 782, 2510, 854)], ack=True)
    m("row", "13-row-done", crop=PANEL, boxes=[(1870, 862, 2464, 930), (1870, 998, 2464, 1064)], ack=True)
    m("canvas", "14-canvas", crop=(640, 660, 2300, 850))
    m("respond", "15-respond-panel", crop=(1810, 155, 2545, 820), boxes=[(1850, 414, 2512, 532)], ack=True)
    m("name-error", "16a-name-error", crop=(120, 0, 1500, 130))
    m("publish-error", "18-publish-error-details", crop=(700, 520, 1880, 890))
    m("tab", "19-tool-workflow-tab", crop=(598, 105, 1978, 1300),
      boxes=[(1286, 536, 1914, 646), (636, 666, 1264, 776)], ack=True)
    m("tooldesc", "23-workflow-tool-desc", crop=(345, 70, 2232, 740), boxes=[(418, 450, 2160, 596)], ack=True)
    m("agent", "24-agent-with-workflow", crop=(120, 0, 2576, 1320), boxes=[(1846, 494, 2546, 700)], ack=True)
    for k, v in s.items.items():
        print("shot", k, v)
    return s


if __name__ == "__main__":
    build()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2594 の実画面（2026-11-13 に今の日本語表示の画面で撮り直し）。
元画像＝articles/_shots/raw-2594/*.png（2838x1552）。座標は幅2576で見たときの値。
  python shots.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _howtokit import Shots  # noqa: E402

DLG = (540, 100, 2040, 1310)


def build():
    s = Shots(HERE, HERE.parent / "_shots" / "raw-2594", k=2838 / 2576)
    m = s.make
    m("list", "01-agents-list", crop=(0, 0, 2576, 640),
      mask=[(1490, 462, 1700, 640), (1820, 462, 2040, 640)], boxes=[(190, 448, 1470, 530)], ack=True)
    m("open", "02-agent-open", crop=(120, 0, 2576, 1150), boxes=[(1846, 686, 2544, 842)], ack=True)
    m("dialog", "03-add-knowledge-dialog", crop=DLG, boxes=[(606, 376, 1958, 692)], ack=True)
    m("file", "04-file-added", crop=DLG, boxes=[(628, 800, 1938, 890)], ack=True)
    m("namedesc", "05-name-desc", crop=DLG, boxes=[(1086, 800, 1938, 890), (1452, 1212, 1782, 1274)], ack=True)
    m("added", "06-added", crop=(120, 0, 2576, 1250), boxes=[(1850, 846, 2224, 914)], ack=True)
    m("processing", "07-knowledge-detail", crop=(470, 140, 2110, 1270), boxes=[(1904, 344, 2068, 398)], ack=True)
    m("ready", "08-knowledge-ready", crop=(470, 140, 2110, 1270), boxes=[(1870, 342, 2074, 400), (526, 482, 2074, 604)], ack=True)
    for k, v in s.items.items():
        print("shot", k, v)
    return s


if __name__ == "__main__":
    build()

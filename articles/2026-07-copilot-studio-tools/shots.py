#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2652 の実画面（2026-11-13 に今の日本語表示の画面で撮り直し）。
元画像＝articles/_shots/raw-2652/*.png（2838x1552）。座標は幅2576で見たときの値。
  python shots.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _howtokit import Shots  # noqa: E402


def build():
    s = Shots(HERE, HERE.parent / "_shots" / "raw-2652", k=2838 / 2576)
    m = s.make
    m("open", "01b-agent-open", crop=(120, 0, 2576, 1250), boxes=[(1846, 494, 2544, 652)], ack=True)
    m("dialog", "02-add-tool-dialog", crop=(580, 90, 1985, 1310), boxes=[(632, 600, 1260, 712)], ack=True)
    m("actions", "03-outlook-actions", crop=(598, 105, 1978, 1300), boxes=[(1286, 1116, 1912, 1228)], ack=True)
    m("detail", "04-send-email-detail", crop=(575, 90, 1975, 700), boxes=[(1732, 250, 1922, 318)], ack=True)
    m("added", "05-after-add", crop=(120, 0, 2576, 1320), boxes=[(1846, 572, 2168, 642)], ack=True)
    m("tool", "06-tool-detail", crop=(345, 70, 2232, 1340), mask=[(1518, 304, 1764, 350)],
      boxes=[(404, 404, 2174, 508)], ack=True)
    m("tooldesc", "08-to-custom", crop=(345, 70, 2232, 1340), mask=[(1518, 304, 1764, 350)],
      boxes=[(404, 404, 2174, 508), (2016, 1254, 2198, 1320)], ack=True)
    m("instruction", "09-instruction-added", crop=(120, 0, 2576, 900), boxes=[(136, 638, 1758, 728)], ack=True)
    for k, v in s.items.items():
        print("shot", k, v)
    return s


if __name__ == "__main__":
    build()

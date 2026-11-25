#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2677 の実画面（2026-11-13 に今の日本語表示の画面で撮り直し）。
元画像＝articles/_shots/raw-2677/*.png（2838x1552）。座標は幅2576で見たときの値。
  python shots.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _howtokit import Shots  # noqa: E402

DLG = (560, 105, 2015, 1305)


def build():
    s = Shots(HERE, HERE.parent / "_shots" / "raw-2677", k=2838 / 2576)
    m = s.make
    m("open", "01-agent-open", crop=(120, 0, 2576, 1250), boxes=[(1846, 262, 2546, 350)], ack=True)
    m("dialog", "02-channel-dialog", crop=(540, 100, 2040, 640), boxes=[(600, 304, 1284, 402)], ack=True)
    m("where", "04-teams-only", crop=(560, 105, 2015, 640), boxes=[(1004, 408, 1700, 518)], ack=True)
    m("version", "05-version-info", crop=DLG, boxes=[(992, 238, 1952, 652), (1738, 1208, 1974, 1278)], ack=True)
    m("added", "06-channel-added", crop=(120, 0, 2576, 1250), boxes=[(1850, 356, 2234, 424), (2370, 22, 2550, 86)], ack=True)
    m("review", "07-review", crop=(1560, 0, 2576, 620))
    m("publish", "08-publish-dialog", crop=(700, 470, 1880, 940), boxes=[(1506, 796, 1796, 868)], ack=True)
    for k, v in s.items.items():
        print("shot", k, v)
    return s


if __name__ == "__main__":
    build()

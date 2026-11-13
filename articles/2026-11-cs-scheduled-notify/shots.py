#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2710 の実画面（2026-11-12 に Copilot Studio の新しいワークフロー画面で撮り直し）。
元画像＝articles/_shots/raw-nav/*.png（2838x1552）。座標は Read で見えた大きさ（幅2576）で書いてある。
  python shots.py   … assets/shot-*.png を作り直す
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _howtokit import Shots  # noqa: E402

AV = (26, 1262, 90, 1328)        # 左下のアバター（左メニューを畳んだ状態）
MAIL = (1898, 446, 2148, 486)    # 接続に出るメールアドレス
PANEL = (1810, 155, 2545, 1380)  # 右の設定パネル


def build():
    s = Shots(HERE, HERE.parent / "_shots" / "raw-nav", k=2838 / 2576)
    m = s.make
    # 画面にたどり着くまで
    m("home", "01-home-nav", crop=(0, 0, 2576, 1150), boxes=[(22, 320, 446, 388)])
    m("list", "02-workflows-list", crop=(0, 0, 2576, 640),
      mask=[(1640, 462, 1900, 625), (1970, 462, 2200, 625), AV], boxes=[(2114, 258, 2512, 348)])
    m("new", "03-new-workflow", mask=[AV], boxes=[(648, 682, 1110, 826), (1846, 366, 2508, 510)])
    # ① トリガー
    m("trigger-types", "04-trigger-types", crop=(1810, 155, 2545, 930), boxes=[(1860, 510, 2494, 600)])
    m("recurrence", "07-recurrence-done", crop=(1810, 155, 2545, 1380),
      boxes=[(1846, 480, 2490, 554), (1846, 742, 2490, 972), (1846, 1272, 2490, 1344)])
    # ② Excel
    m("plus", "07-recurrence-done", crop=(620, 640, 1500, 870), boxes=[(1120, 722, 1182, 786)])
    m("add-dialog", "08-add-step-menu", crop=(540, 100, 2040, 1300), boxes=[(600, 248, 1976, 316)])
    m("search-excel", "09-search-excel", crop=(560, 110, 2016, 900), boxes=[(598, 428, 1272, 538)])
    m("excel-file", "13-excel-file-tree", crop=PANEL, mask=[MAIL],
      boxes=[(1852, 574, 2482, 640), (1852, 722, 2482, 790), (1944, 1066, 2300, 1120)])
    m("excel-done", "15-excel-done", crop=PANEL, mask=[MAIL], boxes=[(1852, 1072, 2482, 1138)])
    # ③ Copilot
    m("copilot-choice", "16-copilot-submenu", crop=(1810, 155, 2545, 1190), boxes=[(1852, 664, 2502, 918)])
    m("copilot-picker", "18-copilot-token-picker", crop=(1810, 155, 2545, 1230), boxes=[(1892, 464, 2476, 528)])
    m("copilot-done", "19-copilot-message-done", crop=(1810, 155, 2545, 1230), boxes=[(1852, 864, 2502, 1012)])
    # ④ Teams
    m("search-teams", "20-search-teams", crop=(560, 110, 2016, 900), boxes=[(598, 428, 1272, 538)])
    m("teams-postin", "22-teams-postin-options", crop=(1780, 155, 2520, 1100), mask=[(1870, 446, 2122, 486)])
    m("teams-picker", "24-teams-token-picker", crop=(1780, 155, 2520, 1380), boxes=[(1896, 690, 2442, 768)])
    m("teams-done", "25-teams-done", crop=(1780, 155, 2520, 1380),
      mask=[(1870, 446, 2122, 486), (1862, 942, 2030, 992)],
      boxes=[(1826, 722, 2456, 790), (1850, 1178, 2434, 1376)])
    # ⑤ 保存
    m("canvas", "26-canvas-full", crop=(290, 660, 1840, 860))
    m("saved", "29-saved", crop=(120, 0, 2576, 280), boxes=[(148, 22, 494, 88), (1968, 24, 2028, 84)])
    m("list-after", "30-workflows-list-after", crop=(0, 0, 2576, 640),
      mask=[(1630, 462, 1900, 625), (1960, 462, 2200, 625), AV], boxes=[(200, 452, 1480, 530)])
    for k, v in s.items.items():
        print("shot", k, v)
    if s.problems:
        print("!! 赤枠を直す:\n  " + "\n  ".join(s.problems))
    return s


if __name__ == "__main__":
    build()

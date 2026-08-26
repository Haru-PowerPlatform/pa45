# -*- coding: utf-8 -*-
"""
PA45 参加バッジ v4 — SVGで設計し、ヘッドレスChromeでレンダリング→Pillowでスーパーサンプリング。

Pillowで線を引くより圧倒的にきれいなベクター仕上がり。
SVGは多色OKなので、アイコンを「フォルダ=ゴールド / 封筒=クリーム」のように塗り分けられる。

使い方:
  python scripts/make-badge-svg.py --vol 15
  python scripts/make-badge-svg.py --vol 15 --out C:\\Temp\\b15.png
依存: Pillow（縮小用）+ ローカルのChrome
"""
import argparse
import math
import os
import subprocess
import sys
import tempfile

from PIL import Image

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT_SIZE = 880          # 最終PNGの一辺
RENDER_SCALE = 2        # 一旦この倍率で描いてから縮小（スーパーサンプリング）

# ---- パレット（Pillow版 make-badge.py と同じ巡回） ------------------------
GOLD = ("#ffe79a", "#f5c542", "#b07c12")   # light, mid, dark
SILV = ("#f1f5f9", "#cbd5e1", "#8292a8")
DEFAULT_PAL = dict(ring=("#7db9ff", "#10265c"), disc=("#2563eb", "#08163a"),
                   gold=GOLD, title="#ffffff", sub="#bcd6ff")
PALETTES = [
    dict(ring=("#86efac", "#06361f"), disc=("#10965c", "#03241a"), gold=GOLD, title="#fff", sub="#a7f3d0"),  # Emerald
    dict(ring=("#d6b8ff", "#2e1058"), disc=("#7c3ad2", "#1c0834"), gold=GOLD, title="#fff", sub="#ddc8ff"),  # Purple (Vol.15)
    dict(ring=("#feb2b2", "#560c16"), disc=("#c82c3a", "#34080c"), gold=GOLD, title="#fff", sub="#fecaca"),  # Crimson (Vol.16)
    dict(ring=("#99f6e4", "#083a3a"), disc=("#0d9494", "#032121"), gold=SILV, title="#fff", sub="#a5f3e8"),  # Teal/Silver
    dict(ring=("#fed7aa", "#682a08"), disc=("#ea781e", "#381805"), gold=("#ffeebc", "#ffd27a", "#b07820"), title="#fff", sub="#fedcb4"),  # Sunset
    dict(ring=("#f9c4e9", "#560e42"), disc=("#c63296", "#2e0826"), gold=GOLD, title="#fff", sub="#f9c4e9"),  # Magenta
]

SESSIONS = {
    15: ("Folder Watch Mail", "2026-06-18", "foldermail"),
    16: ("Copilot Assist", "2026-06-25", "copilot"),
    17: ("Due Date Watch", "2026-07-02", "deadline"),
    18: ("Approval Escalation", "2026-07-09", "approval"),
    19: ("Effect Visualization", "2026-07-16", "dashboard"),
    20: ("Adaptive Cards", "2026-07-23", "card"),
    21: ("First Steps", "2026-07-30", "firststep"),
    22: ("Office Scripts × Copilot", "2026-08-06", "excelscript"),
    23: ("Return Value & Condition", "2026-08-15", "branch"),
    24: ("Reaction Attendance", "2026-08-22", "reaction"),
}


# 回ごとの特別パレット（自動巡回より優先・「かわいい」指定などに対応）
ROSEGOLD = ("#ffeede", "#f4b58f", "#c07d63")  # rose gold: light, mid, dark
PALETTE_OVERRIDE = {
    # Vol.17：かわいいローズピンク × ローズゴールド
    17: dict(ring=("#ffd9ea", "#9c3568"), disc=("#ff8fc0", "#5e1a3d"),
             gold=ROSEGOLD, title="#ffffff", sub="#ffe1ef"),
    # Vol.18：高級感のあるサファイア紺 × ゴールド（承認＝信頼の青）。差し色に
    #          柔らかいペリウィンクルで“かわいさ”を一滴。温色続きからの変化。
    18: dict(ring=("#aecbff", "#0a1c49"), disc=("#2c50cf", "#060e30"),
             gold=GOLD, title="#ffffff", sub="#cfe0ff"),
    # Vol.19：効率化効果の見える化＝成果が積み上がって伸びる。成長のエメラルド×ゴールド。
    #          サファイア青からの変化で、右肩上がりの棒グラフicon（gold）を主役に。
    19: dict(ring=("#a7f3d0", "#04331f"), disc=("#0e9f6e", "#022b1a"),
             gold=GOLD, title="#ffffff", sub="#bbf7d8"),
    # Vol.20：アダプティブカード＝Teams/カードの世界。エメラルドからの変化でインディゴ×ゴールド。
    #          クリーム色のリッチカードicon（金ヘッダー＋アクションボタン）が主役。
    20: dict(ring=("#b7c0ff", "#141c54"), disc=("#4f46e5", "#0b0a33"),
             gold=GOLD, title="#ffffff", sub="#cfd4ff"),
    # Vol.21：原点回帰（基礎・最初の一歩）。PA45の原点であるブルーへ戻す。
    #          階段＋旗の「スタート」iconを主役に。
    21: dict(ring=("#7db9ff", "#0b234f"), disc=("#2563eb", "#08163a"),
             gold=GOLD, title="#ffffff", sub="#cfe0ff"),
    # Vol.22：OfficeスクリプトでExcel自動化。Excelの“表計算グリーン”×ゴールド。
    #          青(21)からの変化で、表計算シート＋Copilotのきらめきiconを主役に。
    22: dict(ring=("#8ef0ab", "#0a3b1c"), disc=("#16a34a", "#052e13"),
             gold=GOLD, title="#ffffff", sub="#b7f3c8"),
    # Vol.23：戻り値で条件分岐＝判断して道が分かれる。グリーン(22)からの変化で、
    #          判断のバイオレット×ゴールド。菱形の条件から2本に分かれる分岐iconが主役。
    23: dict(ring=("#d7c7ff", "#2a1a5e"), disc=("#7c3aed", "#1e0f45"),
             gold=GOLD, title="#ffffff", sub="#e6dcff"),
    # Vol.24：Teamsの👍リアクションで出欠集計。バイオレット(23)からの変化で、
    #          Teamsのインディゴ×ゴールド。吹き出しから立ち上がる親指アップiconが主役。
    24: dict(ring=("#c8caff", "#171a58"), disc=("#4f52c9", "#0b0d33"),
             gold=GOLD, title="#ffffff", sub="#d8daff"),
}


def palette_for(vol):
    if vol in PALETTE_OVERRIDE:
        return PALETTE_OVERRIDE[vol]
    return DEFAULT_PAL if vol < 14 else PALETTES[(vol - 14) % len(PALETTES)]


# ---- アイコン（SVG・多色OK） ---------------------------------------------
def icon_foldermail(g):
    """共有フォルダ監視 → メール通知。フォルダ(金)から封筒(クリーム)が出ている。"""
    gl, gm, gd = g  # gold light/mid/dark
    return f'''
  <g filter="url(#ishadow)">
    <!-- フォルダ背面（タブ付き） -->
    <path d="M330 372 q0 -16 16 -16 h64 q10 0 16 8 l14 16 h94 q16 0 16 16 v94 H330 Z"
          fill="url(#foldback)"/>
    <!-- 封筒（フォルダから上にのぞく） -->
    <g>
      <rect x="372" y="322" width="136" height="118" rx="10" fill="#fffaf0"/>
      <path d="M372 340 L440 392 L508 340" fill="none" stroke="{gd}" stroke-width="9"
            stroke-linejoin="round" stroke-linecap="round"/>
      <path d="M372 340 L440 392 L508 340 L508 332 L440 380 L372 332 Z" fill="{gm}" opacity="0.18"/>
    </g>
    <!-- フォルダ前面ポケット -->
    <path d="M322 404 h236 q14 0 11 14 l-12 60 q-2 10 -14 10 H337 q-12 0 -14 -10 l-12 -60 q-3 -14 11 -14 Z"
          fill="url(#foldfront)"/>
    <path d="M322 404 h236 q14 0 11 14" fill="none" stroke="{gl}" stroke-width="4" opacity="0.7"/>
  </g>'''


def icon_copilot(g):
    """Copilot / AI = 4点キラキラ（大＋小2つ）。"""
    gl, gm, gd = g
    def spark(cx, cy, r, inner=0.30):
        pts = []
        for i in range(8):
            ang = -math.pi / 2 + i * math.pi / 4
            rad = r if i % 2 == 0 else r * inner
            pts.append(f"{cx + rad*math.cos(ang):.1f},{cy + rad*math.sin(ang):.1f}")
        return " ".join(pts)
    return f'''
  <g filter="url(#ishadow)">
    <polygon points="{spark(420, 405, 96)}" fill="url(#sparkgrad)"/>
    <polygon points="{spark(520, 470, 40)}" fill="{gl}"/>
    <polygon points="{spark(512, 338, 28)}" fill="{gm}"/>
  </g>'''


def icon_deadline(g):
    """期限の見張り番 = 目覚まし時計（締切を見張る）。金のベル＋文字盤＋針。"""
    gl, gm, gd = g
    cx, cy, r = 440, 400, 64
    ticks = ""
    for i in range(12):
        a = -math.pi / 2 + i * math.pi / 6
        ro, ri = r - 6, (r - 17 if i % 3 == 0 else r - 12)
        w = 5 if i % 3 == 0 else 3
        ticks += (f'<line x1="{cx+ro*math.cos(a):.1f}" y1="{cy+ro*math.sin(a):.1f}" '
                  f'x2="{cx+ri*math.cos(a):.1f}" y2="{cy+ri*math.sin(a):.1f}" '
                  f'stroke="{gd}" stroke-width="{w}" stroke-linecap="round"/>')
    return f'''
  <g filter="url(#ishadow)">
    <!-- 脚 -->
    <rect x="{cx-60}" y="{cy+r-8}" width="18" height="22" rx="8" fill="{gd}" transform="rotate(24 {cx-51} {cy+r+3})"/>
    <rect x="{cx+42}" y="{cy+r-8}" width="18" height="22" rx="8" fill="{gd}" transform="rotate(-24 {cx+51} {cy+r+3})"/>
    <!-- ベル（左右） -->
    <ellipse cx="{cx-50}" cy="{cy-r-2}" rx="27" ry="24" fill="{gm}" transform="rotate(-30 {cx-50} {cy-r-2})"/>
    <ellipse cx="{cx+50}" cy="{cy-r-2}" rx="27" ry="24" fill="{gm}" transform="rotate(30 {cx+50} {cy-r-2})"/>
    <!-- 打棒 -->
    <rect x="{cx-6}" y="{cy-r-28}" width="12" height="24" rx="6" fill="{gd}"/>
    <circle cx="{cx}" cy="{cy-r-30}" r="11" fill="{gl}"/>
    <!-- 文字盤 -->
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#sparkgrad)"/>
    <circle cx="{cx}" cy="{cy}" r="{r-12}" fill="#fffaf0"/>
    {ticks}
    <!-- 針（締切間近＝10:08あたり） -->
    <line x1="{cx}" y1="{cy}" x2="{cx-25}" y2="{cy-32}" stroke="{gd}" stroke-width="9" stroke-linecap="round"/>
    <line x1="{cx}" y1="{cy}" x2="{cx+34}" y2="{cy-17}" stroke="{gd}" stroke-width="6" stroke-linecap="round"/>
    <circle cx="{cx}" cy="{cy}" r="8" fill="{gd}"/>
  </g>'''


def icon_approval(g):
    """承認エスカレーション = 承認の盾＋チェックに、上へ上げる二段シェブロン。"""
    gl, gm, gd = g
    cx = 440
    return f'''
  <g filter="url(#ishadow)">
    <!-- エスカレーション：上へ上げる二段シェブロン -->
    <path d="M{cx-36} 322 L{cx} 296 L{cx+36} 322" fill="none" stroke="{gl}"
          stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M{cx-36} 350 L{cx} 324 L{cx+36} 350" fill="none" stroke="{gm}"
          stroke-width="15" stroke-linecap="round" stroke-linejoin="round" opacity="0.85"/>
    <!-- 承認の盾 -->
    <path d="M365 368 Q440 352 515 368 L515 440 Q515 488 440 516 Q365 488 365 440 Z"
          fill="url(#sparkgrad)" stroke="{gd}" stroke-width="4"/>
    <!-- 上端ハイライト -->
    <path d="M368 372 Q440 357 512 372 L512 382 Q440 368 368 382 Z" fill="{gl}" opacity="0.55"/>
    <!-- チェック（承認済み） -->
    <path d="M406 438 l24 27 l50 -60" fill="none" stroke="#fffaf0" stroke-width="18"
          stroke-linecap="round" stroke-linejoin="round"/>
  </g>'''


def icon_dashboard(g):
    """効率化効果の見える化 = 右肩上がりの棒グラフ（金）＋上昇トレンド矢印。"""
    gl, gm, gd = g
    base = 486
    w = 40
    bars = [(342, 436), (394, 406), (446, 372), (498, 334)]  # (x, top_y)
    rects = ""
    for (x, ty) in bars:
        rects += (f'    <rect x="{x}" y="{ty}" width="{w}" height="{base-ty}" rx="7" '
                  f'fill="url(#sparkgrad)" stroke="{gd}" stroke-width="3"/>\n')
        rects += (f'    <rect x="{x+6}" y="{ty+5}" width="{w-12}" height="8" rx="4" '
                  f'fill="{gl}" opacity="0.6"/>\n')
    return f'''
  <g filter="url(#ishadow)">
{rects}    <!-- 上昇トレンド矢印 -->
    <path d="M354 430 L408 402 L460 366 L516 324" fill="none" stroke="#fffaf0"
          stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M490 320 L524 310 L514 344 Z" fill="#fffaf0"/>
  </g>'''


def icon_card(g):
    """アダプティブカード = 金ヘッダー＋項目行＋アクションボタン付きのリッチカード。"""
    gl, gm, gd = g
    x, y, w, h, r = 350, 298, 180, 182, 18
    return f'''
  <g filter="url(#ishadow)">
    <!-- カード本体（クリーム） -->
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fffaf0" stroke="{gd}" stroke-width="4"/>
    <!-- ヘッダーバー（金・上端だけ丸め） -->
    <path d="M{x} {y+36} V{y+r} Q{x} {y} {x+r} {y} H{x+w-r} Q{x+w} {y} {x+w} {y+r} V{y+36} Z"
          fill="url(#sparkgrad)"/>
    <rect x="{x+16}" y="{y+13}" width="98" height="11" rx="5.5" fill="#fffaf0" opacity="0.92"/>
    <!-- 項目行 -->
    <rect x="{x+18}" y="{y+58}" width="{w-36}" height="11" rx="5.5" fill="{gm}" opacity="0.55"/>
    <rect x="{x+18}" y="{y+80}" width="{w-62}" height="11" rx="5.5" fill="{gm}" opacity="0.40"/>
    <rect x="{x+18}" y="{y+102}" width="{w-44}" height="11" rx="5.5" fill="{gm}" opacity="0.40"/>
    <!-- アクションボタン -->
    <rect x="{x+18}" y="{y+132}" width="{w-36}" height="42" rx="13"
          fill="url(#sparkgrad)" stroke="{gd}" stroke-width="3"/>
    <rect x="{x+28}" y="{y+140}" width="{w-56}" height="9" rx="4.5" fill="{gl}" opacity="0.60"/>
  </g>'''


def icon_firststep(g):
    """最初の一歩（原点回帰・基礎）= 一段ずつ上る階段＋てっぺんに旗（スタート）。"""
    gl, gm, gd = g
    steps = [(336, 430, 66, 48), (402, 398, 66, 80), (468, 360, 66, 118)]
    rects = ""
    for x, y, w, h in steps:
        rects += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" '
                  f'fill="url(#sparkgrad)" stroke="{gd}" stroke-width="3"/>'
                  f'<rect x="{x+6}" y="{y+6}" width="{w-12}" height="10" rx="5" '
                  f'fill="{gl}" opacity="0.55"/>')
    px = 501  # 旗のポール（最上段の中央）
    return f'''
  <g filter="url(#ishadow)">
    {rects}
    <!-- 旗ポール -->
    <rect x="{px}" y="286" width="7" height="82" rx="3.5" fill="{gd}"/>
    <circle cx="{px+3}" cy="286" r="8" fill="{gl}"/>
    <!-- 旗（スタート＝最初の一歩） -->
    <path d="M{px+7} 292 L{px+52} 308 L{px+7} 324 Z" fill="url(#sparkgrad)"
          stroke="{gd}" stroke-width="3" stroke-linejoin="round"/>
  </g>'''


def icon_excelscript(g):
    """OfficeスクリプトとCopilotでExcel自動化 = 表計算シート＋Copilotのきらめき。"""
    gl, gm, gd = g
    x0, y0, w, h = 350, 322, 180, 168
    hdr = y0 + 40                       # ヘッダー行の下端
    # 縦グリッド（4列）と横グリッド
    grid = ""
    for i in range(1, 4):
        gx = x0 + w * i / 4
        grid += (f'<line x1="{gx:.0f}" y1="{hdr}" x2="{gx:.0f}" y2="{y0+h}" '
                 f'stroke="{gm}" stroke-width="2.4" opacity="0.55"/>')
    for i in range(1, 3):
        gy = hdr + (h - 40) * i / 3
        grid += (f'<line x1="{x0}" y1="{gy:.0f}" x2="{x0+w}" y2="{gy:.0f}" '
                 f'stroke="{gm}" stroke-width="2.4" opacity="0.55"/>')
    # アクセントで塗る2セル（自動で埋まる“結果”のニュアンス）
    cw, ch = w / 4, (h - 40) / 3
    cell1 = f'<rect x="{x0+cw:.0f}" y="{hdr:.0f}" width="{cw:.0f}" height="{ch:.0f}" fill="{gl}" opacity="0.7"/>'
    cell2 = f'<rect x="{x0+2*cw:.0f}" y="{hdr+ch:.0f}" width="{cw:.0f}" height="{ch:.0f}" fill="{gm}" opacity="0.45"/>'
    # Copilotのきらめき（右上に飛び出す4点星・大小）
    def star(px, py, R, r):
        return (f'<path d="M{px} {py-R} L{px+r} {py-r} L{px+R} {py} L{px+r} {py+r} '
                f'L{px} {py+R} L{px-r} {py+r} L{px-R} {py} L{px-r} {py-r} Z" '
                f'fill="url(#sparkgrad)" stroke="{gd}" stroke-width="2.5" stroke-linejoin="round"/>')
    spark = star(524, 322, 30, 9) + star(556, 356, 15, 4)
    return f'''
  <g filter="url(#ishadow)">
    <!-- シート本体 -->
    <rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="14"
          fill="#fffaf0" stroke="{gd}" stroke-width="4"/>
    <!-- ヘッダー行（金） -->
    <path d="M{x0} {y0+14} q0 -14 14 -14 h{w-28} q14 0 14 14 v26 H{x0} Z" fill="url(#sparkgrad)"/>
    {cell1}{cell2}
    {grid}
    <!-- 外枠の内側ハイライト -->
    <rect x="{x0+4}" y="{hdr+3}" width="{w-8}" height="8" rx="4" fill="{gl}" opacity="0.35"/>
    {spark}
  </g>'''


def icon_branch(g):
    """戻り値で条件分岐 = 条件の菱形から2本に分かれ、はい(✓)/いいえ に振り分ける。"""
    gl, gm, gd = g
    cx = 445
    dY, ds = 322, 34            # 菱形の中心・半径
    lX, rX = 372, 518           # 左右ノードの中心X
    nY, nw, nh = 470, 74, 56    # ノードの中心Y・幅・高さ
    # 菱形の下頂点から左右ノードへ分かれる2本のライン
    lines = (
        f'<path d="M{cx} {dY+ds} C {cx} {dY+ds+52}, {lX} {nY-96}, {lX} {nY-nh/2-6}" '
        f'fill="none" stroke="{gd}" stroke-width="7" stroke-linecap="round"/>'
        f'<path d="M{cx} {dY+ds} C {cx} {dY+ds+52}, {rX} {nY-96}, {rX} {nY-nh/2-6}" '
        f'fill="none" stroke="{gd}" stroke-width="7" stroke-linecap="round"/>'
    )
    check = (f'<path d="M{lX-16} {nY} l11 12 l20 -23" fill="none" stroke="{gd}" '
             f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
    dot = f'<circle cx="{rX}" cy="{nY}" r="9" fill="{gd}"/>'
    return f'''
  <g filter="url(#ishadow)">
    {lines}
    <!-- 左ノード（はい＝金） -->
    <rect x="{lX-nw/2:.0f}" y="{nY-nh/2:.0f}" width="{nw}" height="{nh}" rx="12"
          fill="url(#sparkgrad)" stroke="{gd}" stroke-width="4"/>
    {check}
    <!-- 右ノード（いいえ＝クリーム） -->
    <rect x="{rX-nw/2:.0f}" y="{nY-nh/2:.0f}" width="{nw}" height="{nh}" rx="12"
          fill="#fffaf0" stroke="{gd}" stroke-width="4"/>
    {dot}
    <!-- 条件の菱形 -->
    <polygon points="{cx},{dY-ds} {cx+ds},{dY} {cx},{dY+ds} {cx-ds},{dY}"
             fill="url(#sparkgrad)" stroke="{gd}" stroke-width="4.5" stroke-linejoin="round"/>
    <polygon points="{cx},{dY-ds+8} {cx+ds-8},{dY} {cx},{dY+ds-8} {cx-ds+8},{dY}"
             fill="{gl}" opacity="0.35"/>
  </g>'''


def icon_reaction(g):
    """Teamsの投稿に押した👍で出欠が集まる = 吹き出しから親指アップが立ち上がる。"""
    gl, gm, gd = g
    bx, by, bw, bh = 336, 250, 218, 100      # 吹き出し
    lines = "".join(
        f'<rect x="{bx+24}" y="{by+24+i*22}" width="{w}" height="10" rx="5" '
        f'fill="{gd}" opacity="0.45"/>'
        for i, w in enumerate((150, 118, 86)))
    tail = (f'<path d="M{bx+58} {by+bh} l0 30 l34 -30 z" fill="#fffaf0" '
            f'stroke="{gd}" stroke-width="4.5" stroke-linejoin="round"/>')
    # 親指アップ（手のひら＝金グラデ／袖口＝クリーム）
    hand = (f'<path d="M436 400 q4 -34 22 -50 q13 -11 21 0 q7 9 0 24 l-11 25 h47 '
            f'q19 0 15 19 l-13 47 q-5 15 -22 15 h-59 z" '
            f'fill="url(#sparkgrad)" stroke="{gd}" stroke-width="4.5" stroke-linejoin="round"/>')
    cuff = (f'<rect x="392" y="396" width="40" height="84" rx="12" fill="#fffaf0" '
            f'stroke="{gd}" stroke-width="4.5"/>')
    spark = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{gl}" opacity="0.85"/>'
        for x, y, r in ((392, 356, 7), (516, 350, 6), (546, 392, 5)))
    return f'''
  <g filter="url(#ishadow)" transform="translate(0,14)">
    {tail}
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="22" fill="#fffaf0"
          stroke="{gd}" stroke-width="4.5"/>
    {lines}
    {spark}
    {cuff}
    {hand}
  </g>'''


ICONS = {"foldermail": icon_foldermail, "copilot": icon_copilot,
         "deadline": icon_deadline, "approval": icon_approval,
         "dashboard": icon_dashboard, "card": icon_card,
         "firststep": icon_firststep, "excelscript": icon_excelscript,
         "branch": icon_branch,
         "reaction": icon_reaction}


def knurl_dots(cx, cy, r, n, color):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{color}"/>')
    return "\n".join(out)


def text3d(cx, y, size, ls, fill, depth, weight, s, sheen=True):
    """立体（浮き上がり）テキスト：暗い層を下に数枚重ねて押し出し感＋上に光沢ハイライト。"""
    fam = "'Noto Sans JP','Segoe UI',sans-serif"
    base = (f'font-family="{fam}" font-weight="{weight}" '
            f'font-size="{size}" letter-spacing="{ls}" text-anchor="middle"')
    layers = ""
    for d in range(5, 0, -1):
        op = 0.9 if d <= 2 else 0.5
        layers += (f'<text x="{cx}" y="{y + d}" fill="{depth}" fill-opacity="{op}" {base}>{s}</text>')
    # 上端の白ハイライト（ガラス光沢）
    hi = (f'<text x="{cx}" y="{y - 1.2}" fill="#ffffff" fill-opacity="0.30" {base}>{s}</text>'
          if sheen else "")
    top = f'<text x="{cx}" y="{y}" fill="{fill}" {base}>{s}</text>'
    return layers + top + hi


def build_svg(vol, theme, date, key, pal):
    C = 880
    cx = cy = C / 2
    R = 388
    rim = 334
    ID = 300
    gl, gm, gd = pal["gold"]
    title = theme.upper()
    # タイトル長に応じてフォントサイズを調整
    tsize = 70 if len(title) <= 12 else (58 if len(title) <= 17 else 48)
    icon_svg = ICONS.get(key, ICONS["foldermail"])(pal["gold"])

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {C} {C}" width="{C}" height="{C}">
  <defs>
    <linearGradient id="ringgrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{pal['ring'][0]}"/>
      <stop offset="1" stop-color="{pal['ring'][1]}"/>
    </linearGradient>
    <radialGradient id="discgrad" cx="0.5" cy="0.42" r="0.62">
      <stop offset="0" stop-color="{pal['disc'][0]}"/>
      <stop offset="1" stop-color="{pal['disc'][1]}"/>
    </radialGradient>
    <linearGradient id="goldrim" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{gl}"/>
      <stop offset="0.5" stop-color="{gm}"/>
      <stop offset="1" stop-color="{gd}"/>
    </linearGradient>
    <linearGradient id="foldback" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{gm}"/>
      <stop offset="1" stop-color="{gd}"/>
    </linearGradient>
    <linearGradient id="foldfront" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{gl}"/>
      <stop offset="1" stop-color="{gm}"/>
    </linearGradient>
    <linearGradient id="sparkgrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{gl}"/>
      <stop offset="1" stop-color="{gm}"/>
    </linearGradient>
    <radialGradient id="gloss" cx="0.5" cy="0.30" r="0.56">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.60"/>
      <stop offset="0.55" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="vign" cx="0.5" cy="0.60" r="0.62">
      <stop offset="0.55" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.30"/>
    </radialGradient>
    <linearGradient id="bevel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.75"/>
      <stop offset="0.5" stop-color="#ffffff" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.35"/>
    </linearGradient>
    <filter id="dshadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="14" stdDeviation="22" flood-color="#000" flood-opacity="0.55"/>
    </filter>
    <filter id="ishadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="5" stdDeviation="6" flood-color="#000" flood-opacity="0.35"/>
    </filter>
    <clipPath id="discclip"><circle cx="{cx}" cy="{cy}" r="{ID}"/></clipPath>
  </defs>

  <!-- 外周メタリック -->
  <circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#ringgrad)" filter="url(#dshadow)"/>
  <!-- ノブ（粒） -->
  {knurl_dots(cx, cy, (R + rim) / 2 + 4, 40, gm)}
  <!-- ゴールドリム（二重） -->
  <circle cx="{cx}" cy="{cy}" r="{rim}" fill="none" stroke="url(#goldrim)" stroke-width="14"/>
  <circle cx="{cx}" cy="{cy}" r="{rim - 12}" fill="none" stroke="{gd}" stroke-width="3" opacity="0.6"/>
  <!-- 内側ディスク -->
  <circle cx="{cx}" cy="{cy}" r="{ID}" fill="url(#discgrad)"/>
  <circle cx="{cx}" cy="{cy}" r="{ID}" fill="none" stroke="url(#goldrim)" stroke-width="5"/>

  <!-- ブランド（立体） -->
  {text3d(cx, 248, 27, 6, gl, gd, 700, "POWER AUTOMATE 45")}
  <line x1="{cx-150}" y1="266" x2="{cx+150}" y2="266" stroke="{gm}" stroke-width="2" opacity="0.7"/>
  <line x1="{cx-150}" y1="267.4" x2="{cx+150}" y2="267.4" stroke="#ffffff" stroke-width="1" opacity="0.35"/>

  <!-- アイコン -->
  {icon_svg}

  <!-- テーマ名（立体） -->
  {text3d(cx, 572, tsize, 1, pal['title'], gd, 800, title)}
  <!-- VOL・日付（立体） -->
  {text3d(cx, 618, 24, 3, pal['sub'], gd, 600, f"VOL.{vol} · {date}", sheen=False)}

  <!-- 光沢・立体（上半分ハイライト＋下部の陰影＋内周ベベル） -->
  <g clip-path="url(#discclip)">
    <ellipse cx="{cx}" cy="{cy-118}" rx="285" ry="180" fill="url(#gloss)"/>
    <!-- 内周の落ち込み影（凹んだコイン面＝立体感） -->
    <circle cx="{cx}" cy="{cy}" r="{ID}" fill="none" stroke="#000000" stroke-width="24" opacity="0.30"/>
    <circle cx="{cx}" cy="{cy}" r="{ID}" fill="url(#vign)"/>
  </g>
  <!-- 内周ベベルリング（金属の縁の立体感） -->
  <circle cx="{cx}" cy="{cy}" r="{ID-3}" fill="none" stroke="url(#bevel)" stroke-width="9" opacity="1"/>
  <circle cx="{cx}" cy="{cy}" r="{rim}" fill="none" stroke="url(#bevel)" stroke-width="6" opacity="0.85"/>
</svg>'''


def render(svg, out_path):
    rs = OUT_SIZE * RENDER_SCALE
    with tempfile.TemporaryDirectory() as td:
        html = os.path.join(td, "badge.html")
        big = os.path.join(td, "big.png")
        with open(html, "w", encoding="utf-8") as f:
            f.write(f'<!doctype html><html><head><meta charset="utf-8">'
                    f'<style>html,body{{margin:0;padding:0;background:transparent}}'
                    f'svg{{display:block;width:{rs}px;height:{rs}px}}</style></head>'
                    f'<body>{svg}</body></html>')
        cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--no-sandbox", "--force-device-scale-factor=1",
               f"--window-size={rs},{rs}", "--default-background-color=00000000",
               f"--screenshot={big}", "file:///" + html.replace("\\", "/")]
        subprocess.run(cmd, check=True, capture_output=True)
        img = Image.open(big).convert("RGBA")
        img = img.crop((0, 0, rs, rs)).resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        img.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vol", type=int, required=True)
    ap.add_argument("--theme", default=None)
    ap.add_argument("--date", default=None)
    ap.add_argument("--icon", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    theme = date = key = None
    if args.vol in SESSIONS:
        theme, date, key = SESSIONS[args.vol]
    theme = args.theme or theme
    date = args.date or date
    key = args.icon or key or "foldermail"
    if not theme or not date:
        print("ERROR: --theme と --date を指定してください")
        sys.exit(1)

    out = args.out or rf"C:\Users\isamu\Documents\pa45\assets\badges\session-{args.vol:03d}\badge.png"
    svg = build_svg(args.vol, theme, date, key, palette_for(args.vol))
    print("OK:", render(svg, out))


if __name__ == "__main__":
    main()

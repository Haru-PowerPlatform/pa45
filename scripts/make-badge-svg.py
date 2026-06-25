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
}


def palette_for(vol):
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


ICONS = {"foldermail": icon_foldermail, "copilot": icon_copilot}


def knurl_dots(cx, cy, r, n, color):
    out = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{color}"/>')
    return "\n".join(out)


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
    <radialGradient id="gloss" cx="0.5" cy="0.32" r="0.5">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.45"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <filter id="dshadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="10" stdDeviation="16" flood-color="#000" flood-opacity="0.45"/>
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

  <!-- ブランド -->
  <text x="{cx}" y="296" text-anchor="middle" fill="{gm}"
        font-family="'Noto Sans JP','Segoe UI',sans-serif" font-weight="700"
        font-size="27" letter-spacing="6">POWER AUTOMATE 45</text>
  <line x1="{cx-150}" y1="312" x2="{cx+150}" y2="312" stroke="{gm}" stroke-width="2" opacity="0.7"/>

  <!-- アイコン -->
  {icon_svg}

  <!-- テーマ名 -->
  <text x="{cx}" y="560" text-anchor="middle" fill="{pal['title']}"
        font-family="'Noto Sans JP','Segoe UI',sans-serif" font-weight="800"
        font-size="{tsize}" letter-spacing="1">{title}</text>
  <!-- VOL・日付 -->
  <text x="{cx}" y="606" text-anchor="middle" fill="{pal['sub']}"
        font-family="'Noto Sans JP','Segoe UI',sans-serif" font-weight="600"
        font-size="24" letter-spacing="3">VOL.{vol} · {date}</text>

  <!-- 光沢（上半分） -->
  <g clip-path="url(#discclip)">
    <ellipse cx="{cx}" cy="{cy-110}" rx="280" ry="170" fill="url(#gloss)"/>
  </g>
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

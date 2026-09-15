# -*- coding: utf-8 -*-
"""
PA45 参加バッジ v5 — 六角形・モノラインアイコンに、立体の縁・光沢・リボン帯を足したデザイン（2026-09-15〜）。

v4（make-badge-svg.py）の「メダル＋立体文字＋ギザ縁」から一新。
資格バッジ系の落ち着いた見た目に寄せ、次の4点だけで構成する：
  1. 六角形の本体（濃紺）＋ アクセント色の細い縁
  2. 細い線で描いたアイコン（白＋アクセント1色）
  3. 英字タイトル（Bahnschrift の詰めた書体）
  4. アクセント色の帯に「PARTICIPANT · VOL.NN」、下に日付

※特定企業のロゴ・ワードマーク・ブランド色は使わない（雰囲気だけ借りる）。

使い方:
  python scripts/make-badge-v5.py --vol 27
  python scripts/make-badge-v5.py --vol 27 --out C:\\Temp\\b27.png
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
OUT_SIZE = 880
RENDER_SCALE = 2

# 回ごとの設定： vol: (英字タイトル, 日付, アイコンキー, アクセント色)
SESSIONS = {
    27: ("SHOW COPILOT", "2026-09-10", "handoff", "#8b5cf6"),
}

# アクセント色の既定の巡回（SESSIONS に色が無い回に使う）
ACCENTS = ["#22d3ee", "#f59e0b", "#8b5cf6", "#10b981", "#f43f5e", "#3b82f6"]

W = 880
CX, CY = 440, 440


# ---------------------------------------------------------------------------
# 形
# ---------------------------------------------------------------------------
def hex_points(r, cx=CX, cy=CY):
    """頂点が上下にある六角形"""
    pts = []
    for k in range(6):
        a = math.radians(-90 + 60 * k)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


# ---------------------------------------------------------------------------
# アイコン（中心 440,350 付近・おおよそ 240×120 の枠に収める）
# ---------------------------------------------------------------------------
def icon_handoff(accent):
    """資料（スクショ／JSON）を、Copilot の吹き出しに渡す"""
    s = 'stroke="#ffffff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    return f'''
  <g transform="translate(-12,0)">
    <!-- 書類（右上が折れた紙） -->
    <path d="M336,288 H382 L408,314 V388 H336 Z" {s}/>
    <path d="M382,288 V314 H408" {s}/>
    <line x1="352" y1="336" x2="392" y2="336" {s}/>
    <line x1="352" y1="354" x2="392" y2="354" {s}/>
    <line x1="352" y1="372" x2="376" y2="372" {s}/>
    <!-- 渡す矢印 -->
    <line x1="428" y1="338" x2="462" y2="338" stroke="{accent}" stroke-width="8" stroke-linecap="round"/>
    <path d="M450,324 L466,338 L450,352" stroke="{accent}" stroke-width="8"
          stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <!-- 吹き出し -->
    <path d="M500,292 H566 A18,18 0 0 1 584,310 V352 A18,18 0 0 1 566,370
             H524 L500,390 V370 A18,18 0 0 1 482,352 V310 A18,18 0 0 1 500,292 Z" {s}/>
    <!-- 吹き出しの中のきらめき -->
    <path d="M533,310 C536,326 540,330 556,332 C540,334 536,338 533,354
             C530,338 526,334 510,332 C526,330 530,326 533,310 Z" fill="{accent}"/>
  </g>'''


ICONS = {
    "handoff": icon_handoff,
}


# ---------------------------------------------------------------------------
# 本体
# ---------------------------------------------------------------------------
def _mix(hex_color, target, t):
    """hex_color を target（'#ffffff' か '#000000'）へ t の割合で寄せる"""
    a = [int(hex_color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(target[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(a, b))


def build_svg(vol, title, date, icon_key, accent):
    # 帯の両端と落ち影のぶん、六角形を少し小さくしてある
    R_RIM, R_BODY, R_LINE = 372, 342, 316
    hi = _mix(accent, "#ffffff", 0.55)   # 明るい面
    lo = _mix(accent, "#000000", 0.50)   # 暗い面
    lo2 = _mix(accent, "#000000", 0.72)  # 折り返しの影
    icon = ICONS[icon_key](accent)
    body_pts = hex_points(R_BODY)

    # 帯（リボン）の座標
    BY, BH = 552, 72            # 帯の上端・高さ
    BX0, BX1 = 82, 798          # 帯の左右端
    TD = 20                     # 後ろに回る尾の下がり幅
    tail_l = f"{BX0+22},{BY+TD} 30,{BY+TD} 52,{BY+TD+BH/2} 30,{BY+TD+BH} {BX0+22},{BY+TD+BH}"
    tail_r = f"{BX1-22},{BY+TD} 850,{BY+TD} 828,{BY+TD+BH/2} 850,{BY+TD+BH} {BX1-22},{BY+TD+BH}"
    fold_l = f"{BX0},{BY+BH} {BX0+22},{BY+BH+TD} {BX0+22},{BY+BH}"
    fold_r = f"{BX1},{BY+BH} {BX1-22},{BY+BH+TD} {BX1-22},{BY+BH}"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}">
  <defs>
    <!-- 縁：左上が明るく右下が暗い金属の面 -->
    <linearGradient id="rim" x1="0.15" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{hi}"/>
      <stop offset="0.45" stop-color="{accent}"/>
      <stop offset="1" stop-color="{lo}"/>
    </linearGradient>
    <!-- 縁の面取りハイライト（上側だけ光る） -->
    <linearGradient id="bevel" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.95"/>
      <stop offset="0.5" stop-color="#ffffff" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.55"/>
    </linearGradient>
    <!-- 本体 -->
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#34466c"/>
      <stop offset="0.55" stop-color="#141d31"/>
      <stop offset="1" stop-color="#060a13"/>
    </linearGradient>
    <!-- 上半分の光沢 -->
    <linearGradient id="gloss" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.20"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0.00"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.38"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <!-- 帯：上が明るく下が暗い -->
    <linearGradient id="band" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{hi}"/>
      <stop offset="0.5" stop-color="{accent}"/>
      <stop offset="1" stop-color="{lo}"/>
    </linearGradient>
    <linearGradient id="title" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff"/>
      <stop offset="1" stop-color="#cfd9ea"/>
    </linearGradient>

    <filter id="drop" x="-20%" y="-20%" width="140%" height="150%">
      <feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000000" flood-opacity="0.60"/>
    </filter>
    <filter id="lift" x="-20%" y="-40%" width="140%" height="200%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000000" flood-opacity="0.78"/>
    </filter>
    <filter id="bandshadow" x="-10%" y="-60%" width="120%" height="260%">
      <feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#000000" flood-opacity="0.68"/>
    </filter>
    <filter id="blur10"><feGaussianBlur stdDeviation="12"/></filter>

    <clipPath id="clip"><polygon points="{body_pts}"/></clipPath>
    <style>
      .t {{ font-family: Bahnschrift, 'Segoe UI', sans-serif; font-stretch: condensed; }}
    </style>
  </defs>

  <g filter="url(#drop)">
    <!-- 帯の尾（本体の後ろ） -->
    <polygon points="{tail_l}" fill="{lo}"/>
    <polygon points="{tail_r}" fill="{lo}"/>

    <!-- 縁 -->
    <polygon points="{hex_points(R_RIM)}" fill="url(#rim)" stroke="url(#rim)"
             stroke-width="38" stroke-linejoin="round"/>
    <!-- 縁の面取り -->
    <polygon points="{hex_points(R_RIM + 17)}" fill="none" stroke="url(#bevel)"
             stroke-width="4" stroke-linejoin="round"/>
    <polygon points="{hex_points(R_BODY + 10)}" fill="none" stroke="#000000"
             stroke-opacity="0.55" stroke-width="4" stroke-linejoin="round"/>

    <!-- 本体 -->
    <polygon points="{body_pts}" fill="url(#body)" stroke="#0a101d"
             stroke-width="18" stroke-linejoin="round"/>

    <g clip-path="url(#clip)">
      <!-- 縁から内側へ落ちる影（くぼみ） -->
      <polygon points="{body_pts}" fill="none" stroke="#000000" stroke-opacity="0.90"
               stroke-width="64" filter="url(#blur10)"/>
      <!-- アイコンの後ろの光 -->
      <circle cx="{CX}" cy="345" r="200" fill="url(#glow)"/>
      <!-- 内側の細い線 -->
      <polygon points="{hex_points(R_LINE)}" fill="none" stroke="#ffffff"
               stroke-opacity="0.10" stroke-width="2" stroke-linejoin="round"/>
      <!-- 光沢：上半分を弧で切った面 -->
      <path d="M0,0 H{W} V330 Q{CX},270 0,380 Z" fill="url(#gloss)"/>
      <!-- 斜めに走るつや（境目が出ないようにぼかす） -->
      <polygon points="250,60 330,60 150,520 70,520" fill="#ffffff" fill-opacity="0.06"
               filter="url(#blur10)"/>
    </g>

    <!-- 上の小さな名前 -->
    <text class="t" x="{CX}" y="212" text-anchor="middle" font-size="24" font-weight="600"
          letter-spacing="7" fill="#d5deeb" filter="url(#lift)">POWER AUTOMATE 45</text>
    <rect x="{CX - 34}" y="230" width="68" height="4" rx="2" fill="{accent}"/>

    <!-- アイコン（少し縮めて影をつける） -->
    <g filter="url(#lift)" transform="translate({CX},352) scale(0.93) translate({-CX},-340)">
      {icon}
    </g>

    <!-- タイトル -->
    <text class="t" x="{CX}" y="512" text-anchor="middle" font-size="66" font-weight="700"
          letter-spacing="3" fill="url(#title)" filter="url(#lift)">{title}</text>

    <!-- 帯（リボン） -->
    <polygon points="{fold_l}" fill="{lo2}"/>
    <polygon points="{fold_r}" fill="{lo2}"/>
    <g filter="url(#bandshadow)">
      <rect x="{BX0}" y="{BY}" width="{BX1 - BX0}" height="{BH}" fill="url(#band)"/>
    </g>
    <rect x="{BX0}" y="{BY}" width="{BX1 - BX0}" height="3" fill="#ffffff" fill-opacity="0.55"/>
    <rect x="{BX0}" y="{BY + BH - 3}" width="{BX1 - BX0}" height="3" fill="#000000" fill-opacity="0.45"/>
    <text class="t" x="{CX}" y="{BY + 47}" text-anchor="middle" font-size="31" font-weight="700"
          letter-spacing="5" fill="#ffffff" filter="url(#lift)">PARTICIPANT · VOL.{vol}</text>

    <!-- 日付 -->
    <text class="t" x="{CX}" y="676" text-anchor="middle" font-size="25" font-weight="400"
          letter-spacing="4" fill="#9aa8bd">{date.replace("-", ".")}</text>
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
    ap.add_argument("--title", default=None)
    ap.add_argument("--date", default=None)
    ap.add_argument("--icon", default=None)
    ap.add_argument("--accent", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    title = date = key = accent = None
    if args.vol in SESSIONS:
        title, date, key, accent = SESSIONS[args.vol]
    title = args.title or title
    date = args.date or date
    key = args.icon or key or "handoff"
    accent = args.accent or accent or ACCENTS[args.vol % len(ACCENTS)]
    if not title or not date:
        print("ERROR: --title と --date を指定してください")
        sys.exit(1)

    out = args.out or rf"C:\Users\isamu\Documents\pa45\assets\badges\session-{args.vol:03d}\badge.png"
    print("OK:", render(build_svg(args.vol, title.upper(), date, key, accent), out))


if __name__ == "__main__":
    main()

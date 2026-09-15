# -*- coding: utf-8 -*-
"""
PA45 参加バッジ v5 — フラット・六角形・モノラインアイコンの新デザイン（2026-09-15〜）。

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
def build_svg(vol, title, date, icon_key, accent):
    R_RIM, R_BODY, R_LINE = 396, 378, 350
    icon = ICONS[icon_key](accent)
    body_pts = hex_points(R_BODY)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{W}" height="{W}">
  <defs>
    <linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#26324a"/>
      <stop offset="1" stop-color="#0d1422"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.30"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="clip"><polygon points="{body_pts}"/></clipPath>
    <!-- 帯だけは本体の暗い縁の外側まで伸ばして、紫の縁とつなげる -->
    <clipPath id="clipband"><polygon points="{hex_points(R_BODY + 14)}"/></clipPath>
    <style>
      .t {{ font-family: Bahnschrift, 'Segoe UI', sans-serif; font-stretch: condensed; }}
    </style>
  </defs>

  <!-- 縁（角を丸めるため同色の太い線を重ねる） -->
  <polygon points="{hex_points(R_RIM)}" fill="{accent}" stroke="{accent}"
           stroke-width="28" stroke-linejoin="round"/>
  <!-- 本体 -->
  <polygon points="{body_pts}" fill="url(#body)" stroke="#0d1422"
           stroke-width="22" stroke-linejoin="round"/>

  <g clip-path="url(#clip)">
    <!-- アイコンの後ろの淡い光 -->
    <circle cx="{CX}" cy="340" r="190" fill="url(#glow)"/>
    <!-- 内側の細い線 -->
    <polygon points="{hex_points(R_LINE)}" fill="none" stroke="#ffffff"
             stroke-opacity="0.10" stroke-width="2" stroke-linejoin="round"/>
  </g>
  <!-- 帯 -->
  <rect x="0" y="566" width="{W}" height="70" fill="{accent}" clip-path="url(#clipband)"/>

  <!-- 上の小さな名前 -->
  <text class="t" x="{CX}" y="196" text-anchor="middle" font-size="25" font-weight="600"
        letter-spacing="7" fill="#cbd5e1">POWER AUTOMATE 45</text>
  <rect x="{CX - 36}" y="216" width="72" height="4" rx="2" fill="{accent}"/>

  {icon}

  <!-- タイトル -->
  <text class="t" x="{CX}" y="520" text-anchor="middle" font-size="70" font-weight="700"
        letter-spacing="3" fill="#ffffff">{title}</text>

  <!-- 帯の文字 -->
  <text class="t" x="{CX}" y="613" text-anchor="middle" font-size="32" font-weight="700"
        letter-spacing="5" fill="#ffffff">PARTICIPANT · VOL.{vol}</text>

  <!-- 日付 -->
  <text class="t" x="{CX}" y="692" text-anchor="middle" font-size="26" font-weight="400"
        letter-spacing="4" fill="#94a3b8">{date.replace("-", ".")}</text>
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

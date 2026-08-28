# -*- coding: utf-8 -*-
"""
PA45 参加バッジ v5（フラット六角形）— AWS認定バッジのような、立体メダルではない
モダンでスタイリッシュな見た目。SVGで設計→ヘッドレスChromeでレンダリング→縮小。

使い方:
  python scripts/make-badge-flat.py --vol 25
  python scripts/make-badge-flat.py --vol 25 --out C:\\Temp\\b25.png

v4（make-badge-svg.py・金属メダル調）は残置。回ごとにどちらを使うか選ぶ。
依存: Pillow（縮小用）+ ローカルのChrome
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_badge_render import render  # noqa: E402  （render だけ共有）

# ---- 回ごとの内容 -----------------------------------------------------------
# vol: (英語テーマ 1行目, 英語テーマ 2行目, 日付, アイコンkey)
SESSIONS = {
    25: ("MAIL ATTACHMENT", "AUTO SAVE", "2026-08-27", "mailsave"),
}

# ---- 配色（フラット・落ち着いた深色＋明るいアクセント1色）-------------------
THEMES = {
    # AWS Professional 系の深いネイビー × スカイ
    "navy":  dict(bg1="#0B1B33", bg2="#1B3A6B", line="#7DD3FC", accent="#38BDF8",
                  text="#FFFFFF", sub="#BAE6FD", band="#0A1526"),
    "teal":  dict(bg1="#052E2B", bg2="#0F5F57", line="#5EEAD4", accent="#2DD4BF",
                  text="#FFFFFF", sub="#CCFBF1", band="#03201E"),
    "plum":  dict(bg1="#1E1033", bg2="#4C1D95", line="#C4B5FD", accent="#A78BFA",
                  text="#FFFFFF", sub="#EDE9FE", band="#160B26"),
    "amber": dict(bg1="#2A1503", bg2="#7C3E06", line="#FCD34D", accent="#F59E0B",
                  text="#FFFFFF", sub="#FEF3C7", band="#1C0E02"),
}
VOL_THEME = {25: "navy"}


# ---- アイコン（白の線画・塗りつぶし最小）------------------------------------
def icon_mailsave(c):
    """封筒からファイルが下のフォルダへ落ちる＝メール添付の自動保存。"""
    a, w = c["accent"], "#FFFFFF"
    return f'''
  <g transform="translate(440,236) scale(0.88)" fill="none" stroke="{w}" stroke-width="8"
     stroke-linecap="round" stroke-linejoin="round">
    <!-- 封筒 -->
    <rect x="-96" y="-74" width="192" height="126" rx="12"/>
    <path d="M-96 -62 L0 12 L96 -62"/>
    <!-- クリップ（添付）＝封筒の上ぶちに留める。face を横切らない -->
    <path d="M76 -138 v-8 a16 16 0 0 1 32 0 v44 a24 24 0 0 1 -48 0 v-38"
          stroke="{a}" stroke-width="8"/>
  </g>
  <g transform="translate(440,330)" fill="none" stroke="{a}" stroke-width="7"
     stroke-linecap="round" stroke-linejoin="round">
    <path d="M0 -34 v46"/>
    <path d="M-16 -4 L0 12 L16 -4"/>
  </g>
  <g transform="translate(440,400) scale(0.88)" fill="none" stroke="{w}" stroke-width="8"
     stroke-linecap="round" stroke-linejoin="round">
    <path d="M-104 34 v-72 a10 10 0 0 1 10 -10 h44 l18 20 h122 a10 10 0 0 1 10 10 v52
             a10 10 0 0 1 -10 10 h-184 a10 10 0 0 1 -10 -10 z"/>
  </g>'''


ICONS = {"mailsave": icon_mailsave}



def _rounded_poly(pts, r):
    """頂点リストから、角を半径rで丸めたパス文字列を作る。"""
    import math
    n = len(pts)
    d = []
    for i in range(n):
        x, y = pts[i]
        px, py = pts[(i - 1) % n]
        nx, ny = pts[(i + 1) % n]
        v1 = (px - x, py - y); v2 = (nx - x, ny - y)
        l1 = math.hypot(*v1) or 1.0; l2 = math.hypot(*v2) or 1.0
        rr = min(r, l1 / 2, l2 / 2)
        a = (x + v1[0] / l1 * rr, y + v1[1] / l1 * rr)
        b = (x + v2[0] / l2 * rr, y + v2[1] / l2 * rr)
        if i == 0:
            d.append(f"M{a[0]:.1f},{a[1]:.1f}")
        else:
            d.append(f"L{a[0]:.1f},{a[1]:.1f}")
        d.append(f"Q{x:.1f},{y:.1f} {b[0]:.1f},{b[1]:.1f}")
    d.append("Z")
    return " ".join(d)


def build_svg(vol, l1, l2, date, key, c):
    cx, cy = 440, 440
    W, H = 668, 792                      # 六角形の幅・高さ（縦長・上下がとがる）
    hx = [(cx, cy - H / 2), (cx + W / 2, cy - H / 4), (cx + W / 2, cy + H / 4),
          (cx, cy + H / 2), (cx - W / 2, cy + H / 4), (cx - W / 2, cy - H / 4)]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in hx)
    hexd = _rounded_poly(hx, 52)
    rimd = _rounded_poly([(cx + (x - cx) * 1.035, cy + (y - cy) * 1.035) for x, y in hx], 54)

    iW, iH = W - 46, H - 54              # 内側の細いライン
    ihx = [(cx, cy - iH / 2), (cx + iW / 2, cy - iH / 4), (cx + iW / 2, cy + iH / 4),
           (cx, cy + iH / 2), (cx - iW / 2, cy + iH / 4), (cx - iW / 2, cy - iH / 4)]
    ipts = " ".join(f"{x:.1f},{y:.1f}" for x, y in ihx)
    inid = _rounded_poly(ihx, 44)

    # テーマ文字は長さで自動縮小
    def fit(s, base, maxw=470):
        est = len(s) * base * 0.62
        return base if est <= maxw else max(30, int(base * maxw / est))
    f1, f2 = fit(l1, 54), fit(l2, 54)
    fsize = min(f1, f2)

    icon = ICONS.get(key, icon_mailsave)(c)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 880">
  <defs>
    <linearGradient id="face" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0" stop-color="{c['bg2']}"/>
      <stop offset="1" stop-color="{c['bg1']}"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.14"/>
      <stop offset="0.55" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rim" x1="0" y1="0" x2="0.2" y2="1">
      <stop offset="0" stop-color="{c['line']}"/>
      <stop offset="0.5" stop-color="{c['accent']}"/>
      <stop offset="1" stop-color="{c['bg1']}"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.85"/>
      <stop offset="0.45" stop-color="#ffffff" stop-opacity="0.15"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.35"/>
    </linearGradient>
    <radialGradient id="gloss" cx="0.32" cy="0.16" r="0.72">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.30"/>
      <stop offset="0.55" stop-color="#ffffff" stop-opacity="0.05"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="floor" x1="0" y1="0.55" x2="0" y2="1">
      <stop offset="0" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0.42"/>
    </linearGradient>
    <clipPath id="hexclip"><path d="{hexd}"/></clipPath>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#000" flood-opacity="0.42"/>
    </filter>
    <filter id="innersh" x="-20%" y="-20%" width="140%" height="140%">
      <feOffset dx="0" dy="7"/><feGaussianBlur stdDeviation="9" result="b"/>
      <feComposite in="SourceGraphic" in2="b" operator="out" result="o"/>
      <feColorMatrix in="o" type="matrix"
        values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.55 0"/>
    </filter>
  </defs>

  <!-- 縁（厚み）→ 面 の順に重ねて立体に -->
  <path d="{rimd}" fill="url(#rim)" filter="url(#soft)"/>
  <path d="{hexd}" fill="url(#face)"/>
  <g clip-path="url(#hexclip)">
    <path d="{hexd}" fill="url(#sheen)"/>
    <rect x="0" y="{cy + 224}" width="880" height="220" fill="{c['band']}" opacity="0.94"/>
    <rect x="0" y="{cy + 224}" width="880" height="3" fill="{c['accent']}" opacity="0.9"/>
    <rect x="0" y="0" width="880" height="880" fill="url(#floor)"/>
    <rect x="0" y="0" width="880" height="880" fill="url(#gloss)"/>
    <path d="{hexd}" fill="#fff" filter="url(#innersh)" opacity="0.9"/>
  </g>
  <path d="{hexd}" fill="none" stroke="url(#edge)" stroke-width="5"/>
  <path d="{inid}" fill="none" stroke="{c['line']}" stroke-width="1.6" opacity="0.42"/>

  {icon}

  <g font-family="'Segoe UI Semibold','Segoe UI',sans-serif" text-anchor="middle">
    <text x="{cx}" y="{cy + 52}" font-size="24" letter-spacing="7.5"
          fill="{c['sub']}" font-weight="600">POWER AUTOMATE 45</text>
    <line x1="{cx - 148}" x2="{cx + 148}" y1="{cy + 72}" y2="{cy + 72}"
          stroke="{c['line']}" stroke-width="1.4" opacity="0.5"/>
    <text x="{cx}" y="{cy + 132}" font-size="{fsize}" letter-spacing="1.5"
          fill="{c['text']}" font-weight="700">{l1}</text>
    <text x="{cx}" y="{cy + 132 + fsize + 10}" font-size="{fsize}" letter-spacing="1.5"
          fill="{c['text']}" font-weight="700">{l2}</text>
    <text x="{cx}" y="{cy + 288}" font-size="44" letter-spacing="4"
          fill="{c['accent']}" font-weight="700">VOL.{vol}</text>
    <text x="{cx}" y="{cy + 326}" font-size="22" letter-spacing="4.5"
          fill="{c['sub']}" font-weight="600" opacity="0.9">{date}</text>
  </g>
</svg>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vol", type=int, required=True)
    ap.add_argument("--l1", default=None)
    ap.add_argument("--l2", default=None)
    ap.add_argument("--date", default=None)
    ap.add_argument("--icon", default=None)
    ap.add_argument("--color", default=None, choices=sorted(THEMES))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    l1 = l2 = date = key = None
    if args.vol in SESSIONS:
        l1, l2, date, key = SESSIONS[args.vol]
    l1 = args.l1 or l1
    l2 = args.l2 or l2
    date = args.date or date
    key = args.icon or key or "mailsave"
    if not l1 or not date:
        print("ERROR: --l1 と --date を指定してください")
        sys.exit(1)

    c = THEMES[args.color or VOL_THEME.get(args.vol, "navy")]
    out = args.out or rf"C:\Users\isamu\Documents\pa45\assets\badges\session-{args.vol:03d}\badge.png"
    print("OK:", render(build_svg(args.vol, l1, l2 or "", date, key, c), out))


if __name__ == "__main__":
    main()

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


def build_svg(vol, l1, l2, date, key, c):
    cx, cy = 440, 440
    W, H = 668, 792                      # 六角形の幅・高さ（縦長・上下がとがる）
    hx = [(cx, cy - H / 2), (cx + W / 2, cy - H / 4), (cx + W / 2, cy + H / 4),
          (cx, cy + H / 2), (cx - W / 2, cy + H / 4), (cx - W / 2, cy - H / 4)]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in hx)

    iW, iH = W - 46, H - 54              # 内側の細いライン
    ihx = [(cx, cy - iH / 2), (cx + iW / 2, cy - iH / 4), (cx + iW / 2, cy + iH / 4),
           (cx, cy + iH / 2), (cx - iW / 2, cy + iH / 4), (cx - iW / 2, cy - iH / 4)]
    ipts = " ".join(f"{x:.1f},{y:.1f}" for x, y in ihx)

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
    <clipPath id="hexclip"><polygon points="{pts}"/></clipPath>
    <filter id="soft" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="10" stdDeviation="16" flood-color="#000" flood-opacity="0.38"/>
    </filter>
  </defs>

  <polygon points="{pts}" fill="url(#face)" filter="url(#soft)"/>
  <g clip-path="url(#hexclip)">
    <polygon points="{pts}" fill="url(#sheen)"/>
    <!-- 下部の帯 -->
    <rect x="0" y="{cy + 224}" width="880" height="220" fill="{c['band']}" opacity="0.94"/>
    <rect x="0" y="{cy + 224}" width="880" height="3" fill="{c['accent']}" opacity="0.9"/>
  </g>
  <polygon points="{pts}" fill="none" stroke="{c['accent']}" stroke-width="6"/>
  <polygon points="{ipts}" fill="none" stroke="{c['line']}" stroke-width="1.6" opacity="0.45"/>

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

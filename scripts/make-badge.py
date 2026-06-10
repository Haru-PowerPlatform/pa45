# -*- coding: utf-8 -*-
"""
PA45 参加バッジ画像ジェネレーター v3（Pillow）

スタイリッシュな円形メダル型バッジを生成する。
 - 金属グラデーション + ドロップシャドウ + 光沢で立体感
 - 文字は影＋ハイライトで立体的（エンボス調）
 - 各回のテーマを表すベクターアイコンを中央に配置（軽く陰影付き）
 - 英語表記（POWER AUTOMATE 45 / 英語テーマ名 / VOL.N / 日付）
 - カラーは Vol.14 以降、回ごとに自動で変わる（1〜13 は従来のブルー＆ゴールド）
依存: Pillow のみ

使い方:
  python scripts/make-badge.py --vol 14
  python scripts/make-badge.py --vol 14 --out C:\\Temp\\b14.png   # プレビュー
"""
import argparse
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_BLACK = r"C:\Windows\Fonts\NotoSans-Bold.ttf"
FONT_REG = r"C:\Windows\Fonts\NotoSans-Regular.ttf"

GOLD = (245, 197, 66)
GOLD_D = (176, 124, 18)
SILVER = (226, 232, 240)
SILVER_D = (130, 146, 168)
WHITE = (255, 255, 255)

SS = 3
BASE = 880
S = BASE * SS

# ---- カラーパレット -------------------------------------------------------
# キー: ring_top, ring_bot(外周金属グラデ) / in_c, out_c(内側放射) /
#       accent, accent_d(リム・ノブ・アイコン・リボン) / title / sub
DEFAULT_PAL = dict(ring_top=(125, 185, 255), ring_bot=(16, 38, 92),
                   in_c=(37, 99, 235), out_c=(8, 22, 58),
                   accent=GOLD, accent_d=GOLD_D, title=WHITE, sub=(125, 185, 255))

# Vol.14 以降に巡回適用するパレット
PALETTES = [
    dict(ring_top=(134, 239, 172), ring_bot=(6, 54, 38), in_c=(16, 150, 92),
         out_c=(3, 36, 26), accent=GOLD, accent_d=GOLD_D, title=WHITE, sub=(167, 243, 208)),   # Emerald
    dict(ring_top=(214, 184, 255), ring_bot=(46, 16, 88), in_c=(124, 58, 210),
         out_c=(28, 8, 52), accent=GOLD, accent_d=GOLD_D, title=WHITE, sub=(221, 200, 255)),    # Royal Purple
    dict(ring_top=(254, 178, 178), ring_bot=(86, 12, 22), in_c=(200, 44, 58),
         out_c=(52, 8, 12), accent=GOLD, accent_d=GOLD_D, title=WHITE, sub=(254, 202, 202)),     # Crimson
    dict(ring_top=(153, 246, 228), ring_bot=(8, 58, 58), in_c=(13, 148, 148),
         out_c=(3, 33, 33), accent=SILVER, accent_d=SILVER_D, title=WHITE, sub=(165, 243, 232)),  # Teal/Silver
    dict(ring_top=(254, 215, 170), ring_bot=(104, 42, 8), in_c=(234, 120, 30),
         out_c=(56, 24, 5), accent=(255, 238, 188), accent_d=(176, 120, 32), title=WHITE,
         sub=(254, 220, 180)),                                                                    # Sunset
    dict(ring_top=(249, 196, 233), ring_bot=(86, 14, 66), in_c=(198, 50, 150),
         out_c=(46, 8, 38), accent=GOLD, accent_d=GOLD_D, title=WHITE, sub=(249, 196, 233)),      # Magenta
]

# (英語テーマ名, 日付, アイコンキー)
# ★毎週ルール: アイコンは必ずその週のテーマに合うものにする。
#   既存キーで合うものが無ければ _icon() に新しい図形を描き足す（"gear" フォールバックで済ませない）。
SESSIONS = {
    1:  ("Initialize Variable", "2026-03-06", "init"),
    2:  ("Set Variable", "2026-03-12", "set"),
    3:  ("Condition", "2026-03-26", "cond"),
    4:  ("Apply to Each", "2026-04-02", "loop"),
    5:  ("Fundamentals Week", "2026-04-09", "star"),
    6:  ("Forms to Email", "2026-04-17", "mail"),
    7:  ("Forms to SharePoint", "2026-04-23", "list"),
    8:  ("Approvals", "2026-04-30", "check"),
    9:  ("SharePoint to Teams", "2026-05-07", "chat"),
    10: ("Grand Review", "2026-05-14", "trophy"),
    11: ("Resilient Flow Design", "2026-05-21", "shield"),
    12: ("Expressions", "2026-05-28", "fx"),
    13: ("Try-Catch", "2026-06-04", "trycatch"),
    14: ("Reading JSON", "2026-06-11", "json"),
}


def palette_for(vol):
    return DEFAULT_PAL if vol < 14 else PALETTES[(vol - 14) % len(PALETTES)]


def font(path, size):
    return ImageFont.truetype(path, int(size * SS))


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def vgrad_disc(cx, cy, r, top, bottom):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for y in range(cy - r, cy + r):
        t = (y - (cy - r)) / (2 * r)
        d.line([(cx - r, y), (cx + r, y)], fill=lerp(top, bottom, t))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    layer.putalpha(mask)
    return layer


def radial_disc(cx, cy, r, inner, outer):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    step = max(1, r // 600)
    for rad in range(r, 0, -step):
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=lerp(inner, outer, rad / r))
    return layer


def _spaced(d, cx, cy, txt, fnt, fill, spacing, dx=0, dy=0):
    spacing *= SS
    widths = [fnt.getlength(ch) for ch in txt]
    total = sum(widths) + spacing * (len(txt) - 1)
    x = cx - total / 2 + dx
    for ch, w in zip(txt, widths):
        bb = d.textbbox((0, 0), ch, font=fnt)
        d.text((x, cy - (bb[3] - bb[1]) / 2 - bb[1] + dy), ch, font=fnt, fill=fill)
        x += w + spacing


def text3d(d, cx, cy, txt, fnt, fill, spacing, light=None):
    """影＋（任意で）ハイライトを重ねた立体文字"""
    o = max(2, int(fnt.size * 0.05))
    _spaced(d, cx, cy, txt, fnt, (0, 0, 0, 170), spacing, dx=o, dy=o)
    if light:
        _spaced(d, cx, cy, txt, fnt, light, spacing, dx=-o * 0.5, dy=-o * 0.5)
    _spaced(d, cx, cy, txt, fnt, fill, spacing)


def fit_font(path, txt, max_w, start):
    size = start
    while size > 16:
        f = font(path, size)
        if f.getlength(txt) <= max_w:
            return f
        size -= 1
    return font(path, 16)


# ---- アイコン -------------------------------------------------------------
def _check(d, cx, cy, h, col, w):
    d.line([(cx - h * 0.45, cy + h * 0.05), (cx - h * 0.1, cy + h * 0.4),
            (cx + h * 0.5, cy - h * 0.4)], fill=col, width=w, joint="curve")


def _arrowhead(d, x, y, ang, size, col):
    a1, a2 = ang + math.radians(150), ang - math.radians(150)
    d.polygon([(x, y), (x + size * math.cos(a1), y + size * math.sin(a1)),
               (x + size * math.cos(a2), y + size * math.sin(a2))], fill=col)


def _icon(d, key, cx, cy, size, col):
    h = size / 2
    w = max(2, int(size * 0.085))
    if key == "init":
        d.rounded_rectangle([cx - h * 0.78, cy - h * 0.6, cx + h * 0.78, cy + h * 0.6], radius=h * 0.22, outline=col, width=w)
        d.ellipse([cx - h * 0.18, cy - h * 0.18, cx + h * 0.18, cy + h * 0.18], fill=col)
    elif key == "set":
        d.rounded_rectangle([cx - h * 0.1, cy - h * 0.55, cx + h * 0.8, cy + h * 0.55], radius=h * 0.2, outline=col, width=w)
        d.line([(cx - h * 0.95, cy), (cx - h * 0.18, cy)], fill=col, width=w)
        _arrowhead(d, cx - h * 0.18, cy, 0, h * 0.32, col)
    elif key == "cond":
        dia = [(cx, cy - h * 0.85), (cx + h * 0.62, cy - h * 0.15), (cx, cy + h * 0.55), (cx - h * 0.62, cy - h * 0.15)]
        d.line(dia + [dia[0]], fill=col, width=w, joint="curve")
        d.line([(cx - h * 0.45, cy + h * 0.18), (cx - h * 0.85, cy + h * 0.85)], fill=col, width=w)
        d.line([(cx + h * 0.45, cy + h * 0.18), (cx + h * 0.85, cy + h * 0.85)], fill=col, width=w)
        for sx in (-0.85, 0.85):
            d.ellipse([cx + h * sx - w, cy + h * 0.85 - w, cx + h * sx + w, cy + h * 0.85 + w], fill=col)
    elif key == "loop":
        box = [cx - h * 0.8, cy - h * 0.8, cx + h * 0.8, cy + h * 0.8]
        d.arc(box, start=300, end=210, fill=col, width=w)
        ex, ey = cx + h * 0.8 * math.cos(math.radians(300)), cy + h * 0.8 * math.sin(math.radians(300))
        _arrowhead(d, ex, ey, math.radians(390), h * 0.34, col)
        for dy in (-0.22, 0.04, 0.30):
            d.line([(cx - h * 0.32, cy + h * dy), (cx + h * 0.32, cy + h * dy)], fill=col, width=int(w * 0.8))
    elif key == "star":
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = h if i % 2 == 0 else h * 0.42
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)
    elif key == "mail":
        d.rounded_rectangle([cx - h * 0.9, cy - h * 0.6, cx + h * 0.9, cy + h * 0.6], radius=h * 0.12, outline=col, width=w)
        d.line([(cx - h * 0.9, cy - h * 0.55), (cx, cy + h * 0.12), (cx + h * 0.9, cy - h * 0.55)], fill=col, width=w, joint="curve")
    elif key == "list":
        d.rounded_rectangle([cx - h * 0.65, cy - h * 0.8, cx + h * 0.65, cy + h * 0.8], radius=h * 0.14, outline=col, width=w)
        for dy in (-0.4, -0.05, 0.3):
            d.ellipse([cx - h * 0.42, cy + h * dy - w * 0.9, cx - h * 0.42 + w * 1.8, cy + h * dy + w * 0.9], fill=col)
            d.line([(cx - h * 0.18, cy + h * dy), (cx + h * 0.42, cy + h * dy)], fill=col, width=int(w * 0.8))
    elif key == "check":
        d.ellipse([cx - h * 0.85, cy - h * 0.85, cx + h * 0.85, cy + h * 0.85], outline=col, width=w)
        _check(d, cx, cy, h * 0.95, col, int(w * 1.2))
    elif key == "chat":
        d.rounded_rectangle([cx - h * 0.85, cy - h * 0.75, cx + h * 0.85, cy + h * 0.45], radius=h * 0.25, outline=col, width=w)
        d.polygon([(cx - h * 0.4, cy + h * 0.45), (cx - h * 0.15, cy + h * 0.45), (cx - h * 0.45, cy + h * 0.85)], fill=col)
        for dx in (-0.4, 0, 0.4):
            d.ellipse([cx + h * dx - w, cy - h * 0.18 - w, cx + h * dx + w, cy - h * 0.18 + w], fill=col)
    elif key == "trophy":
        d.polygon([(cx - h * 0.55, cy - h * 0.75), (cx + h * 0.55, cy - h * 0.75), (cx + h * 0.4, cy - h * 0.05), (cx - h * 0.4, cy - h * 0.05)], outline=col, width=w)
        d.arc([cx - h * 0.95, cy - h * 0.72, cx - h * 0.45, cy - h * 0.12], start=90, end=270, fill=col, width=w)
        d.arc([cx + h * 0.45, cy - h * 0.72, cx + h * 0.95, cy - h * 0.12], start=270, end=90, fill=col, width=w)
        d.line([(cx, cy - h * 0.05), (cx, cy + h * 0.4)], fill=col, width=w)
        d.line([(cx - h * 0.4, cy + h * 0.55), (cx + h * 0.4, cy + h * 0.55)], fill=col, width=int(w * 1.3))
    elif key in ("shield", "trycatch"):
        pts = [(cx - h * 0.72, cy - h * 0.7), (cx + h * 0.72, cy - h * 0.7), (cx + h * 0.72, cy + h * 0.05), (cx, cy + h * 0.82), (cx - h * 0.72, cy + h * 0.05)]
        d.line(pts + [pts[0]], fill=col, width=w, joint="curve")
        if key == "trycatch":
            _check(d, cx, cy - h * 0.05, h * 0.8, col, int(w * 1.1))
    elif key == "fx":
        f = font(FONT_BLACK, size * 0.62 / SS)
        bb = d.textbbox((0, 0), "fx", font=f)
        d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), "fx", font=f, fill=col)
    elif key == "json":
        f = font(FONT_BLACK, size * 0.95 / SS)
        for ch, dx in (("{", -0.5), ("}", 0.5)):
            bb = d.textbbox((0, 0), ch, font=f)
            d.text((cx + h * dx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), ch, font=f, fill=col)
        d.ellipse([cx - w, cy - w, cx + w, cy + w], fill=col)
    else:
        d.ellipse([cx - h * 0.55, cy - h * 0.55, cx + h * 0.55, cy + h * 0.55], outline=col, width=w)


def draw_icon(d, key, cx, cy, size, col):
    """影付きアイコン（暗い色をオフセットで先描き→本体）"""
    o = max(2, int(size * 0.03))
    _icon(d, key, cx + o, cy + o, size, (0, 0, 0, 150))
    _icon(d, key, cx, cy, size, col)


# ---- バッジ本体 ----------------------------------------------------------
def make_badge(vol, theme, date, key, out_path):
    p = palette_for(vol)
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cx, cy = S // 2, S // 2
    R = int(S * 0.44)
    ir = int(R * 0.80)

    # ドロップシャドウ
    sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([cx - R, cy - R + int(S * 0.02), cx + R, cy + R + int(S * 0.03)], fill=(0, 0, 0, 150))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(int(S * 0.03))))

    # 外周メタリック
    img.alpha_composite(vgrad_disc(cx, cy, R, p["ring_top"], p["ring_bot"]))

    # 金/銀リム
    d = ImageDraw.Draw(img)
    rim = int(R * 0.86)
    for off, col in ((0, p["accent_d"]), (int(S * 0.006), p["accent"])):
        d.ellipse([cx - rim + off, cy - rim + off, cx + rim - off, cy + rim - off], outline=col, width=int(S * 0.012))

    # ノブ
    kr = int((R + rim) / 2)
    for i in range(36):
        a = 2 * math.pi * i / 36
        kx, ky = cx + kr * math.cos(a), cy + kr * math.sin(a)
        rr = int(S * 0.0075)
        d.ellipse([kx - rr, ky - rr, kx + rr, ky + rr], fill=p["accent"])

    # 内側ディスク
    img.alpha_composite(radial_disc(cx, cy, ir, p["in_c"], p["out_c"]))
    d = ImageDraw.Draw(img)
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], outline=p["accent"], width=int(S * 0.006))

    # 光沢
    gl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(gl).ellipse([cx - R * 0.82, cy - R * 0.95, cx + R * 0.82, cy - R * 0.05], fill=(255, 255, 255, 70))
    gl = gl.filter(ImageFilter.GaussianBlur(int(S * 0.02)))
    glmask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(glmask).ellipse([cx - R, cy - R, cx + R, cy + R], fill=255)
    img.alpha_composite(Image.composite(gl, Image.new("RGBA", (S, S), (0, 0, 0, 0)), glmask))
    d = ImageDraw.Draw(img)

    # ブランド（立体）
    text3d(d, cx, cy - int(ir * 0.68), "POWER AUTOMATE 45", font(FONT_BLACK, 25), p["accent"], 5, light=(255, 255, 255, 60))
    d.line([(cx - ir * 0.46, cy - int(ir * 0.53)), (cx + ir * 0.46, cy - int(ir * 0.53))], fill=(*p["accent"], 180), width=int(S * 0.003))

    # アイコン（陰影付き）
    draw_icon(d, key, cx, cy - int(ir * 0.08), int(ir * 0.64), p["accent"])

    # 英語タイトル（立体・大きめ）
    title = theme.upper()
    f_title = fit_font(FONT_BLACK, title, int(ir * 1.55), 66)
    text3d(d, cx, cy + int(ir * 0.45), title, f_title, p["title"], 2, light=(255, 255, 255, 75))

    # VOL.N ＋ 日付
    text3d(d, cx, cy + int(ir * 0.70), f"VOL.{vol}  ·  {date}", font(FONT_REG, 22), p["sub"], 3)

    out = img.resize((BASE, BASE), Image.LANCZOS)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    out.save(out_path)
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
    key = args.icon or key or "gear"
    if not theme or not date:
        print("ERROR: --theme と --date を指定してください")
        sys.exit(1)

    out = args.out or rf"C:\Users\isamu\Documents\pa45\assets\badges\session-{args.vol:03d}\badge.png"
    print("OK:", make_badge(args.vol, theme, date, key, out))


if __name__ == "__main__":
    main()

"""
PA45 アイキャッチ画像生成スクリプト
使い方:
  python scripts/make-ogp.py --title "1行目\n2行目\n3行目" --label "pill上段" --sub "pill下段" --theme blue --out scripts/ogp-output.png

--theme の選択肢:
  blue   : Power Automate Tips（青）
  orange : PA45 レポート（オレンジ）
  green  : Microsoft 365 活用（緑）
  red    : 登壇・イベント（赤）
  yellow : その他（黄）
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR  = Path(__file__).parent
ROOT_DIR    = SCRIPT_DIR.parent
AVATAR_PATH = ROOT_DIR / "assets" / "img" / "haru-avatar.png"

BOLD_FONTS = [
    Path("C:/Windows/Fonts/YuGothB.ttc"),
    Path("C:/Windows/Fonts/BIZ-UDGothicB.ttc"),
    Path("C:/Windows/Fonts/NotoSansJP-VF.ttf"),
    Path("C:/Windows/Fonts/meiryo.ttc"),
]

W, H = 1200, 630

# ── カラーテーマ定義 ───────────────────────────────────────────────────
# 各キー: (背景左, 背景右, カードボーダー, アバターリング, pill左, pill右)
THEMES = {
    "blue": {
        "bg_left":     (96,  200, 220),   # シアン
        "bg_right":    (26,   58, 143),   # ダークブルー
        "border":      (80,  200, 220),   # 水色
        "av_ring":     (160, 225, 240),   # 薄水色
        "pill_left":   (26,   58, 143),   # ネイビー
        "pill_right":  (59,  130, 246),   # ブルー
    },
    "orange": {
        "bg_left":     (255, 200,  80),   # 明るい黄
        "bg_right":    (194,  65,  12),   # 深いオレンジ
        "border":      (251, 146,  60),   # オレンジ
        "av_ring":     (254, 215, 170),   # 薄オレンジ
        "pill_left":   (154,  52,  18),   # 深茶オレンジ
        "pill_right":  (234,  88,  12),   # オレンジ
    },
    "green": {
        "bg_left":     (110, 231, 183),   # ミントグリーン
        "bg_right":    (6,   95,  70),    # ダークグリーン
        "border":      (52,  211, 153),   # グリーン
        "av_ring":     (167, 243, 208),   # 薄グリーン
        "pill_left":   (6,   78,  59),    # 深グリーン
        "pill_right":  (16,  185, 129),   # エメラルド
    },
    "red": {
        "bg_left":     (252, 165, 165),   # 薄赤
        "bg_right":    (127,  29,  29),   # ダークレッド
        "border":      (248, 113, 113),   # 赤
        "av_ring":     (254, 202, 202),   # 薄ピンク
        "pill_left":   (153,  27,  27),   # 深赤
        "pill_right":  (220,  38,  38),   # 赤
    },
    "yellow": {
        "bg_left":     (253, 230, 138),   # 薄黄
        "bg_right":    (146,  64,  14),   # 琥珀
        "border":      (251, 191,  36),   # 黄色
        "av_ring":     (254, 243, 199),   # 薄黄
        "pill_left":   (120,  53,  15),   # 深琥珀
        "pill_right":  (217, 119,   6),   # アンバー
    },
}


def load_font(size):
    for path in BOLD_FONTS:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size)
            except Exception:
                continue
    return ImageFont.load_default()


def h_gradient(w, h, left, right, radius=0):
    gimg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gimg)
    for x in range(w):
        t = x / max(w - 1, 1)
        color = tuple(int(left[i] + (right[i] - left[i]) * t) for i in range(3)) + (255,)
        draw.line([(x, 0), (x, h)], fill=color)
    if radius > 0:
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
        gimg.putalpha(mask)
    return gimg


def circle_avatar(path, size):
    try:
        av = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
    except Exception:
        av = Image.new("RGBA", (size, size), (180, 200, 220, 255))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    av.putalpha(mask)
    return av


def generate(title: str, label: str, sub: str, theme: str, out: Path):
    t = THEMES.get(theme, THEMES["blue"])

    img = Image.new("RGB", (W, H))
    bg  = h_gradient(W, H, t["bg_left"], t["bg_right"])
    img.paste(bg.convert("RGB"))

    draw = ImageDraw.Draw(img)

    # ─── カード ─────────────────────────────────────────────────
    CM, CR = 26, 22
    draw.rounded_rectangle(
        [CM - 6, CM - 6, W - CM + 6, H - CM + 6],
        radius=CR + 6, fill=t["border"],
    )
    draw.rounded_rectangle(
        [CM, CM, W - CM, H - CM],
        radius=CR, fill=(255, 255, 255),
    )

    # ─── Pill ────────────────────────────────────────────────────
    PX      = 72
    pill_x0 = CM + PX
    pill_y0 = CM + 22
    pill_x1 = W - CM - PX
    pill_y1 = pill_y0 + 186
    pw      = pill_x1 - pill_x0
    ph      = pill_y1 - pill_y0

    pill_img = h_gradient(pw, ph, t["pill_left"], t["pill_right"], radius=ph // 2)
    img.paste(pill_img, (pill_x0, pill_y0), pill_img)

    label_font = load_font(56)
    sub_font   = load_font(54)
    pill_cx    = (pill_x0 + pill_x1) // 2
    draw.text((pill_cx, pill_y0 + 54),  label, font=label_font, fill=(255, 255, 255), anchor="mm")
    draw.text((pill_cx, pill_y0 + 133), sub,   font=sub_font,   fill=(255, 255, 255), anchor="mm")

    # ─── アバター ────────────────────────────────────────────────
    AV_SIZE, AV_RING = 265, 8
    av_x = CM + 28
    av_y = pill_y1 + 16
    draw.ellipse(
        [av_x - AV_RING, av_y - AV_RING,
         av_x + AV_SIZE + AV_RING, av_y + AV_SIZE + AV_RING],
        fill=t["av_ring"],
    )
    av_img = circle_avatar(AVATAR_PATH, AV_SIZE)
    img.paste(av_img, (av_x, av_y), av_img)

    # ─── タイトル ────────────────────────────────────────────────
    lines     = title.replace("\\n", "\n").split("\n")
    text_x    = av_x + AV_SIZE + 28
    text_maxw = W - CM - 20 - text_x

    font_size = 80
    while font_size >= 46:
        tfont  = load_font(font_size)
        max_lw = max(tfont.getbbox(l)[2] - tfont.getbbox(l)[0] for l in lines)
        if max_lw <= text_maxw:
            break
        font_size -= 2

    line_h  = int(font_size * 1.28)
    total_h = len(lines) * line_h
    text_y  = av_y + max(0, (AV_SIZE - total_h) // 2)

    for line in lines:
        draw.text((text_x, text_y), line, font=tfont, fill=(15, 23, 42))
        text_y += line_h

    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out), "PNG")
    print(f"[OK] theme={theme} -> {out}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True)
    p.add_argument("--label", default="Power Automate Tips")
    p.add_argument("--sub",   default="実務で使えるフロー")
    p.add_argument("--theme", default="blue", choices=list(THEMES.keys()),
                   help="blue / orange / green / red / yellow")
    p.add_argument("--out",   default="scripts/ogp-output.png")
    args = p.parse_args()

    generate(
        title=args.title,
        label=args.label,
        sub=args.sub,
        theme=args.theme,
        out=ROOT_DIR / args.out,
    )

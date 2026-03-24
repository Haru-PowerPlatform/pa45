"""
PA45 アイキャッチ画像生成スクリプト
使い方:
  python scripts/make-ogp.py --title "1行目\n2行目\n3行目" --label "社外コミュニティ活動" --sub "Power Automate 45" --out scripts/ogp-output.png
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR  = Path(__file__).parent
ROOT_DIR    = SCRIPT_DIR.parent
AVATAR_PATH = ROOT_DIR / "assets" / "img" / "haru-avatar.png"

# フォント優先順位（太め順）
BOLD_FONTS = [
    Path("C:/Windows/Fonts/YuGothB.ttc"),
    Path("C:/Windows/Fonts/BIZ-UDGothicB.ttc"),
    Path("C:/Windows/Fonts/NotoSansJP-VF.ttf"),
    Path("C:/Windows/Fonts/meiryo.ttc"),
]

W, H = 1200, 630


def load_font(size):
    for path in BOLD_FONTS:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size)
            except Exception:
                continue
    return ImageFont.load_default()


def h_gradient(w, h, left, right, radius=0):
    """横グラデーションのRGBA画像"""
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


def generate(title: str, label: str, sub: str, out: Path):
    # ─── キャンバス ─────────────────────────────────────────────
    img = Image.new("RGB", (W, H))

    # 背景グラデーション（シアン → ダークブルー）
    bg = h_gradient(W, H, (96, 200, 220), (26, 58, 143))
    img.paste(bg.convert("RGB"))

    draw = ImageDraw.Draw(img)

    # ─── カード ─────────────────────────────────────────────────
    CM = 26   # 外周マージン
    CR = 22   # 角丸半径

    # 水色ボーダー
    draw.rounded_rectangle(
        [CM - 6, CM - 6, W - CM + 6, H - CM + 6],
        radius=CR + 6,
        fill=(80, 200, 220),
    )
    # 白カード
    draw.rounded_rectangle(
        [CM, CM, W - CM, H - CM],
        radius=CR,
        fill=(255, 255, 255),
    )

    # ─── Pill（上部ラベル帯）────────────────────────────────────
    PX      = 72          # カード端からの横マージン
    pill_x0 = CM + PX
    pill_y0 = CM + 22
    pill_x1 = W - CM - PX
    pill_y1 = pill_y0 + 186
    pw      = pill_x1 - pill_x0
    ph      = pill_y1 - pill_y0
    pr      = ph // 2     # 完全に丸くする

    pill_img = h_gradient(pw, ph, (26, 58, 143), (59, 130, 246), radius=pr)
    img.paste(pill_img, (pill_x0, pill_y0), pill_img)

    # Pill テキスト（2行、中央揃え）
    label_font = load_font(56)
    sub_font   = load_font(54)
    pill_cx    = (pill_x0 + pill_x1) // 2

    draw.text((pill_cx, pill_y0 + 54),  label, font=label_font,
              fill=(255, 255, 255), anchor="mm")
    draw.text((pill_cx, pill_y0 + 133), sub,   font=sub_font,
              fill=(255, 255, 255), anchor="mm")

    # ─── アバター ────────────────────────────────────────────────
    AV_SIZE  = 265
    AV_RING  = 8
    av_x     = CM + 28
    av_y     = pill_y1 + 16

    # 水色リング
    draw.ellipse(
        [av_x - AV_RING, av_y - AV_RING,
         av_x + AV_SIZE + AV_RING, av_y + AV_SIZE + AV_RING],
        fill=(160, 225, 240),
    )
    av_img = circle_avatar(AVATAR_PATH, AV_SIZE)
    img.paste(av_img, (av_x, av_y), av_img)

    # ─── タイトル ────────────────────────────────────────────────
    lines    = title.replace("\\n", "\n").split("\n")
    text_x   = av_x + AV_SIZE + 28
    text_maxw = W - CM - 20 - text_x

    # フォントサイズ自動調整（80px → 最小46px）
    font_size = 80
    while font_size >= 46:
        tfont = load_font(font_size)
        max_lw = max(tfont.getbbox(l)[2] - tfont.getbbox(l)[0] for l in lines)
        if max_lw <= text_maxw:
            break
        font_size -= 2

    line_h  = int(font_size * 1.28)
    total_h = len(lines) * line_h

    # 縦方向をアバター範囲に合わせて中央寄せ
    text_y = av_y + max(0, (AV_SIZE - total_h) // 2)

    for line in lines:
        draw.text((text_x, text_y), line, font=tfont, fill=(15, 23, 42))
        text_y += line_h

    # ─── 出力 ────────────────────────────────────────────────────
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out), "PNG")
    print(f"[OK] {out}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True, help="タイトル（\\nで改行）")
    p.add_argument("--label", default="社外コミュニティ活動", help="pill 1行目")
    p.add_argument("--sub",   default="Power Automate 45",    help="pill 2行目")
    p.add_argument("--out",   default="scripts/ogp-output.png")
    args = p.parse_args()

    generate(
        title=args.title,
        label=args.label,
        sub=args.sub,
        out=ROOT_DIR / args.out,
    )

"""
PA45 connpass アイキャッチ生成スクリプト（詳細デザイン版）
使い方:
  python scripts/make-connpass-eyecatch.py --vol 7 \
    --title "Forms申請をSharePointに自動登録" \
    --sub "Forms × SharePoint × Teams" \
    --sub2 "（申請から通知まで全自動）" \
    --theme-text "Formsの申請をSharePointリストに自動登録する" \
    --out assets/ogp/pa45-vol7-connpass.png
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
REG_FONTS = [
    Path("C:/Windows/Fonts/YuGothM.ttc"),
    Path("C:/Windows/Fonts/BIZ-UDGothicR.ttc"),
    Path("C:/Windows/Fonts/NotoSansJP-VF.ttf"),
    Path("C:/Windows/Fonts/meiryo.ttc"),
]

W, H = 1200, 630


def load_font(size, bold=True):
    fonts = BOLD_FONTS if bold else REG_FONTS
    for path in fonts:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size)
            except Exception:
                continue
    return ImageFont.load_default()


def h_gradient_paste(img, x0, y0, x1, y1, radius, left_color, right_color):
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0:
        return
    grad = Image.new("RGBA", (w, h))
    draw = ImageDraw.Draw(grad)
    for x in range(w):
        t = x / max(w - 1, 1)
        c = tuple(int(left_color[i] + (right_color[i] - left_color[i]) * t) for i in range(3)) + (255,)
        draw.line([(x, 0), (x, h)], fill=c)
    if radius > 0:
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
        grad.putalpha(mask)
    img.paste(grad, (x0, y0), grad)


def circle_avatar(path, size):
    try:
        av = Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)
    except Exception:
        av = Image.new("RGBA", (size, size), (150, 200, 230, 255))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    av.putalpha(mask)
    return av


def text_w(draw, text, font):
    return draw.textlength(text, font=font)


def generate(vol, title, sub, sub2, theme_text, target_text, time_text, out):
    # ── Canvas ──────────────────────────────────────────────────
    img = Image.new("RGB", (W, H), (232, 238, 252))   # light lavender bg
    draw = ImageDraw.Draw(img)

    # ── Card shadow + card ──────────────────────────────────────
    CM, CR = 20, 22
    draw.rounded_rectangle([CM + 4, CM + 4, W - CM + 4, H - CM + 4],
                            radius=CR + 4, fill=(195, 210, 240))
    draw.rounded_rectangle([CM, CM, W - CM, H - CM],
                            radius=CR, fill=(255, 255, 255),
                            outline=(191, 219, 254), width=2)

    # ── Top badge row ────────────────────────────────────────────
    BY = CM + 28          # badge top y
    BH = 54               # badge height

    # Left: "Power Automate 入門講座" (gradient pill)
    badge_font = load_font(26, bold=True)
    badge_label = "Power Automate 入門講座"
    bw = int(text_w(draw, badge_label, badge_font)) + 44
    h_gradient_paste(img, CM + 28, BY, CM + 28 + bw, BY + BH,
                     BH // 2, (37, 99, 235), (109, 40, 217))
    draw.text((CM + 28 + bw // 2, BY + BH // 2),
              badge_label, font=badge_font, fill=(255, 255, 255), anchor="mm")

    # Right: "Vol.N" (gray pill)
    vol_font = load_font(30, bold=True)
    vol_label = f"Vol.{vol}"
    vw = int(text_w(draw, vol_label, vol_font)) + 40
    vx0 = W - CM - 28 - vw
    draw.rounded_rectangle([vx0, BY, W - CM - 28, BY + BH],
                            radius=BH // 2, fill=(226, 232, 240))
    draw.text((vx0 + vw // 2, BY + BH // 2),
              vol_label, font=vol_font, fill=(55, 65, 81), anchor="mm")

    # PA icon (rounded square, blue-indigo) at far right
    icon_r = 24
    icon_cx = W - CM - 28 - vw - 18 - icon_r
    icon_cy = BY + BH // 2
    draw.rounded_rectangle([icon_cx - icon_r, icon_cy - icon_r,
                             icon_cx + icon_r, icon_cy + icon_r],
                            radius=8, fill=(99, 102, 241))
    icon_font = load_font(18, bold=True)
    draw.text((icon_cx, icon_cy), "PA",
              font=icon_font, fill=(255, 255, 255), anchor="mm")

    # ── PA45 + 【第N回】 ─────────────────────────────────────────
    R2Y = BY + BH + 20
    pa45_font = load_font(74, bold=True)
    kai_font  = load_font(60, bold=True)

    pa45_text = "PA45"
    kai_text  = f"【第{vol}回】"
    draw.text((CM + 36, R2Y), pa45_text, font=pa45_font, fill=(37, 99, 235))
    pw = int(text_w(draw, pa45_text, pa45_font))
    draw.text((CM + 36 + pw + 28, R2Y + 8), kai_text, font=kai_font, fill=(15, 23, 42))

    # ── Main title ───────────────────────────────────────────────
    R3Y = R2Y + 84
    title_full = f"第{vol}回：{title}"
    max_title_w = W - CM * 2 - 60
    fs = 52
    while fs >= 32:
        tf = load_font(fs, bold=True)
        if int(text_w(draw, title_full, tf)) <= max_title_w:
            break
        fs -= 2
    title_font = load_font(fs, bold=True)
    draw.text((CM + 36, R3Y), title_full, font=title_font, fill=(15, 23, 42))

    # ── Subtitle (2 lines) ───────────────────────────────────────
    R4Y = R3Y + fs + 18
    sub_font = load_font(32, bold=False)
    draw.text((CM + 36, R4Y), sub, font=sub_font, fill=(55, 65, 81))
    R5Y = R4Y + 40
    draw.text((CM + 36, R5Y), sub2, font=sub_font, fill=(75, 85, 99))

    # ── Info box with left blue border ───────────────────────────
    INFO_Y = R5Y + 48
    INFO_H = 108
    # Left blue accent bar
    draw.rectangle([CM + 36, INFO_Y, CM + 41, INFO_Y + INFO_H], fill=(59, 130, 246))

    lbl_font = load_font(24, bold=True)
    val_font = load_font(24, bold=False)

    rows = [
        ("Theme",  theme_text),
        ("Target", target_text),
        ("Time",   time_text),
    ]
    # Compute max label width for alignment
    max_lbl_w = max(int(text_w(draw, r[0], lbl_font)) for r in rows) + 20

    iy = INFO_Y + 6
    for lbl, val in rows:
        draw.text((CM + 54, iy), lbl,  font=lbl_font, fill=(156, 163, 175))
        draw.text((CM + 54 + max_lbl_w, iy), val, font=val_font, fill=(75, 85, 99))
        iy += 36

    # ── Avatar (bottom right) ────────────────────────────────────
    AV = 215
    av_ring = 8
    av_x = W - CM - 30 - AV
    av_y = H - CM - 30 - AV
    draw.ellipse([av_x - av_ring, av_y - av_ring,
                  av_x + AV + av_ring, av_y + AV + av_ring],
                 fill=(186, 230, 253))
    av_img = circle_avatar(AVATAR_PATH, AV)
    img.paste(av_img, (av_x, av_y), av_img)

    # ── "A" badge (next to avatar, lower left of it) ────────────
    a_size = 52
    ax = av_x - a_size - 12
    ay = av_y + AV - a_size
    draw.rounded_rectangle([ax, ay, ax + a_size, ay + a_size],
                            radius=12, fill=(99, 102, 241))
    a_font = load_font(28, bold=True)
    draw.text((ax + a_size // 2, ay + a_size // 2), "A",
              font=a_font, fill=(255, 255, 255), anchor="mm")

    # ── Bottom bar ────────────────────────────────────────────────
    BAR_H = 42
    BAR_Y = H - CM - 12 - BAR_H
    draw.rounded_rectangle([CM + 10, BAR_Y, W - CM - 10, BAR_Y + BAR_H],
                            radius=BAR_H // 2, fill=(219, 234, 254))
    bar_font = load_font(21, bold=False)
    bar_text = "学んだこと・気づいたことを #PA45 でリアルタイムに投稿しよう！スクショOK！"
    bar_text_w = int(text_w(draw, bar_text, bar_font))
    # Draw small circle icon before text
    icon_d = 18
    bar_cx = (W - bar_text_w) // 2 - icon_d - 10
    bar_cy = BAR_Y + BAR_H // 2
    draw.ellipse([bar_cx - icon_d, bar_cy - icon_d,
                  bar_cx + icon_d, bar_cy + icon_d], fill=(59, 130, 246))
    draw.text(((W - bar_text_w) // 2, BAR_Y + BAR_H // 2),
              bar_text, font=bar_font, fill=(29, 78, 216), anchor="lm")

    # ── Save ─────────────────────────────────────────────────────
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(out), "PNG")
    print(f"[OK] -> {out}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--vol",         type=int, required=True)
    p.add_argument("--title",       required=True)
    p.add_argument("--sub",         default="Forms × SharePoint × Teams")
    p.add_argument("--sub2",        default="（申請から通知まで全自動）")
    p.add_argument("--theme-text",  default="Power Automateで業務を自動化する")
    p.add_argument("--target-text", default="はじめての方（プログラミング知識ゼロでOK)")
    p.add_argument("--time-text",   default="約10分ハンズオン")
    p.add_argument("--out",         default="assets/ogp/pa45-connpass.png")
    args = p.parse_args()

    generate(
        vol         = args.vol,
        title       = args.title,
        sub         = args.sub,
        sub2        = args.sub2,
        theme_text  = args.theme_text,
        target_text = args.target_text,
        time_text   = args.time_text,
        out         = ROOT_DIR / args.out,
    )

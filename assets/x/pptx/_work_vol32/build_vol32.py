# -*- coding: utf-8 -*-
"""Vol.32 メール添付ファイル自動保存 1枚スライド
   デザインシステム準拠版（Noto Sans JP / Tailwind配色 / 太字既定 / F8F9FAカード+色枠 / 画像アイコン）
   ※reference_x_tips_design_system.md の仕様に従う。以降の雛形。"""
import os, math, random
random.seed(7)
HAND = "Zen Kurenaido"   # 手書き風フォント（手作り感）
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---- Tailwind palette ----
BLUE      = RGBColor(0x25, 0x63, 0xEB)  # blue-600
BLUE_DK   = RGBColor(0x1E, 0x40, 0xAF)  # blue-800
BLUE_BG   = RGBColor(0xEF, 0xF6, 0xFF)  # blue-50
GREEN     = RGBColor(0x16, 0xA3, 0x4A)  # green-600
GREEN_DK  = RGBColor(0x06, 0x4E, 0x3B)  # green-900
GREEN_BG  = RGBColor(0xEC, 0xFD, 0xF5)  # green-50
RED       = RGBColor(0xDC, 0x26, 0x26)  # red-600
ENJI      = RGBColor(0xA4, 0x28, 0x3C)  # 臙脂（深い赤）アクセント
ENJI_DK   = RGBColor(0x6E, 0x16, 0x28)  # 濃い臙脂
CARD      = RGBColor(0xF8, 0xF9, 0xFA)  # gray-50-ish card bg
GREYTX    = RGBColor(0x4B, 0x55, 0x63)  # gray-600 body
GREYMUT   = RGBColor(0x6B, 0x72, 0x80)  # gray-500
DARK      = RGBColor(0x11, 0x18, 0x27)  # gray-900 code band
DARK2     = RGBColor(0x1F, 0x29, 0x37)  # gray-800
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
LGREY     = RGBColor(0xE5, 0xE7, 0xEB)  # gray-200
CODEFG    = RGBColor(0xF1, 0xF5, 0xF9)
FONT = "Noto Sans JP"

ICON = r"C:\Users\isamu\Documents\pa45\assets\x\pptx\_assets\icons"
IRAS = r"C:\Users\isamu\Documents\pa45\assets\x\pptx\_assets\irasutoya"
CHARA = r"C:\Users\isamu\Documents\pa45\assets\x\pptx\_assets\chara"
RIRO  = r"C:\Users\isamu\Documents\pa45\assets\x\pptx\_assets\riro"
SHOTS = r"C:\Users\isamu\Documents\pa45\assets\x\pptx\_work_vol32\shots"

def circle_png(src):
    """角を透明にした円形PNGを作って返す（dark帯でも白角が出ない）"""
    if not os.path.exists(src): return None
    out = src.rsplit(".",1)[0] + "_circle.png"
    try:
        from PIL import Image, ImageDraw
        im = Image.open(src).convert("RGBA")
        s = min(im.size); im = im.crop((0,0,s,s))
        mask = Image.new("L", (s,s), 0)
        ImageDraw.Draw(mask).ellipse((0,0,s,s), fill=255)
        im.putalpha(mask); im.save(out); return out
    except Exception:
        return src

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
slide = prs.slides.add_slide(prs.slide_layouts[6])
shp = slide.shapes

def rect(x, y, w, h, fill, line=None, lw=1.0, rounded=False, radius=0.08):
    s = shp.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line; s.line.width = Pt(lw)
    s.shadow.inherit = False
    if rounded:
        try: s.adjustments[0] = radius
        except Exception: pass
    return s

def txt(x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
        space=Pt(2), wrap=True):
    tb = shp.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = wrap; tf.vertical_anchor = anchor
    tf.margin_left = Pt(4); tf.margin_right = Pt(4)
    tf.margin_top = Pt(1); tf.margin_bottom = Pt(1)
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = space; p.space_before = Pt(0)
        for (t, sz, b, col, *fnt) in para:
            r = p.add_run(); r.text = t
            r.font.size = Pt(sz); r.font.bold = b
            r.font.color.rgb = col; r.font.name = fnt[0] if fnt else FONT
    return tb

def pic(path, x, y, h=None, w=None):
    if not os.path.exists(path): return None
    kw = {}
    if h: kw["height"] = Inches(h)
    if w: kw["width"] = Inches(w)
    return shp.add_picture(path, Inches(x), Inches(y), **kw)

def pic_rot(path, x, y, w, rot):
    if not os.path.exists(path): return None
    p = shp.add_picture(path, Inches(x), Inches(y), width=Inches(w)); p.rotation = rot; return p

def chip(x, y, w, h, fill, text, sz=16):
    rect(x, y, w, h, fill, rounded=True, radius=0.28)
    txt(x, y, w, h, [[(text, sz, True, WHITE)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ---- 手描き風（freeform）注釈 ----
def hand_stroke(points, color, lw=3.0, close=False):
    fb = shp.build_freeform(points[0][0], points[0][1], scale=Emu(914400))
    fb.add_line_segments(points[1:], close=close)
    s = fb.convert_to_shape()
    s.fill.background(); s.line.color.rgb = color; s.line.width = Pt(lw); s.shadow.inherit = False
    return s

def hand_underline(x0, x1, y, color, lw=3.5, amp=0.028, seg=20):
    pts=[]
    for i in range(seg+1):
        t=i/seg
        yy=y+math.sin(t*math.pi*3.2)*amp + random.uniform(-0.012,0.012)
        pts.append((x0+(x1-x0)*t, yy))
    hand_stroke(pts, color, lw)

def hand_circle(cx, cy, rx, ry, color, lw=3.2, seg=48):
    start=random.uniform(-0.5,-0.1); pts=[]
    for i in range(seg+1):
        t=start+(i/seg)*(2*math.pi+0.55)   # 描き過ぎ＝手書きっぽさ
        wob=1+0.09*math.sin(t*2.7+1.3)+random.uniform(-0.05,0.05)
        pts.append((cx+math.cos(t)*rx*wob,
                    cy+math.sin(t)*ry*wob))
    hand_stroke(pts, color, lw)

# ===== 1) Title bar (2563EB + white outline) =====
rect(0, 0, 13.333, 0.92, BLUE, line=WHITE, lw=1.25)
rect(0.18, 0.17, 1.5, 0.58, WHITE, rounded=True, radius=0.5)
txt(0.18, 0.18, 1.5, 0.55, [[("Vol.32", 24, True, BLUE)]],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
_TITLE = "Power Automate：メールの添付を自動で保存する方法"
txt(1.88, 0.12, 9.9, 0.78, [[(_TITLE, 25, True, BLUE_DK)]], anchor=MSO_ANCHOR.MIDDLE)  # 影
txt(1.85, 0.08, 9.9, 0.78, [[(_TITLE, 25, True, WHITE)]], anchor=MSO_ANCHOR.MIDDLE)     # 本体
# 右上マスコットは最後に描画して最前面に（下部で配置）

# ===== 2) 結論 bar =====
rect(0, 0.92, 13.333, 0.72, BLUE_BG)
pic(os.path.join(ICON, "pa_logo.png"), 0.22, 1.03, h=0.5)
txt(0.86, 0.94, 12.3, 0.68,
    [[("結論　", 18, True, BLUE),
      ("必要な添付だけを、届いた瞬間に自動でフォルダへ。手作業のダウンロード&保存はもうしない。", 16.5, True, DARK2)]],
    anchor=MSO_ANCHOR.MIDDLE)

COL_Y = 1.80
COL_H = 4.04

# ===== 3) Left card : こんな時に効く？ =====
rect(0.20, COL_Y, 3.70, COL_H, CARD, line=ENJI, lw=2.0, rounded=True, radius=0.05)
chip(1.05, COL_Y+0.12, 2.00, 0.46, ENJI, "こんな時に効く？", sz=15)
checks = [
    "請求書や注文書を毎回手で保存している",
    "添付の保存先がバラバラで探せない",
    "保存し忘れ・取りこぼしをなくしたい",
]
cy = COL_Y + 0.78
for c in checks:
    txt(0.30, cy-0.03, 0.40, 0.72, [[("✓", 17, True, ENJI)]], anchor=MSO_ANCHOR.MIDDLE)
    txt(0.70, cy-0.03, 3.08, 0.74, [[(c, 16, True, GREYTX)]])
    cy += 0.84
rect(0.40, COL_Y+COL_H-0.84, 3.30, 0.70, WHITE, line=ENJI, lw=1.25, rounded=True, radius=0.1)
txt(0.52, COL_Y+COL_H-0.80, 3.10, 0.62,
    [[("Point　", 13.5, True, ENJI), ("狙いは“届いた瞬間に仕分け”", 13.5, True, GREYTX)],
     [("―探す時間をゼロにする", 12, False, GREYMUT)]], space=Pt(1))
# 左カード上部に「困り顔」マスコット（=悩みの可視化）
pic(os.path.join(CHARA, "chara_trouble.png"), 3.02, COL_Y-0.18, h=1.02)

# ===== 4) Center : PA アクションカード風（実画面の再現） =====
CX, CW = 4.05, 5.08
TITLEC = RGBColor(0x1F, 0x29, 0x37)
chip(CX+1.05, COL_Y+0.04, CW-2.10, 0.50, BLUE, "実際のフロー（3アクション）", sz=15)

def pa_card(y, h, no, iconfile, title, sub, accent):
    # Power Automate のアクションカードを忠実に：白い角丸長方形＋左に本物アイコン＋中にアクション名
    rect(CX+0.15, y, CW-0.30, h, WHITE, line=LGREY, lw=1.25, rounded=True, radius=0.08)
    iy = y+(h-0.56)/2
    pic(os.path.join(ICON, iconfile), CX+0.30, iy, w=0.56)   # 本物アイコン（PA画面から切り出し）
    txt(CX+1.02, y+0.05, CW-1.50, h-0.08,
        [[(no+" ", 12, True, accent), (title, 14.5, True, TITLEC)],
         [(sub, 11, False, GREYMUT)]], space=Pt(2), anchor=MSO_ANCHOR.MIDDLE)
    txt(CX+CW-0.50, y, 0.30, h, [[("⋮", 16, True, RGBColor(0xA6,0xAE,0xBA))]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

def connector(y):
    cxm = CX+CW/2
    ln = shp.add_shape(MSO_SHAPE.RECTANGLE, Inches(cxm-0.013), Inches(y), Inches(0.026), Inches(0.26))
    ln.fill.solid(); ln.fill.fore_color.rgb = RGBColor(0xC2,0xC9,0xD6); ln.line.fill.background(); ln.shadow.inherit=False
    o = shp.add_shape(MSO_SHAPE.OVAL, Inches(cxm-0.115), Inches(y+0.02), Inches(0.23), Inches(0.23))
    o.fill.solid(); o.fill.fore_color.rgb = BLUE; o.line.color.rgb = WHITE; o.line.width=Pt(1); o.shadow.inherit=False
    txt(cxm-0.115, y+0.005, 0.23, 0.23, [[("＋", 11, True, WHITE)]],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 本物アイコン（PA画面から切り出し）を使用
y = COL_Y + 0.64
pa_card(y, 0.76, "①", "pa_outlook.png", "新しいメールが届いたとき", "Office 365 Outlook・添付あり", BLUE)
connector(y+0.78)
y2 = y + 1.06
pa_card(y2, 0.76, "②", "pa_control.png", "条件（Condition）", "件名に「請求書」を含む", BLUE)
connector(y2+0.78)
y3 = y2 + 1.06
pa_card(y3, 0.80, "③", "pa_sharepoint.png", "ファイルの作成", "SharePoint / OneDrive へ保存", GREEN)
txt(CX, y3+0.84, CW, 0.30,
    [[("→ 年月フォルダへ自動で振り分け", 13, True, GREEN)]],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ===== 5) Right card : 実務でこう使う =====
RX, RW = 9.25, 3.90
rect(RX, COL_Y, RW, COL_H, CARD, line=GREEN, lw=2.0, rounded=True, radius=0.05)
chip(RX+0.95, COL_Y+0.12, 2.00, 0.46, GREEN, "実務でこう使う", sz=15)
pins = [
    "請求書を取引先フォルダへ自動保存",
    "申込書を SharePoint に集約",
    "保存と同時に Teams で受領通知",
]
py = COL_Y + 0.78
for p in pins:
    pic(os.path.join(ICON, "icon_check_blue.png"), RX+0.18, py+0.02, h=0.26)
    txt(RX+0.50, py-0.03, RW-0.64, 0.74, [[(p, 15.5, True, GREYTX)]])
    py += 0.80
rect(RX+0.18, COL_Y+COL_H-0.92, RW-0.36, 0.78, GREEN_BG, line=GREEN, lw=1.5, rounded=True, radius=0.1)
pic(os.path.join(CHARA, "chara_guts.png"), RX+0.16, COL_Y+COL_H-1.06, h=0.98)
txt(RX+0.92, COL_Y+COL_H-0.94, RW-1.05, 0.82,
    [[("メリット　", 12.5, True, GREEN), ("保存作業 毎回15分 → ", 13, True, GREEN_DK), ("0分", 17, True, GREEN_DK)],
     [("探す手間・保存もれもゼロに", 12.5, True, GREEN_DK)]],
    anchor=MSO_ANCHOR.MIDDLE, space=Pt(1))

# ===== 6) Bottom dark band : フロー構成 =====
BY = 5.98
rect(0, BY, 13.333, 1.52, DARK)
rect(0, BY, 0.16, 1.52, BLUE)
# 左下：中の人マスコット（笑顔・署名的に）
pic(os.path.join(CHARA, "chara_smile.png"), 0.14, BY+0.06, h=1.44)
LX = 1.35
txt(LX, BY+0.10, 5.6, 0.42, [[("フロー構成（組む順番）", 18, True, WHITE)]])
txt(LX, BY+0.56, 7.3, 0.88,
    [[("① Outlook：新しいメール受信（添付ファイルあり）", 14, True, CODEFG)],
     [("② 条件：件名に「請求書」を含む 等で絞り込み", 14, True, CODEFG)],
     [("③ 保存：SharePoint / OneDrive にファイル作成", 14, True, CODEFG)]],
    space=Pt(2))
rect(9.05, BY+0.28, 4.05, 0.94, DARK2, line=BLUE, lw=1.25, rounded=True, radius=0.12)
txt(9.15, BY+0.32, 3.85, 0.86,
    [[("覚え方", 14, True, RGBColor(0x9D,0xC2,0xFF))],
     [("「届いたら・選んで・しまう」", 15, True, WHITE)],
     [("の3ステップだけ", 14, True, WHITE)]],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space=Pt(1))

# ===== 最前面：右上マスコット（大きめ・PC作業） =====
pic(os.path.join(CHARA, "chara_laptop.png"), 12.00, -0.14, h=2.02)

out = r"C:\Users\isamu\Documents\pa45\assets\x\pptx\未投稿\vol32.pptx"
prs.save(out)
print("saved:", out)

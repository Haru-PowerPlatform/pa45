# -*- coding: utf-8 -*-
"""Vol.32 イントロ（1枚目）：先生はる × 生徒リロ の会話で導入"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BLUE=RGBColor(0x25,0x63,0xEB); BLUE_DK=RGBColor(0x1E,0x40,0xAF); BLUE_BG=RGBColor(0xEF,0xF6,0xFF)
GREEN=RGBColor(0x16,0xA3,0x4A); ENJI=RGBColor(0xA4,0x28,0x3C)
GREYTX=RGBColor(0x33,0x3A,0x46); DARK=RGBColor(0x11,0x18,0x27)
WHITE=RGBColor(0xFF,0xFF,0xFF); LGREY=RGBColor(0xE5,0xE7,0xEB)
FONT="Noto Sans JP"
CHARA=r"C:\Users\isamu\Documents\pa45\assets\x\pptx\_assets\chara"
RIRO=r"C:\Users\isamu\Documents\pa45\assets\x\pptx\_assets\riro"

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
slide=prs.slides.add_slide(prs.slide_layouts[6]); shp=slide.shapes

def rect(x,y,w,h,fill,line=None,lw=1.0,rounded=False,radius=0.08):
    s=shp.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                    Inches(x),Inches(y),Inches(w),Inches(h))
    if fill is None: s.fill.background()
    else: s.fill.solid(); s.fill.fore_color.rgb=fill
    if line is None: s.line.fill.background()
    else: s.line.color.rgb=line; s.line.width=Pt(lw)
    s.shadow.inherit=False
    if rounded:
        try: s.adjustments[0]=radius
        except: pass
    return s

def txt(x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=Pt(2),wrap=True):
    tb=shp.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame
    tf.word_wrap=wrap; tf.vertical_anchor=anchor
    tf.margin_left=Pt(6); tf.margin_right=Pt(6); tf.margin_top=Pt(2); tf.margin_bottom=Pt(2)
    for i,para in enumerate(runs):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.space_after=space; p.space_before=Pt(0)
        for (t,sz,b,col) in para:
            r=p.add_run(); r.text=t; r.font.size=Pt(sz); r.font.bold=b; r.font.color.rgb=col; r.font.name=FONT
    return tb

def pic(path,x,y,h=None,w=None):
    if not os.path.exists(path): return
    kw={}
    if h:kw["height"]=Inches(h)
    if w:kw["width"]=Inches(w)
    shp.add_picture(path,Inches(x),Inches(y),**kw)

def tail(x,y,rot,fill):
    t=shp.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE,Inches(x),Inches(y),Inches(0.28),Inches(0.26))
    t.fill.solid(); t.fill.fore_color.rgb=fill; t.line.fill.background(); t.shadow.inherit=False
    t.rotation=rot

def bubble(bx,by,bw,bh,border,side,who,whocol,lines):
    rect(bx,by,bw,bh,WHITE,line=border,lw=2.0,rounded=True,radius=0.12)
    if side=="left":  tail(bx-0.12, by+bh/2-0.13, 270, border)
    else:             tail(bx+bw-0.16, by+bh/2-0.13, 90, border)
    runs=[[(who+"　", 13, True, whocol)]+[(lines[0], 16.5, True, GREYTX)]]
    for ln in lines[1:]:
        runs.append([(ln, 16.5, True, GREYTX)])
    txt(bx+0.2, by+0.08, bw-0.4, bh-0.16, runs, anchor=MSO_ANCHOR.MIDDLE, space=Pt(2))

# ===== Title bar =====
rect(0,0,13.333,0.92,BLUE,line=WHITE,lw=1.25)
rect(0.18,0.17,1.5,0.58,WHITE,rounded=True,radius=0.5)
txt(0.18,0.18,1.5,0.55,[[("Vol.32",24,True,BLUE)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
_T="メールの添付、まだ手で保存してませんか？"
txt(1.90,0.12,10.0,0.78,[[(_T,24,True,BLUE_DK)]],anchor=MSO_ANCHOR.MIDDLE)
txt(1.87,0.08,10.0,0.78,[[(_T,24,True,WHITE)]],anchor=MSO_ANCHOR.MIDDLE)
# はじめにタグ
rect(11.55,0.26,1.55,0.42,BLUE_DK,rounded=True,radius=0.4)
txt(11.55,0.27,1.55,0.40,[[("はじめに",13,True,WHITE)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)

# ===== 会話 3ターン =====
# Turn1: リロ（困り）左
pic(os.path.join(RIRO,"riro_trouble.png"),0.30,1.18,h=1.66)
bubble(2.15,1.34,10.85,1.34,ENJI,"left","リロ",ENJI,
       ["先生、メールで届く請求書…毎回ダウンロードして手で保存してるんですけど、",
        "正直、地味にしんどいです…"])
# Turn2: はる（先生）右
pic(os.path.join(CHARA,"chara_point.png"),11.35,3.02,h=1.66)
bubble(0.30,3.18,10.75,1.34,BLUE,"right","はる先生",BLUE,
       ["あるあるだね。それ、Power Automate で “自動保存” にすると、",
        "もう自分で触らなくてよくなるよ。"])
# Turn3: リロ（喜び）左
pic(os.path.join(RIRO,"riro_happy.png"),0.30,4.86,h=1.62)
bubble(2.15,5.04,10.85,1.20,GREEN,"left","リロ",GREEN,
       ["えっ、やってみたいです！ どう作るんですか？"])

# ===== Footer =====
rect(0,6.62,13.333,0.88,DARK)
rect(0,6.62,0.16,0.88,BLUE)
txt(0.45,6.62,12.6,0.88,
    [[("→ 実際のフロー（作り方）は ", 17, True, WHITE),
      ("次の1枚", 17, True, RGBColor(0x7D,0xB0,0xFF)),
      (" で公開！", 17, True, WHITE)]],
    anchor=MSO_ANCHOR.MIDDLE)

out=r"C:\Users\isamu\Documents\pa45\assets\x\pptx\未投稿\vol32_00_intro.pptx"
prs.save(out); print("saved:",out)

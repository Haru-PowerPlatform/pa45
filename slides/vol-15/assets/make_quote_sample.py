# -*- coding: utf-8 -*-
"""PA45 Vol.15 用 サンプル御見積書PDF（受講生も使える汎用テンプレート）"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# 日本語フォントを埋め込み（どのビューアでも表示されるように）
pdfmetrics.registerFont(TTFont("JP", r"C:\Windows\Fonts\meiryo.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("JPB", r"C:\Windows\Fonts\meiryob.ttc", subfontIndex=0))
G = "JPB"  # 見出し・強調（ボールド）
M = "JP"   # 本文（レギュラー）

NAVY = HexColor("#1f3864")
BLUE = HexColor("#2563eb")
LIGHT = HexColor("#eef3fb")
GRAY = HexColor("#666666")
LINE = HexColor("#c9d3e6")

OUT = r"C:\Users\isamu\Documents\pa45\slides\vol-15\assets\見積書_サンプル.pdf"
W, H = A4

# ---- 見積データ（受講生はここを書き換えるだけ） -------------------
issuer = {
    "company": "サンプル商事株式会社",
    "zip": "〒100-0001",
    "addr": "東京都千代田区サンプル1-2-3 サンプルビル5F",
    "tel": "TEL: 03-1234-5678 / FAX: 03-1234-5679",
    "person": "営業部　見本 太郎",
}
customer = "〇〇株式会社"
quote_no = "Q-2026-0618"
issue_date = "2026年6月18日"
expire = "発行日より30日間"
subject = "オフィス備品・サービス 一式"
items = [
    ("ノートPC（標準モデル）", 2, "台", 98000),
    ("モニター 24インチ", 2, "台", 18000),
    ("セットアップ・初期設定", 1, "式", 25000),
    ("保守サポート（年間）", 1, "式", 30000),
]
TAX_RATE = 0.10
# ------------------------------------------------------------------

c = canvas.Canvas(OUT, pagesize=A4)

def yen(n):
    return "¥{:,}".format(int(round(n)))

# 余白
LM, RM = 22 * mm, W - 22 * mm

# タイトル
c.setFillColor(NAVY)
c.setFont(G, 26)
c.drawCentredString(W / 2, H - 30 * mm, "御 見 積 書")
c.setStrokeColor(BLUE)
c.setLineWidth(1.4)
c.line(W / 2 - 42 * mm, H - 33 * mm, W / 2 + 42 * mm, H - 33 * mm)

# 右上：番号・日付
c.setFillColor(GRAY)
c.setFont(G, 9.5)
ry = H - 42 * mm
c.drawRightString(RM, ry, f"見積番号： {quote_no}")
c.drawRightString(RM, ry - 5 * mm, f"発行日： {issue_date}")

# 宛先
c.setFillColor(NAVY)
c.setFont(G, 15)
c.drawString(LM, H - 50 * mm, f"{customer}　御中")
c.setStrokeColor(NAVY)
c.setLineWidth(0.8)
c.line(LM, H - 52.5 * mm, LM + 78 * mm, H - 52.5 * mm)

# 発行元ブロック（右・上部）
ix = RM - 70 * mm
iy = H - 56 * mm
c.setFillColor(HexColor("#222222"))
c.setFont(G, 11)
c.drawString(ix, iy, issuer["company"])
c.setFont(M, 8.8)
c.setFillColor(GRAY)
for i, t in enumerate([issuer["zip"], issuer["addr"], issuer["tel"], issuer["person"]]):
    c.drawString(ix, iy - (4.6 * (i + 1)) * mm, t)
# 角印プレースホルダ
c.setStrokeColor(HexColor("#c0392b"))
c.setLineWidth(1)
c.circle(RM - 6 * mm, iy + 1 * mm, 6.5 * mm, fill=0)
c.setFillColor(HexColor("#c0392b"))
c.setFont(G, 7)
c.drawCentredString(RM - 6 * mm, iy - 1.2 * mm, "印")

# あいさつ
c.setFillColor(HexColor("#222222"))
c.setFont(M, 10.5)
c.drawString(LM, H - 82 * mm, "下記の通り御見積申し上げます。ご検討のほど、よろしくお願いいたします。")

# 件名
c.setFont(G, 10.5)
c.drawString(LM, H - 90 * mm, f"件　名： {subject}")

# 御見積金額（強調帯）
subtotal = sum(q * p for _, q, _, p in items)
tax = subtotal * TAX_RATE
total = subtotal + tax
by = H - 106 * mm
c.setFillColor(LIGHT)
c.roundRect(LM, by, 110 * mm, 14 * mm, 2 * mm, fill=1, stroke=0)
c.setFillColor(NAVY)
c.setFont(G, 12)
c.drawString(LM + 5 * mm, by + 5 * mm, "御見積金額（消費税込）")
c.setFont(G, 18)
c.drawRightString(LM + 105 * mm, by + 4 * mm, yen(total))

# ---- 明細テーブル ----
ty = H - 120 * mm
col = [LM, LM + 12 * mm, LM + 92 * mm, LM + 108 * mm, LM + 128 * mm, RM]  # No,品名,数量,単位,単価,金額(right)
rowh = 9 * mm
# ヘッダ
c.setFillColor(NAVY)
c.rect(LM, ty - rowh, RM - LM, rowh, fill=1, stroke=0)
c.setFillColor(HexColor("#ffffff"))
c.setFont(G, 9.5)
heads = [("No.", col[0] + 2 * mm, "l"), ("品　名", col[1] + 2 * mm, "l"),
         ("数量", col[3] - 2 * mm, "r"), ("単位", col[3] + 2 * mm, "l"),
         ("単価", col[4] + 16 * mm, "r"), ("金額", RM - 2 * mm, "r")]
for txt, x, a in heads:
    (c.drawRightString if a == "r" else c.drawString)(x, ty - rowh + 3 * mm, txt)

# 行
c.setFont(M, 9.5)
y = ty - rowh
DISPLAY_ROWS = max(len(items), 6)
for i in range(DISPLAY_ROWS):
    y -= rowh
    if i % 2 == 1:
        c.setFillColor(HexColor("#f6f8fc"))
        c.rect(LM, y, RM - LM, rowh, fill=1, stroke=0)
    if i < len(items):
        name, qty, unit, price = items[i]
        amt = qty * price
        c.setFillColor(HexColor("#222222"))
        c.drawString(col[0] + 2 * mm, y + 3 * mm, str(i + 1))
        c.drawString(col[1] + 2 * mm, y + 3 * mm, name)
        c.drawRightString(col[3] - 2 * mm, y + 3 * mm, f"{qty:,}")
        c.drawString(col[3] + 2 * mm, y + 3 * mm, unit)
        c.drawRightString(col[4] + 16 * mm, y + 3 * mm, yen(price))
        c.drawRightString(RM - 2 * mm, y + 3 * mm, yen(amt))

# 罫線
c.setStrokeColor(LINE)
c.setLineWidth(0.6)
top = ty - rowh
bottom = y
c.rect(LM, bottom, RM - LM, top - bottom, fill=0, stroke=1)
for x in col[1:-1]:
    c.line(x, bottom, x, top)
yy = top
for _ in range(DISPLAY_ROWS):
    yy -= rowh
    c.line(LM, yy, RM, yy)

# 合計ブロック（右下）
sx = LM + 108 * mm
def trow(label, val, yv, bold=False):
    c.setStrokeColor(LINE)
    c.rect(sx, yv, RM - sx, rowh, fill=0, stroke=1)
    c.setFillColor(NAVY if bold else HexColor("#333333"))
    c.setFont(G, 10 if bold else 9.5)
    c.drawString(sx + 3 * mm, yv + 3 * mm, label)
    c.drawRightString(RM - 2 * mm, yv + 3 * mm, yen(val))

sy = bottom - rowh - 2 * mm
trow("小　計", subtotal, sy)
trow("消費税（10%）", tax, sy - rowh)
c.setFillColor(LIGHT)
c.rect(sx, sy - 2 * rowh, RM - sx, rowh, fill=1, stroke=0)
trow("合　計", total, sy - 2 * rowh, bold=True)

# 備考
ry2 = sy - 2 * rowh
c.setFillColor(HexColor("#333333"))
c.setFont(G, 9.5)
c.drawString(LM, ry2 + 3 * mm, "備　考")
c.setStrokeColor(LINE)
c.rect(LM, ry2 - 22 * mm, 95 * mm, 25 * mm, fill=0, stroke=1)
c.setFont(M, 8.8)
c.setFillColor(GRAY)
notes = [
    f"・お見積有効期限： {expire}",
    "・納期： ご発注後 約2週間",
    "・お支払： 月末締め翌月末払い（銀行振込）",
    "※本書はPA45ハンズオン用のサンプルです。",
]
for i, t in enumerate(notes):
    c.drawString(LM + 3 * mm, ry2 - 4 * mm - i * 4.6 * mm, t)

# フッター
c.setFillColor(HexColor("#9aa6bf"))
c.setFont(G, 7.5)
c.drawCentredString(W / 2, 12 * mm, "SAMPLE / PA45 第15回ハンズオン用サンプル見積書 ー 数値・社名はすべて架空です")

c.showPage()
c.save()
print("OK:", OUT)

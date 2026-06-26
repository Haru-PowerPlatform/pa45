"""バッジ中央アイコン（AIスパーク）を SVG から透過PNGに焼く。

cairo ネイティブが無い環境向けに、LibreOffice で白背景/黒背景の2回レンダリングし、
その差分から正確なアルファ（透過＋色）を復元する。

出力: assets/badges/_icons/copilot-spark.svg / copilot-spark.png
使い方: python scripts/build-badge-icon.py
"""
import subprocess, os
from PIL import Image
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "assets", "badges", "_icons")
os.makedirs(OUTDIR, exist_ok=True)
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"
TMP = os.environ.get("TEMP", r"C:\Temp")

# --- AIスパーク（4点・凹カーブ）＋サブスパーク ---
SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="560" height="560">
  <defs>
    <radialGradient id="g" cx="42%" cy="34%" r="72%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="38%" stop-color="#a5f3fc"/>
      <stop offset="72%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#2563eb"/>
    </radialGradient>
    <radialGradient id="g2" cx="42%" cy="34%" r="72%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="60%" stop-color="#7dd3fc"/>
      <stop offset="100%" stop-color="#0ea5e9"/>
    </radialGradient>
  </defs>
  <path d="M120,34 C129,98 142,111 206,120 C142,129 129,142 120,206 C111,142 98,129 34,120 C98,111 111,98 120,34 Z"
        fill="#0b1020" opacity="0.30" transform="translate(4 6)"/>
  <path d="M120,34 C129,98 142,111 206,120 C142,129 129,142 120,206 C111,142 98,129 34,120 C98,111 111,98 120,34 Z"
        fill="url(#g)"/>
  <ellipse cx="104" cy="92" rx="14" ry="10" fill="#ffffff" opacity="0.55" transform="rotate(-30 104 92)"/>
  <path d="M196,44 C199,62 205,68 223,71 C205,74 199,80 196,98 C193,80 187,74 169,71 C187,68 193,62 196,44 Z"
        fill="url(#g2)"/>
</svg>'''

svg_path = os.path.join(OUTDIR, "copilot-spark.svg")
open(svg_path, "w", encoding="utf-8").write(SVG)

i = SVG.index(">") + 1
def render(color, tag):
    rect = f'<rect x="-20" y="-20" width="280" height="280" fill="{color}"/>'
    s = SVG[:i] + rect + SVG[i:]
    p = os.path.join(TMP, f"_sp_{tag}.svg"); open(p, "w", encoding="utf-8").write(s)
    png = os.path.join(TMP, f"_sp_{tag}.png")
    if os.path.exists(png): os.remove(png)
    subprocess.run([SOFFICE, "--headless", "--convert-to", "png", "--outdir", TMP, p],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return np.asarray(Image.open(png).convert("RGB")).astype(np.float64)

Iw = render("#ffffff", "w"); Ib = render("#000000", "b")
alpha = np.clip(1.0 - (Iw - Ib).mean(axis=2) / 255.0, 0, 1)
a3 = np.clip(alpha[..., None], 1e-6, 1.0)
color = np.clip(Ib / a3, 0, 255)
rgba = np.dstack([color, alpha * 255]).astype(np.uint8)
out_png = os.path.join(OUTDIR, "copilot-spark.png")
Image.fromarray(rgba, "RGBA").save(out_png)
print("OK:", out_png, rgba.shape)

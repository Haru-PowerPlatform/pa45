# -*- coding: utf-8 -*-
"""バッジSVG→PNG のレンダリング（make-badge-svg.py / make-badge-flat.py 共用）。

ヘッドレスChromeで2倍サイズに描いてからPillowで縮小＝スーパーサンプリング。
"""
import os
import subprocess
import tempfile

from PIL import Image

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT_SIZE = 880
RENDER_SCALE = 2


def render(svg, out_path):
    rs = OUT_SIZE * RENDER_SCALE
    with tempfile.TemporaryDirectory() as td:
        html = os.path.join(td, "badge.html")
        big = os.path.join(td, "big.png")
        with open(html, "w", encoding="utf-8") as f:
            f.write('<!doctype html><html><head><meta charset="utf-8">'
                    '<style>html,body{margin:0;padding:0;background:transparent}'
                    f'svg{{display:block;width:{rs}px;height:{rs}px}}</style></head>'
                    f'<body>{svg}</body></html>')
        cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               "--no-sandbox", "--force-device-scale-factor=1",
               f"--window-size={rs},{rs}", "--default-background-color=00000000",
               f"--screenshot={big}", "file:///" + html.replace("\\", "/")]
        subprocess.run(cmd, check=True, capture_output=True)
        img = Image.open(big).convert("RGBA")
        img = img.crop((0, 0, rs, rs)).resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        img.save(out_path)
    return out_path

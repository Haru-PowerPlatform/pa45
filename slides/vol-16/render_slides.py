# -*- coding: utf-8 -*-
"""vol-16/index.html の各 <section class="slide"> を 1280x720 PNG に書き出す。"""
import re, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "index.html")
OUT  = os.path.join(HERE, "png")
os.makedirs(OUT, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

html = open(SRC, encoding="utf-8").read()
style = re.search(r"<style>.*?</style>", html, re.S).group(0)
# 各スライド section（id="sN"）を抽出
sections = re.findall(r'(<section class="slide[^"]*" id="s\d+">.*?</section>)', html, re.S)
print(f"{len(sections)} slides found")

WRAP = """<!doctype html><html lang="ja"><head><meta charset="utf-8">
{style}
<style>
  body{{margin:0;padding:0;background:#fff;}}
  .toc,.toc-toggle,.deck-header{{display:none!important;}}
  .slide{{margin:0!important;box-shadow:none!important;border-radius:0!important;}}
  .slide-num{{display:none!important;}}
</style></head><body>{section}</body></html>"""

for i, sec in enumerate(sections, 1):
    m = re.search(r'id="s(\d+)"', sec)
    n = int(m.group(1))
    page = WRAP.format(style=style, section=sec)
    tmp = os.path.join(OUT, f"_tmp_s{n:02d}.html")
    open(tmp, "w", encoding="utf-8").write(page)
    png = os.path.join(OUT, f"vol16-s{n:02d}.png")
    url = "file:///" + tmp.replace("\\", "/")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=1280,720",
                    f"--screenshot={png}", url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
    ok = os.path.exists(png)
    print(f"  s{n:02d} -> {'OK' if ok else 'FAIL'} {png if ok else ''}")
    os.remove(tmp)

print("done")

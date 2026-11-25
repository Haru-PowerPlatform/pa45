#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""アイキャッチ（2026-11-22 作り直し）。
はる指摘：アイキャッチだけだと何の資格か分かりづらい → Microsoft 認定・Microsoft 365 Copilot の資格であることを前に出す。
_eyecatch_kit の型（カテゴリ96）で描き、右上に Copilot のアイコンを重ねる。

  python make_eyecatch.py          … assets/eyecatch.png を作るだけ
  python make_eyecatch.py --push   … アップロードして Post 5930 のアイキャッチを差し替える
"""
import json, pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import _eyecatch_kit  # noqa: E402
from _howtokit import _req  # noqa: E402

OUT = HERE / "assets" / "eyecatch.png"
ICON = pathlib.Path(r"C:\Users\isamu\Documents\assets-icons\ms\copilot.png")

_eyecatch_kit.render(96, "Microsoft 認定資格 AB-730",
                     "Microsoft 365 Copilot の資格",
                     "<b>実画面</b>で1問ずつ",
                     "知識だけで終わらせず、実務で使える形にする", OUT)

# Copilot のアイコンを左上の余白に置く（2400×1260 の2倍解像度）
im = Image.open(OUT).convert("RGBA")
ic = Image.open(ICON).convert("RGBA").resize((210, 210), Image.LANCZOS)
im.alpha_composite(ic, (150, 110))
im.convert("RGB").save(OUT, optimize=True)
print(OUT, im.size)

if "--push" in sys.argv:
    st = json.loads((HERE / "post_state.json").read_text(encoding="utf8"))
    m = _req("POST", "/wp-json/wp/v2/media", raw=OUT.read_bytes(),
             headers={"Content-Type": "image/png", "Content-Disposition": 'attachment; filename="ab730-handson-eyecatch-v2.png"'})
    _req("POST", f"/wp-json/wp/v2/posts/{st['post_id']}", {"featured_media": m["id"]})
    j = _req("GET", f"/wp-json/wp/v2/posts/{st['post_id']}?context=edit")
    st["eyecatch"] = m["id"]
    (HERE / "post_state.json").write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf8")
    print("featured_media", j["featured_media"], "status", j["status"])

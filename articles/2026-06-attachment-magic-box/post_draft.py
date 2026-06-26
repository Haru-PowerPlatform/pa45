#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""魔法の箱記事をWordPress下書きとして作成（アイキャッチ=スライドPNG）。自動公開しない=status:draft固定。"""
import os, sys, base64, mimetypes, requests, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]   # pa45/
HERE = pathlib.Path(__file__).resolve().parent

# .env 読み込み
env = {}
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()

WP_URL  = env["WP_URL"].rstrip("/")
WP_USER = env["WP_USER"]
WP_PASS = env["WP_PASS"]
auth = base64.b64encode(f"{WP_USER}:{WP_PASS}".encode()).decode()
H = {"Authorization": f"Basic {auth}"}

TITLE = "メールの重い添付を自動でOneDriveへ｜“魔法の箱”フローの作り方（Power Automate）"
SLUG  = "attachment-auto-save-onedrive"
CAT   = 76  # Power Automate 実践・Tips
body  = (HERE / "article.html").read_text(encoding="utf-8")

# 1) アイキャッチ（スライドPNG）をアップロード
png = ROOT / "assets" / "x" / "html" / "vol-43" / "vol43.png"
media_id = None
if png.exists():
    data = png.read_bytes()
    mh = dict(H)
    mh["Content-Disposition"] = 'attachment; filename="attachment-magic-box.png"'
    mh["Content-Type"] = "image/png"
    r = requests.post(f"{WP_URL}/wp-json/wp/v2/media", headers=mh, data=data, timeout=120)
    r.raise_for_status()
    media_id = r.json()["id"]
    print("media_id =", media_id)
else:
    print("WARN: slide PNG not found:", png)

# 2) 下書き作成
payload = {
    "title": TITLE,
    "slug": SLUG,
    "status": "draft",          # ★公開しない（手動公開）
    "content": body,
    "categories": [CAT],
}
if media_id:
    payload["featured_media"] = media_id

r = requests.post(f"{WP_URL}/wp-json/wp/v2/posts", headers=H, json=payload, timeout=120)
r.raise_for_status()
j = r.json()
print("POST_ID =", j["id"])
print("EDIT    =", f"{WP_URL}/wp-admin/post.php?post={j['id']}&action=edit")
print("PREVIEW =", f"{WP_URL}/?p={j['id']}&preview=true")

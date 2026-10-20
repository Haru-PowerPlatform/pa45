# -*- coding: utf-8 -*-
"""automate136 の全投稿を、表示が崩れる・壊れる観点でまとめて調べる（読むだけ。変更しない）。

  python scripts/audit-wp-posts.py            # 一覧を出す
  python scripts/audit-wp-posts.py --images   # 画像URLの生存確認もする（公開・予約のみ・時間がかかる）
"""
import json, pathlib, re, sys
from collections import defaultdict
import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
env = {}
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"')
WP = env["WP_URL"].rstrip("/"); AUTH = (env["WP_USER"], env["WP_PASS"])

posts = []
for st in ("publish", "future", "draft"):
    page = 1
    while True:
        r = requests.get(f"{WP}/wp-json/wp/v2/posts", auth=AUTH, timeout=120,
                         params={"status": st, "per_page": 100, "page": page, "context": "edit",
                                 "_fields": "id,status,title,content,featured_media,slug,categories"})
        if r.status_code != 200 or not r.json():
            break
        posts += r.json(); page += 1

issues = defaultdict(list)
img_urls = defaultdict(set)
for p in posts:
    pid, st = p["id"], p["status"]
    raw, ren = p["content"]["raw"], p["content"]["rendered"]
    title = p["title"]["raw"]
    tag = (pid, st, title[:28])
    for svg in re.findall(r"<svg.*?</svg>", ren, flags=re.S):
        if re.search(r"<p[ >]|</p>|<br", svg):
            issues["SVGの中に<p>/<br>が入っている"].append(tag); break
    if re.search(r"<script", raw):
        issues["<script>がある"].append(tag)
    if re.search(r"(file:///|localhost|127\.0\.0\.1|C:\\\\Users|C:/Users)", raw):
        issues["ローカルのパス/URLが残っている"].append(tag)
    if re.search(r"(^|\n)\s*#{2,3} |\*\*[^*\n]+\*\*", re.sub(r"<style.*?</style>|<pre.*?</pre>|<code.*?</code>", "", raw, flags=re.S)):
        issues["Markdown記法が残っている（** や ##）"].append(tag)
    if re.search(r"TODO|ここに.{0,10}(入れる|入る|差し替え)|（仮）|XXX", re.sub(r"<style.*?</style>", "", raw, flags=re.S)):
        issues["仮の文字が残っている（TODO・ここに入れる など）"].append(tag)
    empties = len(re.findall(r"<p>\s*(&nbsp;)?\s*</p>", ren))
    if empties >= 3:
        issues[f"空の段落が3つ以上"].append(tag + (empties,))
    if re.search(r"<[a-z]", title):
        issues["タイトルにHTMLタグ"].append(tag)
    if not title.strip():
        issues["タイトルが空"].append(tag)
    if st in ("publish", "future") and not p["featured_media"]:
        issues["アイキャッチ未設定（公開・予約）"].append(tag)
    if st in ("publish", "future") and re.search(r"%[0-9a-f]{2}", p["slug"], flags=re.I):
        issues["スラッグが日本語のまま（公開・予約）"].append(tag)
    if st in ("publish", "future") and p["categories"] == [1]:
        issues["カテゴリ未設定（未分類）"].append(tag)
    if re.search(r"<img(?![^>]*\balt=)[^>]*>", ren):
        issues["altの無い画像"].append(tag)
    # 閉じ忘れの目安：div の開きと閉じの数
    o, c = len(re.findall(r"<div\b", raw)), len(re.findall(r"</div>", raw))
    if o != c:
        issues[f"<div>の開きと閉じの数が合わない"].append(tag + (f"{o}/{c}",))
    if st in ("publish", "future"):
        for u in re.findall(r'<img[^>]+src="([^"]+)"', ren):
            img_urls[u].add(pid)

print(f"posts={len(posts)}")
for k, v in issues.items():
    print(f"\n■ {k}：{len(v)}本")
    for t in v[:40]:
        print("   ", t)

if "--images" in sys.argv:
    dead = []
    for u, pids in img_urls.items():
        if u.startswith("data:"):
            continue
        try:
            r = requests.head(u, timeout=20, allow_redirects=True)
            if r.status_code >= 400:
                r = requests.get(u, timeout=20, stream=True)
            if r.status_code >= 400:
                dead.append((r.status_code, u, sorted(pids)))
        except Exception as e:
            dead.append(("ERR", u, sorted(pids)))
    print(f"\n■ 表示されない画像（公開・予約）：{len(dead)}件 / {len(img_urls)}件中")
    for d in dead[:60]:
        print("   ", d)

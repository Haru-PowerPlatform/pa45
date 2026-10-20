# -*- coding: utf-8 -*-
"""automate136 の投稿本文に埋め込んだ <style> を、WordPress に壊されない形（1行）に直す。

WordPress は表示のときに <style> の中の改行を <br />、空行を </p><p> に変え、CSS のルールが無効になる（2026-10-20 確認）。
content.raw の <style>…</style> の中だけ、改行・空行・紛れ込んだ <p> <br> を取り除いて1行にする。status は変えない。

  python scripts/fix-wp-style-blocks.py          # 対象を一覧にするだけ（変更しない）
  python scripts/fix-wp-style-blocks.py --apply  # バックアップを取ってから更新
  python scripts/fix-wp-style-blocks.py --check  # 全投稿の content.rendered を確認
"""
import json, pathlib, re, sys, datetime
import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
env = {}
for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"')
WP = env["WP_URL"].rstrip("/"); AUTH = (env["WP_USER"], env["WP_PASS"])
BK = ROOT.parent / "_wp_style_backup" / datetime.date.today().isoformat()   # 公開リポジトリの外（下書き本文を含むため）


def all_posts():
    out = []
    for st in ("publish", "draft", "future", "pending", "private"):
        page = 1
        while True:
            r = requests.get(f"{WP}/wp-json/wp/v2/posts", auth=AUTH, timeout=120,
                             params={"status": st, "per_page": 100, "page": page, "context": "edit",
                                     "_fields": "id,status,title,content,date"})
            if r.status_code != 200:
                break
            js = r.json()
            if not js:
                break
            out += js
            page += 1
    return out


def style_broken(rendered):
    bad = 0
    for s in re.findall(r"<style[^>]*>(.*?)</style>", rendered, flags=re.S):
        if "<br" in s or "<p" in s or "</p>" in s:
            bad += 1
    return bad


def fix_style(raw):
    def one(m):
        css = m.group(2)
        css = re.sub(r"</?p[^>]*>|<br\s*/?>", "", css)        # 紛れ込んだタグ
        css = re.sub(r"\s*\n\s*", "", css)                     # 改行・空行
        return m.group(1) + css + m.group(3)
    return re.sub(r"(<style[^>]*>)(.*?)(</style>)", one, raw, flags=re.S)


def main():
    posts = all_posts()
    targets = [p for p in posts if "<style" in p["content"]["rendered"] and style_broken(p["content"]["rendered"])]
    with_style = sum(1 for p in posts if "<style" in p["content"]["rendered"])
    print(f"posts={len(posts)} with_style={with_style} broken={len(targets)}")
    if "--check" in sys.argv:
        for p in targets:
            print("  still broken:", p["id"], p["status"], p["title"]["raw"][:40])
        return
    if "--apply" not in sys.argv:
        for p in targets:
            print(f"  {p['id']:>5} {p['status']:<8} {p['title']['raw'][:40]}")
        return
    BK.mkdir(parents=True, exist_ok=True)
    results = []
    for p in targets:
        raw = p["content"]["raw"]
        (BK / f"{p['id']}.html").write_text(raw, encoding="utf-8")
        new = fix_style(raw)
        if new == raw:
            results.append((p["id"], p["status"], "変更なし（raw は正常・別要因）")); continue
        r = requests.post(f"{WP}/wp-json/wp/v2/posts/{p['id']}", auth=AUTH, json={"content": new}, timeout=120)
        q = requests.get(f"{WP}/wp-json/wp/v2/posts/{p['id']}", auth=AUTH, timeout=60,
                         params={"context": "edit", "_fields": "status,content,date"}).json()
        ok = r.status_code == 200 and q["status"] == p["status"] and not style_broken(q["content"]["rendered"])
        results.append((p["id"], p["status"], ("OK" if ok else f"NG http={r.status_code} status={q['status']}")))
        print(p["id"], p["status"], results[-1][2])
    (BK / "_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print("backup:", BK)


if __name__ == "__main__":
    main()

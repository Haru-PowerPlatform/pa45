r"""
ブログ（automate136.com）の投稿状況を取得して data/blog-board.json に書き出す

articles/*/ から WordPress の投稿IDを拾い（post_state.json / post_id.txt / README.md の順）、
WP REST API で「いま下書きなのか公開済みなのか」を実際に見に行きます。
記事がまだ無い企画（plan.md だけある）は「ネタ」として拾います。

出力は投稿ボード（scripts/build-x-board.py）のブログタブが読みます。
未公開記事のタイトルが入るので data/blog-board.json は .gitignore 済み。

使い方:
  python scripts/fetch-blog-status.py
"""

import base64
import glob
import io
import json
import os
import pathlib
import re
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "blog-board.json"


def load_env():
    env = {}
    p = ROOT / ".env"
    if not p.exists():
        raise SystemExit(".env が見つかりません（WP_URL / WP_USER / WP_PASS が必要）")
    for line in io.open(p, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def find_post_id(d: str):
    """記事フォルダから WordPress の投稿IDを探す"""
    ps = os.path.join(d, "post_state.json")
    if os.path.exists(ps):
        try:
            pid = json.load(io.open(ps, encoding="utf-8")).get("post_id")
            if pid:
                return int(pid)
        except Exception:
            pass
    pt = os.path.join(d, "post_id.txt")
    if os.path.exists(pt):
        m = re.search(r"\d+", io.open(pt, encoding="utf-8").read())
        if m:
            return int(m.group())
    rm = os.path.join(d, "README.md")
    if os.path.exists(rm):
        t = io.open(rm, encoding="utf-8", errors="replace").read()
        m = re.search(r"Post ID[^\d]{0,6}(\d{3,6})", t)
        if m:
            return int(m.group(1))
    return None


def summary_of(d: str):
    """README の企画意図 → なければ article.html の冒頭から要約用テキストを作る"""
    rm = os.path.join(d, "README.md")
    if os.path.exists(rm):
        t = io.open(rm, encoding="utf-8", errors="replace").read()
        m = re.search(r"##\s*企画意図\s*\n+(.+?)(?:\n##|\Z)", t, re.S)
        if m:
            return re.sub(r"\s+", " ", m.group(1)).strip()[:180]
    for f in ("plan.md", "PLAN.md"):
        p = os.path.join(d, f)
        if os.path.exists(p):
            t = io.open(p, encoding="utf-8", errors="replace").read()
            t = re.sub(r"^#.*$", "", t, flags=re.M)
            return re.sub(r"\s+", " ", t).strip()[:180]
    a = os.path.join(d, "article.html")
    if os.path.exists(a):
        return lead_of_html(io.open(a, encoding="utf-8", errors="replace").read())
    return ""


def lead_of_html(t: str):
    """本文HTMLから冒頭のリード文を取り出す（style/scriptは捨てる）"""
    t = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", t, flags=re.S | re.I)
    for m in re.finditer(r"<p[^>]*>(.*?)</p>", t, re.S | re.I):
        txt = re.sub(r"<[^>]+>", "", m.group(1))
        txt = re.sub(r"\s+", " ", txt).strip()
        if len(txt) >= 20:                     # 見出し直下の飾り行を飛ばす
            return txt[:180]
    txt = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", txt).strip()[:180]


def wp_get(base, auth, pid):
    url = (f"{base}/wp-json/wp/v2/posts/{pid}?context=edit"
           "&_fields=id,status,title,date,modified,link,slug,content")
    req = urllib.request.Request(url, headers={"Authorization": "Basic " + auth,
                                               "User-Agent": "pa45-blog-board"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)


def main():
    env = load_env()
    base = env["WP_URL"].rstrip("/")
    auth = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()

    items = []
    for d in sorted(glob.glob(str(ROOT / "articles" / "*") + os.sep), reverse=True):
        name = pathlib.Path(d.rstrip(os.sep)).name
        pid = find_post_id(d)
        row = {
            "slug": name,
            "post_id": pid,
            "summary": summary_of(d),
            "has_article": os.path.exists(os.path.join(d, "article.html")),
            "folder": f"pa45/articles/{name}/",
        }
        if pid:
            try:
                w = wp_get(base, auth, pid)
                raw = w.get("content", {}).get("raw", "")
                clean = re.sub(r"<(style|script)[^>]*>.*?</(?:style|script)>", " ", raw,
                               flags=re.S | re.I)
                text = re.sub(r"<[^>]+>", "", clean)
                lead = lead_of_html(raw)
                if lead:
                    row["summary"] = lead        # 記事があるならWP本文の書き出しを見せる
                row.update({
                    "title": w["title"]["raw"],
                    "status": w["status"],          # draft / publish / private など
                    "modified": w["modified"][:10],
                    "chars": len(re.sub(r"\s+", "", text)),
                    "edit_url": f"{base}/wp-admin/post.php?post={pid}&action=edit",
                    "preview_url": f"{base}/?p={pid}&preview=true",
                    "public_url": w.get("link", ""),
                })
            except urllib.error.HTTPError as e:
                row.update({"title": name, "status": f"error({e.code})"})
            except Exception as e:
                row.update({"title": name, "status": f"error"})
                print(f"  [WARN] {name}: {e}")
        else:
            row.update({"title": name, "status": "idea"})   # 企画だけ（WP未作成）
        items.append(row)

    order = {"draft": 0, "idea": 1, "publish": 2}
    items.sort(key=lambda r: (order.get(r["status"], 3), r["slug"]), reverse=False)

    OUT.write_text(json.dumps({
        "_note": "automate136.com の投稿状況。WP REST APIで実ステータスを取得（下書きタイトルを含むためgit管理外）",
        "site": base,
        "items": items,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    n = {"draft": 0, "publish": 0, "idea": 0}
    for r in items:
        n[r["status"]] = n.get(r["status"], 0) + 1
    print(f"[OK] {OUT}")
    print(f"  下書き {n.get('draft',0)} / 公開済み {n.get('publish',0)} / ネタ {n.get('idea',0)}")


if __name__ == "__main__":
    main()

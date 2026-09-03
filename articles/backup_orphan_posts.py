#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成元スクリプトが失われた記事を、WordPress から本文ごと回収してリポジトリに退避する。

2026-09-04、articles/ 配下の 2026-08 系フォルダの build_article.py が消えていることが判明した。
git に一度も追跡されていなかったため復元できない。WP 側の記事は生きているので、
本文（raw HTML）と体裁だけでも versioned な形で残しておく。

  python backup_orphan_posts.py            # 生成元が実在する記事フォルダを一覧表示するだけ
  python backup_orphan_posts.py --fetch    # 既知の Copilot Studio 記事を WP から取得して _recovered/ に保存

保存先: articles/_recovered/<slug>-<id>/article.html  ＋  meta.json
※ 生成元の代わりにはならない（--push で更新はできない）。あくまで内容の保全。
※ 生成元が残っている記事も含めて丸ごと取得する。差分が出たら WP 側が正（手で直された可能性）。
"""
import base64, json, pathlib, sys, re
import requests

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
OUT = HERE / "_recovered"
FETCH = "--fetch" in sys.argv

# Copilot Studio 系として把握している記事（メモリの Post ID 表より）
KNOWN = {
    2583: "first-agent", 2594: "knowledge", 2588: "orchestrator", 2652: "tools",
    2591: "vs-pa", 2670: "a2a", 2653: "cost-design", 2825: "credit-boundary",
    2712: "declutter", 2638: "evaluate", 2675: "flow", 2823: "harness",
    2837: "harness-pricing", 2821: "learning-environment", 2728: "parts-translation",
    2710: "scheduled-notify", 2733: "skills", 2677: "teams",
    3071: "boundary", 3165: "environment", 3170: "dlp-policy", 3186: "managed-env",
    3198: "credit-visibility", 3241: "knowledge-governance", 3282: "alm",
    4079: "industry-demos",
}


def local_generators():
    """build_article.py が実在する記事フォルダの一覧。"""
    return {p.parent.name for p in HERE.glob("*/build_article.py")}


def wp_session():
    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1); env[k.strip()] = v.strip()
    url = env["WP_URL"].rstrip("/")
    auth = base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    return url, {"Authorization": f"Basic {auth}"}


def main():
    have = local_generators()
    print(f"生成元が実在する記事フォルダ: {len(have)} 件")
    for n in sorted(have):
        print("   ", n)

    if not FETCH:
        print("\n--fetch を付けると、WP から本文を取得して _recovered/ に保存します")
        return

    WP, H = wp_session()
    OUT.mkdir(exist_ok=True)
    saved, missing = [], []
    for pid, tag in sorted(KNOWN.items()):
        r = requests.get(f"{WP}/wp-json/wp/v2/posts/{pid}?context=edit", headers=H, timeout=60)
        if r.status_code != 200:
            missing.append((pid, tag, r.status_code)); continue
        j = r.json()
        slug = j.get("slug") or tag
        d = OUT / f"{slug}-{pid}"
        d.mkdir(parents=True, exist_ok=True)
        (d / "article.html").write_text(j["content"]["raw"], encoding="utf-8")
        meta = {
            "post_id": pid, "slug": slug, "status": j["status"],
            "title": j["title"]["raw"], "categories": j["categories"],
            "featured_media": j.get("featured_media"),
            "modified": j.get("modified"),
            "note": "生成元スクリプトが失われた記事の内容退避（2026-09-04）",
        }
        (d / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        saved.append((pid, slug, j["status"], len(j["content"]["raw"])))

    print(f"\n保存: {len(saved)} 件 -> {OUT}")
    for pid, slug, st, n in saved:
        print(f"   {pid}  {st:7}  {n:>7,} chars  {slug}")
    if missing:
        print("\n取得できず:")
        for pid, tag, code in missing:
            print(f"   {pid}  {tag}  HTTP {code}")


if __name__ == "__main__":
    main()

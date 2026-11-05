#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""公開済み記事の「赤枠がずれているスクショ」を元スクショから作り直して差し替える（2026-11-05）。

2026-11-04 はる指摘「赤枠がずれてるスクショがあり」→ 全記事の赤枠を目視で点検した結果の直し。
方式は articles/2026-08-copilot-studio-a2a/fix_boxes_rest.py（Post 2670）と同じ：
  元スクショ（OneDrive\\画像\\Screenshots）の同じ範囲を切り出し → _shots.render で枠・マスクを描く
  → WPメディアへアップ → 本文の画像URLだけ差し替える（status は触らない・raw はバックアップ）。
元スクショと切り出し位置は、旧画像との照合（赤を除いたテンプレートマッチ）で特定した。

spec = articles/_shots/redbox_fix_2026-11.json  {"<post_id>": [{"old": URL, "id": .., "src": .., "crop": .., "boxes": .., "mask": ..}]}
  python _fix_red_boxes.py 2638          … 画像だけ作る（_shots/img/<pid>-<id>.png）
  python _fix_red_boxes.py 2638 --push   … アップして本文の画像URLを差し替え
"""
import json, sys, time
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _shots  # noqa

SPEC = HERE / "_shots" / "redbox_fix_2026-11.json"
BACKUP = HERE / "_shots" / "backup"


def main():
    pid = int(sys.argv[1])
    shots = json.loads(SPEC.read_text(encoding="utf-8"))[str(pid)]
    outs = {}
    for s in shots:
        out, size = _shots.render(pid, s)
        outs[s["old"]] = out
        print("png:", out, size)
    if _shots.BOX_PROBLEMS:
        for p in _shots.BOX_PROBLEMS:
            print("BOX:", p)
        raise SystemExit("枠の位置を決め直す")
    if "--push" not in sys.argv:
        return
    wp, auth = _shots._env()
    post = requests.get(f"{wp}/wp-json/wp/v2/posts/{pid}", auth=auth,
                        params={"context": "edit", "_fields": "status,content"}).json()
    raw, st = post["content"]["raw"], post["status"]
    BACKUP.mkdir(exist_ok=True)
    (BACKUP / f"redbox-{pid}-{time.strftime('%Y%m%d-%H%M%S')}.html").write_text(raw, encoding="utf-8")
    new = raw
    for old, out in outs.items():
        assert new.count(old) == 1, old
        new = new.replace(old, _shots.upload(out, wp, auth))
    r = requests.post(f"{wp}/wp-json/wp/v2/posts/{pid}", auth=auth, json={"content": new}, timeout=120)
    r.raise_for_status()
    assert r.json()["status"] == st
    print("UPDATED", pid, st)


if __name__ == "__main__":
    main()

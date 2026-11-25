# -*- coding: utf-8 -*-
"""スクショだけ差し替える（本文は作り直さない）。2026-11-05。

WP の本文には build_NN を通さずに入った変更（CTA の差し替え・ゴールラベルのCSS）があるため、
`build_NN_*.py --push` で丸ごと上書きすると、それが消える。
ここでは shotkit で書き出した画像のうち、post_state の sha と違うものだけをアップし、
本文の画像URLだけを置き換え、post_state の media も新しいものに更新する（status は触らない）。
  python swap_shots.py 01          … 差分の一覧だけ
  python swap_shots.py 01 --push   … アップして差し替え
"""
import hashlib, json, sys, time, pathlib
import requests
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent))
import shotkit  # noqa
import _shots  # noqa

no = sys.argv[1]
state_path = HERE / f"post_state_{no}.json"
state = json.loads(state_path.read_text(encoding="utf-8"))
pid = state["post_id"]

changed = []
for key, m in state["media"].items():
    out, size = shotkit.render(key)
    sha = hashlib.sha1(out.read_bytes()).hexdigest()
    if sha != m.get("sha"):
        changed.append((key, out, sha))
if shotkit.BOX_PROBLEMS:
    raise SystemExit("枠の位置を直す:\n" + "\n".join(shotkit.BOX_PROBLEMS))
print(pid, "changed:", [k for k, _, _ in changed])
if "--push" not in sys.argv or not changed:
    sys.exit()

wp, auth = _shots._env()
post = requests.get(f"{wp}/wp-json/wp/v2/posts/{pid}", auth=auth, params={"context": "edit", "_fields": "status,content"}).json()
raw, st = post["content"]["raw"], post["status"]
(HERE / "shots" / f"backup-{pid}-{time.strftime('%Y%m%d-%H%M%S')}.html").write_text(raw, encoding="utf-8")
new = raw
for key, out, sha in changed:
    old = state["media"][key]["url"]
    assert new.count(old) >= 1, old
    r = requests.post(f"{wp}/wp-json/wp/v2/media", auth=auth, data=out.read_bytes(), timeout=180,
                      headers={"Content-Disposition": f'attachment; filename="{out.name}"', "Content-Type": "image/png"})
    r.raise_for_status(); j = r.json()
    requests.post(f"{wp}/wp-json/wp/v2/media/{j['id']}", auth=auth, json={"alt_text": shotkit.SHOTS[key]["alt"]}, timeout=60)
    new = new.replace(old, j["source_url"])
    state["media"][key] = {"id": j["id"], "url": j["source_url"], "size": list(Image.open(out).size), "sha": sha}
    print("uploaded", key, j["source_url"])
r = requests.post(f"{wp}/wp-json/wp/v2/posts/{pid}", auth=auth, json={"content": new}, timeout=120)
r.raise_for_status()
assert r.json()["status"] == st
state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
print("UPDATED", pid, st)

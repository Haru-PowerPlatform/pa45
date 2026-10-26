r"""
今日の投稿を選んで、朝ボード（posts/today）に書き込む形の JSON を出す。

  python scripts/pick-today-posts.py --done postdone.json [--date 2026-10-26] [--out posts-today.json]

--done は朝ボードの postdone コレクション（はるが「投稿したらチェック」を付けたもの）を
ArtifactData で書き出したファイル。[{id, done}] の配列か {id: {done}} の辞書のどちらでもよい。

選び方（量で圧倒しないよう1日2本まで・開催日だけ3本）
  X        毎日1本。X技術Tips を板と同じ並び順で、まだ投稿していないものから。
           火曜はコパスタ、金曜は M365 Copilot（在庫が無ければ Power Automate）。
           PA45 の開催週は、月曜＝告知②、開催日＝告知③（昼）と④（開催15分前）を足す。
  LinkedIn 月曜・金曜に1本。data/linkedin-board.json の順番（MCT自己紹介の1本目 → ブログ紹介と
           Tips紹介を交互 → 4本ごとに MCT自己紹介の残り）で、まだ投稿していないもの。
本文と画像の場所は X投稿ボードと同じもの（build-x-board.py の関数をそのまま使う）。
"""
import argparse
import importlib.util
import json
import sys
from datetime import datetime, timedelta, timezone, date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("bxb", ROOT / "scripts" / "build-x-board.py")
bxb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bxb)

JST = timezone(timedelta(hours=9))
WD = "月火水木金土日"


def load_done(path):
    if not path:
        return set()
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        raw = [{"id": k, **(v if isinstance(v, dict) else {"done": v})} for k, v in raw.items()]
    return {str(r.get("id")) for r in raw if r.get("done")}


def x_tip_item(t, label):
    key = {"tips": "tips", "copasta": "cs", "m365copilot": "mc"}.get(t.get("series", "tips"), "tips")
    f = t["folder"]
    return {
        "id": f"x-{key}-{t['vol']}", "platform": "x", "label": label,
        "title": t["title"], "body": t["body"],
        "openUrl": bxb.intent(t["body"]), "openLabel": "Xで開く（本文入り）",
        "imagePath": str(bxb.POST_IMG_ROOT / f), "imageNote": "フォルダ（開いて Ctrl+A で全部選ぶ）",
        "when": "朝〜昼のどこかで",
    }


def pick_x_tip(tips, series, done):
    def queue(s):
        q = [t for t in tips if t.get("series", "tips") == s and t.get("status") != "posted"]
        if s == "tips":
            q.sort(key=lambda t: (t.get("order", 10000), -t["vol"]))
        else:
            q.sort(key=lambda t: -t["vol"])
        return [t for t in q if x_tip_item(t, "")["id"] not in done]
    for s in (series, "tips"):
        q = queue(s)
        if q:
            return q[0]
    return None


def announce_event(today):
    """次の PA45 の回（今日以降）。upcoming-event.json → announce-events.json の順で探す。"""
    up = {}
    f = ROOT / "data" / "config" / "upcoming-event.json"
    if f.exists():
        up = json.loads(f.read_text(encoding="utf-8"))
    evs = []
    af = ROOT / "data" / "announce-events.json"
    if af.exists():
        evs = json.loads(af.read_text(encoding="utf-8"))["events"]
    if up.get("vol"):
        manual = next((e for e in evs if int(e.get("vol", -1)) == int(up["vol"])), None)
        evs = evs + [manual or bxb.derive_announce_from_upcoming(up)]
    ahead = [e for e in evs if e.get("date") and e["date"] >= today.isoformat() and e.get("connpass_url")]
    return min(ahead, key=lambda e: e["date"]) if ahead else None


def announce_items(today):
    ev = announce_event(today)
    if not ev:
        return []
    d = date.fromisoformat(ev["date"])
    slots = []
    if today == d - timedelta(days=d.weekday()) and today != d:   # 開催週の月曜
        slots = [2]
    elif today == d:
        slots = [3, 4]
    out = []
    for slot, body in bxb.ann_bodies(ev):
        if slot["n"] in slots:
            out.append({
                "id": f"x-ann-{ev['vol']}-{slot['n']}", "platform": "x", "label": f"PA45 第{ev['vol']}回 告知",
                "title": slot["when"], "body": body,
                "openUrl": bxb.intent(body), "openLabel": "Xで開く（本文入り）",
                "when": {2: "今日のうちに", 3: "お昼ごろ", 4: "20:00ごろ（開催15分前）"}[slot["n"]],
            })
    return out


def li_queue(items):
    first = [p for p in items if p.get("group") == "mct"]
    blog = [p for p in items if p.get("group") == "blog"]
    tips = [p for p in items if p.get("group") == "tips"]
    rest_mct = first[1:]
    q = first[:1]
    mix = []
    for i in range(max(len(blog), len(tips))):
        if i < len(blog):
            mix.append(blog[i])
        if i < len(tips):
            mix.append(tips[i])
    for i, p in enumerate(mix, 1):
        q.append(p)
        if i % 4 == 0 and rest_mct:
            q.append(rest_mct.pop(0))
    q += rest_mct
    q += [p for p in items if p.get("group") not in ("mct", "blog", "tips", "profile", "announce")]
    return q


def li_item(p, tokens):
    body = bxb._apply_tokens(p["body"], tokens)
    it = {"id": f"li-{p['no']}", "platform": "linkedin", "label": p.get("angle", ""),
          "title": p["title"], "body": body,
          "openUrl": bxb.LI_COMPOSE, "openLabel": "LinkedInを開く", "when": "朝〜夜のどこかで"}
    if p.get("tips_folder"):
        it["imagePath"] = str(bxb.POST_IMG_ROOT / p["tips_folder"])
        it["imageNote"] = "フォルダ（開いて Ctrl+A で全部選ぶ）"
    elif p.get("image_file"):
        it["imagePath"] = str(ROOT.parent / p["image_file"])
        it["imageNote"] = "画像"
    return it


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--done")
    ap.add_argument("--date")
    ap.add_argument("--out")
    a = ap.parse_args()
    now = datetime.now(JST)
    today = date.fromisoformat(a.date) if a.date else now.date()
    done = load_done(a.done)
    wd = today.weekday()

    items = []
    tips = json.loads((ROOT / "data" / "x-tips-board.json").read_text(encoding="utf-8"))["items"]
    series = {1: "copasta", 4: "m365copilot"}.get(wd, "tips")
    t = pick_x_tip(tips, series, done)
    if t:
        items.append(x_tip_item(t, {"tips": "Power Automate Tips", "copasta": "コパスタ",
                                    "m365copilot": "M365 Copilot"}[t.get("series", "tips")]))
    # 画像は X投稿ボードを作るときに pa45-x-images へまとめられる。無ければここで揃える
    if t:
        img1, rel1, img2, rel2, extras = bxb.tip_images(t["folder"])
        for i in [img1, img2] + [e[0] for e in extras]:
            bxb.sync_post_image(i, bxb.POST_IMG_ROOT / t["folder"])
    items += announce_items(today)

    if wd in (0, 4):
        lid = json.loads((ROOT / "data" / "linkedin-board.json").read_text(encoding="utf-8"))
        q = [p for p in li_queue(lid.get("items", [])) if f"li-{p['no']}" not in done]
        if q:
            p = q[0]
            if p.get("tips_folder"):
                img1, rel1, img2, rel2, extras = bxb.tip_images(p["tips_folder"])
                for i in [img1, img2] + [e[0] for e in extras]:
                    bxb.sync_post_image(i, bxb.POST_IMG_ROOT / p["tips_folder"])
            items.append(li_item(p, bxb._insight_tokens()))

    out = {"date": today.isoformat(), "generatedAt": f"{today.month}/{today.day}({WD[wd]}) {now:%H:%M}",
           "items": items}
    s = json.dumps(out, ensure_ascii=False, indent=1)
    if a.out:
        Path(a.out).write_text(s + "\n", encoding="utf-8")
    sys.stdout.write(s + "\n")


if __name__ == "__main__":
    main()

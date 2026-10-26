r"""
LinkedIn 投稿用の画像（1200x627）を作る。data/linkedin-board.json のうち、
画像が無い投稿（tips_folder も image_file も無いもの・プロフィールは除く）に1枚ずつ作って image_file を書き込む。
画像の見出しは item の image_title（
 で改行位置を決める・1行は全角13字まで）。無ければ title を自動で折り返す。

  python scripts/make-linkedin-images.py          # 画像が無いものだけ作る
  python scripts/make-linkedin-images.py --all    # 自動で作った画像をすべて作り直す
  python scripts/make-linkedin-images.py --no 20  # 1件だけ作り直す

出力：Documents\pa45-x-images\linkedin\li-NN.png（X の画像と同じ置き場。公開リポジトリには入れない）
デザインは X ヘッダー v5 と同じ背景＋MCT バッジ。文字は枠に収まるまで自動で小さくし、はみ出したら NG を出す。
"""
import argparse
import base64
import html
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT.parent
OUT_DIR = DOCS / "pa45-x-images" / "linkedin"
BOARD = ROOT / "data" / "linkedin-board.json"
BADGE_FILE = DOCS / "mct-badge" / "mct-badge-official.png"
W, H = 1200, 627

# 区分ごとの札と、タイトルの下に出す1行（item に image_label / image_sub があればそちらを使う）
LABEL = {"mct": "Microsoft 認定トレーナー", "blog": "ブログ", "tips": "Power Automate Tips",
         "announce": "PA45 開催のお知らせ"}
SUB = {"mct": "Power Automate・Copilot Studio・M365 Copilot の研修とハンズオン",
       "blog": "automate136.com", "tips": "作り方は本文に",
       "announce": "オンライン・参加無料・見るだけの参加もOK"}

HTML = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@500;700;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
#c{{position:relative;width:{W}px;height:{H}px;overflow:hidden;font-family:"Noto Sans JP",sans-serif;color:#0b1f3a;
  background:linear-gradient(120deg,#d9ecfd 0%,#cfe4fb 45%,#d6f1fb 100%)}}
.blob{{position:absolute;border-radius:50%;filter:blur(60px)}}
#lab{{position:absolute;left:72px;top:64px;font-size:26px;font-weight:700;color:#fff;background:#0b4a8f;
  border-radius:999px;padding:6px 22px}}
#box{{position:absolute;left:72px;top:140px;width:820px;height:300px;display:flex;flex-direction:column;justify-content:center}}
#t{{font-size:64px;font-weight:900;line-height:1.3;overflow-wrap:anywhere}}
#t.pre{{white-space:pre;overflow-wrap:normal}}
#s{{margin-top:22px;font-size:30px;font-weight:700;color:#0b4a8f;line-height:1.4}}
#foot{{position:absolute;left:72px;bottom:56px;font-size:26px;font-weight:700;color:#1b2f4a}}
#b{{position:absolute;right:56px;top:50%;transform:translateY(-50%);width:230px;height:230px}}
</style></head><body><div id="c">
<div class="blob" style="left:-10%;top:40%;width:40%;height:110%;background:#9aa8ff;opacity:.7"></div>
<div class="blob" style="left:25%;top:-45%;width:45%;height:110%;background:#7cc4ff;opacity:.5"></div>
<div class="blob" style="left:60%;top:30%;width:40%;height:110%;background:#7ee7f7;opacity:.5"></div>
<div id="lab">{label}</div>
<div id="box"><div id="t" class="{tcls}">{title}</div><div id="s">{sub}</div></div>
<div id="foot">Haru ｜ Microsoft 認定トレーナー（MCT）</div>
<img id="b" src="{badge}">
</div></body></html>"""

# タイトルが枠（#box）に収まるまで文字を小さくする。40px でも収まらなければ NG を返す
FIT = """() => {
  const box = document.getElementById('box'), t = document.getElementById('t');
  let px = 64;
  while (px > 40 && (box.scrollHeight > box.clientHeight + 1 || t.scrollWidth > t.clientWidth + 1)) {
    px -= 2; t.style.fontSize = px + 'px';
  }
  const over = box.scrollHeight > box.clientHeight + 1 || t.scrollWidth > t.clientWidth + 1;
  return {px, over};
}"""


def needs_image(p, args):
    if p.get("group") == "profile" or p.get("tips_folder"):
        return False
    if args.no is not None:
        return p["no"] == args.no
    auto = str(p.get("image_file", "")).startswith("pa45-x-images/linkedin/")
    if args.all:
        return auto or not p.get("image_file")
    return not p.get("image_file") or (auto and not (DOCS / p["image_file"]).exists())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--no", type=int)
    args = ap.parse_args()

    data = json.loads(BOARD.read_text(encoding="utf-8"))
    todo = [p for p in data["items"] if needs_image(p, args)]
    if not todo:
        print("画像を作る投稿はありません")
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    badge = "data:image/png;base64," + base64.b64encode(BADGE_FILE.read_bytes()).decode()
    ng = 0
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        page = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        for p in todo:
            g = p.get("group", "")
            page.set_content(HTML.format(
                W=W, H=H, badge=badge,
                label=html.escape(p.get("image_label") or LABEL.get(g, p.get("angle", ""))),
                title=html.escape(p.get("image_title") or p["title"]),
                tcls="pre" if p.get("image_title") else "",
                sub=html.escape(p.get("image_sub") or SUB.get(g, ""))))
            page.wait_for_timeout(1500)
            fit = page.evaluate(FIT)
            out = OUT_DIR / f"li-{p['no']:02d}.png"
            tmp = out.with_suffix(".2x.png")
            page.screenshot(path=str(tmp))
            Image.open(tmp).resize((W, H), Image.LANCZOS).save(out, optimize=True)
            tmp.unlink()
            p["image_file"] = out.relative_to(DOCS).as_posix()
            mark = "NG" if fit["over"] else "OK"
            ng += fit["over"]
            print(f"[{mark}] LI-{p['no']:02d} {fit['px']}px  {out}")
        br.close()
    BOARD.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if ng:
        print(f"{ng}件はタイトルが長すぎて収まりません。item に image_title（短い見出し）を足して作り直してください。")
    return 1 if ng else 0


if __name__ == "__main__":
    sys.exit(main())

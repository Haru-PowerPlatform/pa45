#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""LT登壇レポートのアイキャッチ生成（大阪版 nandemo-osaka-eyecatch.png と同じデザイン）。
1200x630 を force-device-scale-factor=2 で 2400x1260 に描画 → WPメディアへ上げて Post 4392 の featured に設定。
  python make_eyecatch.py          # PNG生成のみ
  python make_eyecatch.py --push   # 生成→WPアップ→featured設定
"""
import base64, subprocess, pathlib, sys, requests, os

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
AVATAR = ROOT / "assets" / "img" / "haru-avatar.png"
OUT_PNG = HERE / "assets" / "nandemo-lt-eyecatch.png"
POST_ID = 4392
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

avatar_b64 = base64.b64encode(AVATAR.read_bytes()).decode()

HTML = """<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1200px;height:630px;overflow:hidden;}
.card{position:relative;width:1200px;height:630px;
  background:radial-gradient(120% 130% at 78% 45%,#28407a 0%,#16264c 42%,#0c1730 100%);
  font-family:'Yu Gothic UI','Meiryo','Segoe UI',sans-serif;overflow:hidden;}
.stripes{position:absolute;left:-40px;top:-60px;height:760px;width:220px;transform:rotate(0deg);}
.stripes i{position:absolute;top:0;height:760px;transform:skewX(-18deg);border-radius:6px;}
.s1{left:22px;width:20px;background:#7c5cff;opacity:.9;}
.s2{left:52px;width:12px;background:#3b82f6;opacity:.85;}
.s3{left:74px;width:34px;background:linear-gradient(#c8922e,#8a5a12);opacity:.9;}
.pill{position:absolute;left:70px;top:74px;padding:16px 34px;border-radius:44px;
  background:linear-gradient(135deg,#f6b45a,#ef9d7a);color:#15233f;font-weight:800;font-size:33px;letter-spacing:.02em;}
.ev{position:absolute;left:74px;top:168px;color:#eaf1ff;font-weight:800;font-size:41px;letter-spacing:.01em;}
.cap{position:absolute;left:76px;top:236px;color:#8fb4e6;font-weight:700;font-size:24px;letter-spacing:.42em;}
.ttl{position:absolute;left:70px;top:290px;color:#fff;font-weight:900;font-size:96px;line-height:1.12;letter-spacing:.005em;
  text-shadow:0 3px 18px rgba(0,0,0,.35);}
.ttl em{font-style:normal;}
.sub{position:absolute;left:74px;top:520px;padding:15px 26px;border-radius:14px;
  background:rgba(20,32,58,.62);border:1px solid rgba(120,150,200,.25);
  color:#e7eefb;font-weight:800;font-size:32px;letter-spacing:.01em;}
.ava{position:absolute;right:96px;top:170px;width:404px;height:404px;border-radius:50%;
  padding:8px;background:conic-gradient(from 210deg,#f6b45a,#ef7a9d,#7c5cff,#3b82f6,#f6b45a);}
.ava img{width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;}
</style></head><body>
<div class="card">
  <div class="stripes"><i class="s1"></i><i class="s2"></i><i class="s3"></i></div>
  <div class="pill">登壇レポート</div>
  <div class="ev">なんでもCopilot LT大会（オンライン）</div>
  <div class="cap">コミュニティ登壇 ・ LT</div>
  <div class="ttl">会議を、<br><em>コスト化する。</em></div>
  <div class="sub">Copilot × Power Automate で、7アクションのBot。</div>
  <div class="ava"><img src="data:image/png;base64,__AVA__"></div>
</div>
</body></html>""".replace("__AVA__", avatar_b64)

def main():
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    html_path = HERE / "_eyecatch.html"
    html_path.write_text(HTML, encoding="utf-8")
    url = "file:///" + str(html_path).replace("\\", "/")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--window-size=1200,630", "--force-device-scale-factor=2",
                    "--default-background-color=00000000",
                    f"--screenshot={OUT_PNG}", url], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    html_path.unlink(missing_ok=True)
    print("PNG:", OUT_PNG, OUT_PNG.stat().st_size, "bytes")

    if "--push" not in sys.argv:
        print("（生成のみ。--push でWPアップ＋featured設定）")
        return

    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1); env[k.strip()] = v.strip()
    WP = env["WP_URL"].rstrip("/")
    auth = "Basic " + base64.b64encode(f"{env['WP_USER']}:{env['WP_PASS']}".encode()).decode()
    mh = {"Authorization": auth, "Content-Disposition": 'attachment; filename="nandemo-lt-eyecatch.png"',
          "Content-Type": "image/png"}
    r = requests.post(f"{WP}/wp-json/wp/v2/media", headers=mh, data=OUT_PNG.read_bytes(), timeout=180)
    r.raise_for_status(); mid = r.json()["id"]; print("MEDIA", mid)
    requests.post(f"{WP}/wp-json/wp/v2/media/{mid}", headers={"Authorization": auth},
                  json={"alt_text": "なんでもCopilot LT大会 登壇レポート｜会議をコスト化するBot",
                        "title": "なんでもCopilot LT大会 登壇レポート"}, timeout=60)
    r = requests.post(f"{WP}/wp-json/wp/v2/posts/{POST_ID}", headers={"Authorization": auth},
                      json={"featured_media": mid, "status": "draft"}, timeout=60)
    r.raise_for_status()
    print("SET featured", mid, "on", POST_ID, "status=", r.json()["status"])

if __name__ == "__main__":
    main()

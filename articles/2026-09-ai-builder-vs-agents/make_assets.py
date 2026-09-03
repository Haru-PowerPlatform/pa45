#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""「AI Builder／エージェント ビルダー／Copilot Studio」比較記事の画像を作る。

  python make_assets.py          # PNG生成のみ（assets/ に出力）

生成物:
  assets/eyecatch.png    1200x630  コパスタ共通デザイン＋はる／CS45バッジ
  assets/fig-layers.png  1040x606  3つは層がちがう（部品／軽量／本格）
  assets/fig-money.png   1040x558  お金は「操作」で決まる

※ PNGを直接いじらない。直すときはこのファイル内のHTML文字列を編集して作り直す。
※ レンダリング用の中間HTMLは毎回作って消す（アバターをbase64で埋めるため2MB超になる）。
"""
import base64, subprocess, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "assets"
AVATAR = ROOT / "assets" / "img" / "haru-avatar.png"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

avatar_b64 = base64.b64encode(AVATAR.read_bytes()).decode()

BASE = """*{margin:0;padding:0;box-sizing:border-box;}
html,body{overflow:hidden;}
body{font-family:'Yu Gothic UI','Meiryo','Segoe UI',sans-serif;}
"""

# ---------------------------------------------------------------- アイキャッチ
EYECATCH = """<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
__BASE__
html,body{width:1200px;height:630px;}
.card{position:relative;width:1200px;height:630px;overflow:hidden;
  background:radial-gradient(125% 135% at 76% 40%,#4c2f8f 0%,#33206b 44%,#1b1140 100%);}
.stripes{position:absolute;left:-40px;top:-60px;height:780px;width:220px;}
.stripes i{position:absolute;top:0;height:780px;transform:skewX(-18deg);border-radius:6px;}
.s1{left:22px;width:20px;background:#a78bfa;opacity:.92;}
.s2{left:52px;width:12px;background:#38bdf8;opacity:.8;}
.s3{left:74px;width:34px;background:linear-gradient(#c8922e,#8a5a12);opacity:.9;}
.pill{position:absolute;left:70px;top:62px;padding:15px 32px;border-radius:44px;
  background:linear-gradient(135deg,#c4b5fd,#a78bfa);color:#221046;font-weight:800;font-size:37px;letter-spacing:.02em;}
.cap{position:absolute;left:76px;top:156px;color:#b5a5e6;font-weight:700;font-size:23px;letter-spacing:.4em;}
.ttl{position:absolute;left:70px;top:206px;color:#fff;font-weight:900;font-size:80px;line-height:1.2;
  letter-spacing:.005em;text-shadow:0 3px 18px rgba(0,0,0,.35);}
.ttl em{font-style:normal;color:#fbbf6b;}
.sub{position:absolute;left:74px;top:496px;padding:14px 26px;border-radius:14px;
  background:rgba(28,18,60,.62);border:1px solid rgba(150,130,210,.28);
  color:#ece6fb;font-weight:800;font-size:29px;}
.haru-badge{position:absolute;right:30px;bottom:24px;display:flex;flex-direction:column;align-items:center;gap:10px;}
.haru-badge img{width:92px;height:92px;border-radius:50%;object-fit:cover;border:4px solid #fff;
  box-shadow:0 4px 14px rgba(0,0,0,.35);}
.haru-badge span{background:#f3ecff;color:#5B21B6;font-weight:800;font-size:24px;padding:5px 18px;border-radius:999px;}
</style></head><body>
<div class="card">
  <div class="stripes"><i class="s1"></i><i class="s2"></i><i class="s3"></i></div>
  <div class="pill">Copilot Studio &times; 使い分け</div>
  <div class="cap">3つのAIを1枚で整理</div>
  <div class="ttl">AI Builder と<br><em>2つのエージェント</em></div>
  <div class="sub">どれで作るか。お金はどこから発生するか。</div>
  <div class="haru-badge"><img src="data:image/png;base64,__AVA__"><span>はる／CS45</span></div>
</div>
</body></html>"""

# ---------------------------------------------------------------- 図解1：層
FIG_LAYERS = """<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
__BASE__
html,body{width:1040px;height:606px;background:#fff;}
.wrap{width:1040px;height:606px;padding:32px 34px;background:#fff;}
.hd{font-size:29px;font-weight:900;color:#2c2340;margin-bottom:6px;}
.sh{font-size:18px;color:#6b6480;margin-bottom:22px;line-height:1.6;}
.cols{display:flex;gap:15px;}
.col{flex:1;border-radius:16px;padding:18px 18px 20px;border:2px solid;background:#fff;}
.col.a{border-color:#bfd4f5;background:#f4f8fe;}
.col.b{border-color:#b8ded9;background:#f2faf9;}
.col.c{border-color:#d6c9f5;background:#f8f5fe;}
.tag{display:inline-block;font-size:15.5px;font-weight:800;padding:5px 14px;border-radius:999px;margin-bottom:11px;}
.a .tag{background:#dce9fb;color:#1e40af;}
.b .tag{background:#d5eeeb;color:#0d6b68;}
.c .tag{background:#e9e0fb;color:#5b21b6;}
.nm{font-size:24px;font-weight:900;line-height:1.35;margin-bottom:11px;min-height:64px;}
.a .nm{color:#1e40af;} .b .nm{color:#0d6b68;} .c .nm{color:#5b21b6;}
.dsc{font-size:17px;color:#3f3a4d;line-height:1.72;margin-bottom:14px;min-height:118px;}
.mt{border-top:1px dashed #cfc9dd;padding-top:11px;font-size:15px;color:#5b5470;line-height:1.7;}
.mt b{color:#2c2340;}
.foot{margin-top:18px;background:#f6f4fb;border-left:6px solid #8b5cf6;border-radius:8px;
  padding:13px 20px;font-size:18px;color:#3f3557;line-height:1.7;font-weight:700;}
</style></head><body>
<div class="wrap">
  <div class="hd">3つは「並ぶ製品」ではなく、層がちがう</div>
  <div class="sh">同じ表に並べると比べにくいのは、そもそも役割の大きさが別だから。</div>
  <div class="cols">
    <div class="col a">
      <span class="tag">部品</span>
      <div class="nm">AI Builder</div>
      <div class="dsc">フローやアプリの途中に差し込む、入力から出力を返すAI機能。会話はしない。</div>
      <div class="mt">作る場所：<b>Power Automate / Power Apps</b><br>使う人：フローを作る人</div>
    </div>
    <div class="col b">
      <span class="tag">軽量エージェント</span>
      <div class="nm">エージェント<br>ビルダー</div>
      <div class="dsc">Copilot Chat の中で会話しながら作る、自分と小さなチーム向けのQ&amp;A係。</div>
      <div class="mt">作る場所：<b>Microsoft 365 Copilot の中</b><br>使う人：情報を扱う人</div>
    </div>
    <div class="col c">
      <span class="tag">本格エージェント</span>
      <div class="nm">Copilot Studio</div>
      <div class="dsc">専用ポータルで作る、部門・全社・社外向けのエージェント。業務そのものを動かす。</div>
      <div class="mt">作る場所：<b>copilotstudio.microsoft.com</b><br>使う人：作成者・開発者</div>
    </div>
  </div>
  <div class="foot">左から右へ、できることと管理の重さが増える。迷ったら左から始めて、足りなくなったら右へ移す。</div>
</div>
</body></html>"""

# ---------------------------------------------------------------- 図解2：お金
FIG_MONEY = """<!doctype html><html lang="ja"><head><meta charset="utf-8"><style>
__BASE__
html,body{width:1040px;height:558px;background:#fff;}
.wrap{width:1040px;height:558px;padding:32px 34px;background:#fff;}
.hd{font-size:29px;font-weight:900;color:#2c2340;margin-bottom:6px;}
.sh{font-size:18px;color:#6b6480;margin-bottom:22px;line-height:1.6;}
table{width:100%;border-collapse:collapse;}
th,td{padding:15px 16px;text-align:left;vertical-align:top;font-size:17px;line-height:1.72;border-bottom:1px solid #e8e4f2;}
thead th{font-size:19.5px;font-weight:900;padding:12px 16px;border-bottom:3px solid #ddd6ef;}
thead th.a{color:#1e40af;background:#f4f8fe;}
thead th.b{color:#0d6b68;background:#f2faf9;}
thead th.c{color:#5b21b6;background:#f8f5fe;}
thead th.k{background:#fafafb;}
tbody th{width:196px;font-size:16px;font-weight:800;color:#5b5470;background:#fafafb;}
tbody th.pd{color:#a3341f;}
.free{color:#1f7a4d;font-weight:800;}
.paid{color:#a3341f;font-weight:800;}
tbody tr:last-child th,tbody tr:last-child td{border-bottom:none;}
.foot{margin-top:20px;background:#fffdf5;border:2px solid #ffd54f;border-radius:10px;
  padding:14px 20px;font-size:18px;color:#4a4030;line-height:1.72;}
.foot b{color:#b4700a;}
</style></head><body>
<div class="wrap">
  <div class="hd">お金は「土台」ではなく「操作」で決まる</div>
  <div class="sh">3つとも、作るところまでは無料。動かした内容によって課金される。</div>
  <table>
    <thead><tr><th class="k"></th><th class="a">AI Builder</th><th class="b">エージェント ビルダー</th><th class="c">Copilot Studio</th></tr></thead>
    <tbody>
      <tr><th>作る・試す</th>
        <td class="free">無料</td><td class="free">無料</td><td class="free">無料</td></tr>
      <tr><th>ただで動く範囲</th>
        <td>Premiumライセンスに付く<br>シードクレジット</td>
        <td>公開Webサイトだけを<br>根拠にするとき</td>
        <td>M365 Copilot保有者の<br>社内利用</td></tr>
      <tr><th class="pd">お金がかかる瞬間</th>
        <td class="paid">フローやアプリで<br>実行したとき</td>
        <td class="paid">社内データを<br>読ませたとき</td>
        <td class="paid">公開後に<br>動かされたとき</td></tr>
    </tbody>
  </table>
  <div class="foot"><b>共通の通貨は Copilot クレジット。</b>ただし Power Automate のクラウドフローは対象外で、これまで通り Power Automate のライセンスで動く。</div>
</div>
</body></html>"""

FIGS = [
    ("eyecatch",   EYECATCH,   1200, 630),
    ("fig-layers", FIG_LAYERS, 1040, 606),
    ("fig-money",  FIG_MONEY,  1040, 558),
]


def render(name, html, w, h):
    OUT.mkdir(parents=True, exist_ok=True)
    src = html.replace("__BASE__", BASE).replace("__AVA__", avatar_b64)
    tmp = HERE / f"_{name}.html"
    tmp.write_text(src, encoding="utf-8")
    png = OUT / f"{name}.png"
    url = "file:///" + str(tmp).replace("\\", "/")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={w},{h}", "--force-device-scale-factor=2",
                    f"--screenshot={png}", url],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp.unlink(missing_ok=True)   # 中間HTMLは残さない（アバターのbase64で2MB超になるため）
    print(f"  {png.name}: {png.stat().st_size:,} bytes ({w}x{h} @2x)")


def main():
    print("PNG生成:")
    for name, html, w, h in FIGS:
        render(name, html, w, h)
    print("図解・アイキャッチを直すときは、このファイル内の EYECATCH / FIG_LAYERS / FIG_MONEY を編集する")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""PA45 各回レポート（automate136・カテゴリ93）の生成キット。第24回（Post 4383）の型をそのまま再現する。

各回の volNN.py が本文の中身（dict）だけを持ち、ここで
  数字（参加者・アンケート・累計）＝ data/ から取り直す（架空禁止）
  画像＝ slides/vol-NN/assets/*.png を WP メディアへ（sha でキャッシュ）
  アイキャッチ＝ articles/_eyecatch_kit.py のカテゴリ93
  下書き＝ status=draft 固定（公開ははる本人）
を組み立てる。  python volNN.py          … article.html だけ作る
                python volNN.py --push   … WP の下書きを作成／更新
"""
import glob, hashlib, html, json, pathlib, re, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
ART = HERE.parent
ROOT = ART.parent
sys.path.insert(0, str(ART))
sys.path.insert(0, str(HERE))
from _howtokit import _req  # noqa: E402
from _workcta import work_cta  # noqa: E402
from _spacing import CSS as SPACING_CSS  # noqa: E402
from _report_css import MAIN as CSS_MAIN, SUMMARY as CSS_SUM  # noqa: E402

PUSH = "--push" in sys.argv
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE = "https://haru-powerplatform.github.io/pa45"
E = html.escape


# ---------------------------------------------------------------- 数字（data/ から）
def _json(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def activity(vol):
    for f in glob.glob(str(ROOT / "data" / "activities" / f"*-pa45-vol{vol}.json")):
        if "video" not in f:
            return _json(f)
    return None


def video_url(vol):
    for f in glob.glob(str(ROOT / "data" / "activities" / f"*-video-pa45-vol{vol}.json")):
        return _json(f)["evidence"]["video"]
    return None


def survey(vol):
    return _json(ROOT / "data" / "surveys" / f"vol-{vol:02d}.json")


def totals(vol):
    """第1回〜第vol回の累計（insights.json と同じ：理解・役立ちは回答数で重み付け）。"""
    n = ppl = resp = 0
    u = us = 0.0
    for v in range(1, vol + 1):
        a = activity(v)
        if a:
            n += 1
            ppl += a.get("participants", 0) or 0
        f = ROOT / "data" / "surveys" / f"vol-{v:02d}.json"
        if f.exists():
            s = _json(f)
            resp += s["total_responses"]
            u += s["understanding_pct"] * s["total_responses"]
            us += s["usefulness_pct"] * s["total_responses"]
    return dict(sessions=n, participants=ppl, responses=resp, und=round(u / resp, 1), use=round(us / resp, 1))


def slide_count(vol):
    s = (ROOT / "slides" / f"vol-{vol}" / "index.html").read_text(encoding="utf-8")
    return len(re.findall(r'<section[^>]*class="[^"]*\bslide\b', s))


# ---------------------------------------------------------------- 画像
class Media:
    def __init__(self, state):
        self.state = state
        self.sizes = {}

    def url(self, key, path, fname):
        from PIL import Image
        b = pathlib.Path(path).read_bytes()
        sha = hashlib.sha1(b).hexdigest()
        self.sizes[key] = Image.open(path).size
        rec = self.state["media"].get(key)
        if rec and rec["sha"] == sha:
            return rec["url"], rec["id"]
        if not PUSH:
            return pathlib.Path(path).as_uri(), None
        j = _req("POST", "/wp-json/wp/v2/media", raw=b,
                 headers={"Content-Type": "image/png", "Content-Disposition": f'attachment; filename="{fname}"'})
        self.state["media"][key] = {"id": j["id"], "url": j["source_url"], "sha": sha}
        return j["source_url"], j["id"]


_INJECT = """<style>.toc,.toc-toggle,.deck-header,.deck-footer{display:none!important;}
html,body{margin:0!important;padding:0!important;background:#fff!important;overflow:hidden!important;}
.slide{margin:0!important;box-shadow:none!important;border-radius:0!important;}</style>
<script>window.addEventListener('load',function(){var s=document.querySelectorAll('.slide');
s.forEach(function(e,i){e.style.display=(i===__N__?'flex':'none');});document.body.classList.add('toc-collapsed');});</script>"""


def render_slide(vol, out, n=1):
    """スライドの n 枚目（1始まり）だけを 1280x720・2倍で撮る（mvp-application/render-slide-pngs.py と同じやり方）。"""
    d = ROOT / "slides" / f"vol-{vol}"
    src = (d / "index.html").read_text(encoding="utf-8")
    tmp = d / f"_render_report_{n}.html"
    tmp.write_text(src.replace("</body>", _INJECT.replace("__N__", str(n - 1)) + "</body>"), encoding="utf-8")
    try:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1280,720",
                        "--force-device-scale-factor=2", f"--screenshot={out}", tmp.as_uri()],
                       check=True, capture_output=True, timeout=90)
    finally:
        tmp.unlink(missing_ok=True)


# ---------------------------------------------------------------- 本文の部品
def para(lines):
    """関連する文を <br> で1段落に束ねる（PA45 レポートの型）。"""
    if isinstance(lines, str):
        lines = [lines]
    return "<p>" + "<br>".join(lines) + "</p>"


def shot_html(url, size, cap):
    w, h = size
    alt = E(re.sub(r"<[^>]+>", "", cap), quote=True)
    return (f'<figure class="mb-shot"><span class="sh-tag">実際の画面</span><div class="sh-frame">'
            f'<a href="{url}" target="_blank" rel="noopener"><img src="{url}" alt="{alt}" width="{w}" height="{h}" loading="lazy" /></a>'
            f'</div><figcaption>▲ {cap}</figcaption></figure>')


def step_html(no, title, text):
    return f'<div class="mb-step"><div class="st-ttl"><span class="st-no">{no}</span>{title}</div><p>{text}</p></div>'


def build(cfg):
    vol = cfg["vol"]
    here = pathlib.Path(cfg["here"])
    state_f = here / "post_state.json"
    state = _json(state_f) if state_f.exists() else {"post_id": None, "media": {}}
    m = Media(state)
    act, sv, tot = activity(vol), survey(vol), totals(vol)
    vurl = video_url(vol)
    vid = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", vurl).group(1) if vurl else None
    ins = f"{BASE}/achievements/insights/vol-{vol}.html"
    sdir = ROOT / "slides" / f"vol-{vol}" / "assets"

    def shot(name, cap):
        u, _ = m.url(f"shot-{name}", sdir / f"{name}.png", f"pa45-vol{vol}-{name}.png")
        return shot_html(u, m.sizes[f"shot-{name}"], cap)

    o = []
    o.append('<div class="mb-body">')
    o.append(f'<p class="cs-preface">&#x1f4dd; この記事は、PA45 第{vol}回でつくったフローをあとから見返せるようにまとめたものです。<br>'
             '当日参加できなかった方も、この記事だけで同じフローが作れます。<br>画面や仕様は更新が続きます。最新の情報は '
             '<a href="https://learn.microsoft.com/ja-jp/power-automate/" target="_blank" rel="noopener">Microsoft 公式（Microsoft Learn）</a>をご確認ください。</p>')
    o.append('<!-- pa45:why -->\n<div class="mb-intro pa45"><b>&#x1f9ed; なぜ毎週やっているのか</b><br>2022年から、Power Automate for Desktop とクラウドフローの社内展開に取り組んできました。<br>'
             'そこで接してきたのは、ITが専門ではない人や、自動化にはじめて触れる人がほとんどです。<br>どこで手が止まるかは、だいたい同じところでした。<br><br>'
             'PA45を毎週続けているのは、その手前のハードルを下げたいからです。<br>「これなら自分にもできそう」と思えるところまで持っていければ、使う人の裾野は広がります。</div>')
    o.append(f'<!-- pa45:survey-top -->\n<div class="mb-point"><b>&#x1f4ca; この回のアンケート結果</b><br>参加者 <b>{act["participants"]}名</b> ／ '
             f'アンケート回答 <b>{sv["total_responses"]}件</b> ／ 理解できた <b>{sv["understanding_pct"]:.1f}%</b> ／ 役立ちそう <b>{sv["usefulness_pct"]:.1f}%</b><br>'
             f'<a href="{ins}" target="_blank" rel="noopener">第{vol}回のアンケート結果をぜんぶ見る</a>（選択肢の内訳も、自由記述も、いただいたまま公開しています）</div>')
    o.append('<p class="mb-lead">' + "<br>".join(cfg["lead"]) + "</p>")
    if vid:
        o.append(f'<div class="mb-ytcard"><a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="PA45 第{vol}回 ハンズオン録画" loading="lazy"></a>'
                 f'<div class="yt-body"><p class="yt-ttl">&#x25b6; 当日のハンズオン録画</p><p>手元で止めながら進めたい方は、動画とあわせてどうぞ。</p>'
                 f'<a class="mb-btn yt" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">この回の録画をYouTubeで見る</a></div></div>')

    for sec in cfg["sections"]:
        o.append(f"\n<h2>{sec['h2']}</h2>")
        for blk in sec["body"]:
            kind = blk[0]
            if kind == "p":
                o.append(para(blk[1]))
            elif kind == "shot":
                o.append(shot(blk[1], blk[2]))
            elif kind == "step":
                o.append(step_html(*blk[1:]))
            elif kind == "code":
                o.append(f'<pre class="mb-code"><code>{E(blk[1])}</code></pre>')
            elif kind == "html":
                o.append(blk[1])

    # 当日のスライド（1枚目を撮ってカードに）
    sp = here / "assets" / "slide-01.png"
    sp.parent.mkdir(exist_ok=True)
    if not sp.exists():
        render_slide(vol, sp, cfg.get("slide", 1))
    su, _ = m.url("slide-01", sp, f"pa45-vol{vol}-slide-01.png")
    n_sl = slide_count(vol)
    o.append("\n<h2>当日のスライド</h2>")
    o.append(f'<div class="mb-slidecard"><a href="{BASE}/slides/vol-{vol}/" target="_blank" rel="noopener"><img src="{su}" alt="PA45 第{vol}回 スライド" loading="lazy"></a>'
             f'<div class="sc-body"><p class="sc-ttl">&#x1f5a5;&#xfe0f; 当日のスライド（全{n_sl}枚）</p><p>ブラウザでそのまま開けます。手順書と完成フローのダウンロードは資料リンク集にあります。</p>'
             f'<a class="mb-btn pa" href="{BASE}/slides/vol-{vol}/" target="_blank" rel="noopener">スライドを開く</a> '
             f'<a class="mb-btn pa" href="{BASE}/slides/vol-{vol}/links.html" target="_blank" rel="noopener">資料リンク集</a></div></div>')

    # まとめ
    o.append("<!-- pa45:summary-v2 -->\n\n<h2>まとめ</h2>")
    o.append(f"<style>{CSS_SUM}</style>")
    o.append('<div class="mb-sum">')
    o.append('<h3 class="sum-h">今日のポイント</h3>')
    o.append('<div class="mb-check"><ul>' + "".join(f"<li>{x}</li>" for x in cfg["points"]) + "</ul></div>")
    o.append('<h3 class="sum-h">参加者アンケート：この45分でできるようになったこと</h3>\n<!-- pa45:survey-bottom -->')
    n = sv["total_responses"]
    cds = sorted(sv["can_do"].items(), key=lambda kv: -kv[1])
    o.append('<div class="mb-cando">' + "".join(
        f'<div class="cd"><span class="ring" style="--p:{c / n * 100:.1f}"><b>{round(c / n * 100)}%</b></span><span class="lb">{E(k)}<small>{c}件</small></span></div>'
        for k, c in cds) + f'</div><p class="cd-note">第{vol}回のアンケート{n}件の回答から。複数選択なので、合計は100%になりません。</p>')
    o.append('<h3 class="sum-h">次回</h3>')
    o.append(f'<p class="sum-next">{cfg["next"]}</p>')
    o.append('<h3 class="sum-h">PA45 の記録</h3>')
    o.append(f'<div class="mb-point"><b>&#x1f501; PA45は毎週やっています</b><br>第1回（2026-03-06）から第{vol}回まで、のべ <b>{tot["participants"]}名</b>にご参加いただきました。'
             f'アンケートは <b>{tot["responses"]}件</b>、理解できた <b>{tot["und"]:.1f}%</b>／役立ちそう <b>{tot["use"]:.1f}%</b>です。</div>')
    o.append(f'<div class="mb-nav"><a href="{ins}" target="_blank" rel="noopener"><span class="nv-lbl">この回の結果</span>第{vol}回 アンケート結果</a>'
             f'<a href="{BASE}/achievements/insights/can-do.html" target="_blank" rel="noopener"><span class="nv-lbl">全回の集計</span>できるようになったことランキング</a>'
             f'<a href="{BASE}/achievements/insights/" target="_blank" rel="noopener"><span class="nv-lbl">データで振り返る</span>PA45のアンケートまとめ</a></div>')
    o.append("</div>")
    pid = state.get("post_id")
    o.append(work_cta(str(pid or "new")))
    o.append('<p class="mb-disc">※ 本記事は公開日時点の内容です。筆者が実際に学んで試した手順をまとめたもので、Power Automate や各サービスの仕様は今後変わる可能性があります。<br>'
             '※ 記事の構成・図解の一部は、AIを壁打ち相手にしながら作成しています。</p>\n</div>')
    o.append(f"<!-- pa45:spacing-v1 --><style>{SPACING_CSS}</style><!-- /pa45:spacing-v1 -->")
    body = f"<style>{CSS_MAIN}</style>\n" + "\n".join(o)
    body = re.sub(r"\n{3,}", "\n\n", body)
    (here / "article.html").write_text(body, encoding="utf-8")
    print("article.html", len(body), "chars | img", body.count("<img"), "| shot", body.count('class="mb-shot"'),
          "| step", body.count('class="mb-step"'))

    # アイキャッチ
    ep = here / "assets" / "eyecatch.png"
    if not ep.exists():
        from _eyecatch_kit import render
        render(93, f"PA45 第{vol}回 ハンズオン", cfg["eye"][0], cfg["eye"][1], cfg["eye"][2], ep)
    if not PUSH:
        state_f.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        return
    _, eid = m.url("eyecatch", ep, f"pa45-vol{vol}-eyecatch.png")
    payload = {"title": cfg["title"], "content": body, "excerpt": cfg["excerpt"], "slug": cfg["slug"],
               "categories": [93], "featured_media": eid, "status": "draft"}
    if pid:
        cur = _req("GET", f"/wp-json/wp/v2/posts/{pid}?context=edit")
        if cur["status"] != "draft":
            payload.pop("status")   # はるが公開・予約したあとは状態を触らない
        bk = here / "backup"
        bk.mkdir(exist_ok=True)
        (bk / f"{pid}-{time.strftime('%Y%m%d-%H%M%S')}.html").write_text(cur["content"]["raw"], encoding="utf-8")
        j = _req("POST", f"/wp-json/wp/v2/posts/{pid}", payload)
    else:
        j = _req("POST", "/wp-json/wp/v2/posts", payload)
        state["post_id"] = pid = j["id"]
        state_f.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        # CTA の utm に記事IDを入れ直す
        body = body.replace(work_cta("new"), work_cta(str(pid)))
        (here / "article.html").write_text(body, encoding="utf-8")
        _req("POST", f"/wp-json/wp/v2/posts/{pid}", {"content": body})
    state_f.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    verify(pid)


def verify(pid):
    j = _req("GET", f"/wp-json/wp/v2/posts/{pid}?context=edit")
    c, r = j["content"]["raw"], j["content"]["rendered"]
    st = "".join(re.findall(r"<style.*?</style>", r, flags=re.S))
    print("POST", pid, "| status:", j["status"], "| slug:", j["slug"], "| cat:", j["categories"],
          "| featured:", j["featured_media"], "| img:", c.count("<img"),
          "| empty <p>:", len(re.findall(r"<p>\s*</p>", r)), "| style broken:", ("<br" in st or "<p" in st),
          "| excerpt:", bool(j["excerpt"]["raw"]))
    print("EDIT", f"https://www.automate136.com/wp-admin/post.php?post={pid}&action=edit")

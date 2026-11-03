"""柱記事 #553（変数）と #239（承認）の本文を書き直す。

2026-11-03 はる指示「全部直してほしいです」（作業中に見つけた問題を含めて全部）
- 本文の生成元＝articles/pillar-rewrite-20261103/{id}-body.html
  {{shot:ID}} は公開中の本文にある実画面の図（<!--shot:ID-->…<!--/shot:ID-->）をそのまま入れる。
  {{link:ID}} はその記事のURLに置き換える。
- 本文の前の <style> と、末尾の免責は公開中の本文から引き継ぐ。
- 本文のあとに「このテーマの記事」一覧（add-pillar-links.py）と研修・相談の案内
  （replace-cta-work.py の NEW_CTA）を入れる。
- 公開済みなので WordPress の自動保存として保存する。公開ページは、はるが「更新」を押すまで変わらない。

使い方:
  python scripts/rewrite-pillar-posts.py            # 確認だけ
  python scripts/rewrite-pillar-posts.py --apply
"""
import importlib.util, re, sys
from pathlib import Path
import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "articles/pillar-rewrite-20261103"


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PL = load("add-pillar-links")
NEW_CTA = load("replace-cta-work").NEW_CTA

# 記事ID: (柱キー, 新しいタイトル or None＝そのまま)
TARGETS = {
    553: ("A", "Power Automate 変数の初期化｜空欄の行をTeamsに知らせる"),
    239: ("F", "Power Automate 承認の種類と使い分け｜残業申請フローで確認"),
}

BANNED = ["★", "X投稿案", "公開予定", "つまずき", "ぜひ", "みたいな", "なんです", "しましょう", "てください。",
          "ポイント！", "皆さん", "&#8216;", "&#8217;", "関連記事：", "pa45-cta-v1"]


def build(pid, key, live, T):
    style = live[:live.index("</style>") + len("</style>")]
    disc = re.search(r'<p class="mb-disc">.*?</p>', live, re.S).group(0)
    body = (SRC / f"{pid}-body.html").read_text(encoding="utf-8")
    for sid in re.findall(r"\{\{shot:([\w-]+)\}\}", body):
        fig = re.search(rf"<!--shot:{sid}-->.*?<!--/shot:{sid}-->", live, re.S).group(0)
        body = body.replace("{{shot:%s}}" % sid, fig)
    links = [int(x) for x in re.findall(r"\{\{link:(\d+)\}\}", body)]
    if links:
        LT = PL.titles(links)
        for i in links:
            body = body.replace("{{link:%d}}" % i, LT[i][0])
    assert "{{" not in body
    return "\n\n".join([style, '<div class="mb-body">', body.strip(), PL.block(key, T), NEW_CTA, disc, "</div>"]) + "\n"


def check(s):
    body = s[s.index("</style>"):]
    # 禁止語は本文だけを見る（Teams に送る文面の pre と、ほかの記事のタイトルが並ぶ一覧は除く）
    prose = re.sub(r"<pre.*?</pre>|<!--pillar-links-->.*?<!--/pillar-links-->", "", body, flags=re.S)
    hits = [w for w in BANNED if w in prose]
    assert not hits, hits
    assert not re.search(r"<p>\s*</p>", body)
    assert body.count("<div") == body.count("</div>"), (body.count("<div"), body.count("</div>"))
    # 絵文字（記号ブロック）が本文に無いこと
    assert not re.search(r"&#x1f|&#x26a0;|&#x2705;|[\U0001F000-\U0001FAFF☀-➿]", body)


def main():
    apply = "--apply" in sys.argv
    need = [i for v in PL.PILLARS.values() for i in v[2] + v[3]] + list(PL.PILLAR_IDS.values())
    T = PL.titles(need)
    for pid, (key, title) in TARGETS.items():
        post = PL.get(f"posts/{pid}", params={"context": "edit"})
        assert post["status"] == "publish"
        s = build(pid, key, post["content"]["raw"], T)
        check(s)
        (PL.OUTDIR / "after" / f"{pid}.html").write_text(s, encoding="utf-8")
        new_title = title or post["title"]["raw"]
        plain = re.sub(r"<[^>]+>", "", s[s.index("</style>"):])
        print(f"{pid}: 本文 {len(post['content']['raw'])}→{len(s)}字（文字だけ {len(plain)}字） 画像 {s.count('<img')}枚 "
              f"タイトル {new_title}（{len(new_title)}字）")
        if apply:
            r = requests.post(f"{PL.WP}/wp-json/wp/v2/posts/{pid}/autosaves", auth=PL.AUTH, timeout=120,
                              json={"title": new_title, "excerpt": post["excerpt"]["raw"], "content": s})
            r.raise_for_status()
            print(f"      自動保存 id={r.json()['id']}")


if __name__ == "__main__":
    main()

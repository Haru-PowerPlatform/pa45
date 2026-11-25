"""PA実践・Tips の柱記事に「このテーマの記事」一覧と、柱どうしのリンクを入れる。

2026-11-03 はる指示「柱記事9本に『このテーマの記事』一覧と柱どうしのリンクを入れて、下書きで更新して」
設計＝Documents\\automate136-link-design.html

- 柱記事は公開済みなので、本文は書き換えずに WordPress の「自動保存」として保存する
  （POST /posts/{id}/autosaves）。公開ページは変わらない。
  はるがエディターで「自動保存を表示」→「復元」→「更新」を押したときに反映される。
- ブロックは <!--pillar-links--> 〜 <!--/pillar-links--> で囲む。再実行で入れ直し（冪等）。
- 変更前の本文は data/backup-wp/pillar-links-20261103/before.json、
  入れたあとの本文は同フォルダの after/{id}.html に保存する。

使い方:
  python scripts/add-pillar-links.py            # 確認だけ（書き込まない）
  python scripts/add-pillar-links.py --apply    # 9本の自動保存を作る
"""
import html, json, re, sys
from pathlib import Path
import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "data/backup-wp/pillar-links-20261103"
ENV = dict(l.strip().split("=", 1) for l in open(ROOT / ".env", encoding="utf-8") if "=" in l and not l.startswith("#"))
WP, AUTH = ENV["WP_URL"], (ENV["WP_USER"], ENV["WP_PASS"])

# 柱キー: (柱記事ID, テーマ名, 子記事, PA45回, ほかの柱)
PILLARS = {
    "A":  (553,  "変数",             [303, 320, 345, 361],                               [1276, 1257, 1026],       ["D", "G"]),
    "B":  (1318, "Teams通知",        [280, 286, 780, 1316, 1320, 1336, 764, 3068, 186, 1224], [2378, 2385, 2771, 2799], ["C1", "F"]),
    "C1": (1326, "JSON",             [1322, 1324, 1328, 402],                            [2749, 2539],             ["C2", "G"]),
    "C2": (1330, "配列・データ操作", [677, 1314, 1020],                                  [2132],                   ["C1", "B"]),
    "D":  (1338, "条件分岐と式",     [1334, 1346, 1348, 507],                            [1291],                   ["A", "E"]),
    "E":  (1340, "日付の計算",       [1342, 1344, 441, 715],                             [2726],                   ["D", "B"]),
    "F":  (239,  "承認フロー",       [],                                                 [2374, 2780, 2697],       ["B", "G"]),
    "G":  (1332, "エラーと止まらないフロー", [822],                                      [2450, 2739],             ["C1", "D"]),
    "H":  (4401, "使い分けと導入の判断", [2423, 956, 1288, 2442, 2119],                  [],                       ["P0", "F"]),
}
PILLAR_IDS = {k: v[0] for k, v in PILLARS.items()} | {"P0": 982}

START, END = "<!--pillar-links-->", "<!--/pillar-links-->"
S_BOX = "background:#f8fafc;border:1px solid #cbd5e1;border-radius:14px;padding:18px 22px;margin:40px 0;"
S_TTL = "font-weight:800;color:#0f172a;margin:0 0 4px;font-size:1.05em;"
S_SUB = "font-weight:700;color:#334155;margin:16px 0 4px;font-size:.95em;"
S_LEAD = "font-size:.9em;color:#475569;margin:0 0 8px;"
S_UL = "margin:0;padding-left:1.3em;line-height:1.8;"


def get(path, **kw):
    r = requests.get(f"{WP}/wp-json/wp/v2/{path}", auth=AUTH, timeout=60, **kw)
    r.raise_for_status()
    return r.json()


def titles(ids):
    out = {}
    ids = sorted(set(ids))
    for i in range(0, len(ids), 50):
        for p in get("posts", params={"include": ",".join(map(str, ids[i:i + 50])), "per_page": 50,
                                       "_fields": "id,link,title,status"}):
            assert p["status"] == "publish", p["id"]
            t = re.sub(r"<[^>]+>", "", p["title"]["rendered"])
            t = re.sub(r"^【[^】]*】\s*", "", t)          # 先頭の【Vol.N】【Power Automate入門】は落とす
            out[p["id"]] = (p["link"], t)
    missing = set(ids) - set(out)
    assert not missing, f"公開されていない記事: {missing}"
    return out


def ul(ids, T):
    lis = "".join(f'<li><a href="{html.escape(T[i][0])}">{T[i][1]}</a></li>' for i in ids)
    return f'<ul style="{S_UL}">{lis}</ul>'


def block(key, T):
    pid, name, kids, vols, cross = PILLARS[key]
    parts = [f'<div class="mb-series" style="{S_BOX}">', f'<p style="{S_TTL}">このテーマの記事</p>']
    if kids:
        parts += [f'<p style="{S_LEAD}">{name}について、アクションや使い方を1本ずつ扱った記事です。</p>', ul(kids, T)]
    if vols:
        parts += [f'<p style="{S_SUB}">PA45 のハンズオンで同じ内容を扱った回</p>', ul(vols, T)]
    parts += [f'<p style="{S_SUB}">ほかのテーマの記事</p>', ul([PILLAR_IDS[c] for c in cross], T), "</div>"]
    return START + "".join(parts) + END   # 改行を入れない（WPの自動整形で <br> <p> が混ざるため）


def insert(raw, blk):
    raw = re.sub(re.escape(START) + ".*?" + re.escape(END), "", raw, flags=re.S)
    body_from = raw.find("</style>") + len("</style>") if "</style>" in raw else 0
    anchors = [r"<h2>次回のPA45で", r'<div class="mb-cta', r"<!-- pa45-cta-v1 -->"]
    for a in anchors:
        m = re.compile(a).search(raw, body_from)
        if m:
            return raw[:m.start()] + blk + "\n\n" + raw[m.start():]
    raise ValueError("差し込み位置が見つからない")


def main():
    apply = "--apply" in sys.argv
    need = [i for v in PILLARS.values() for i in v[2] + v[3]] + list(PILLAR_IDS.values())
    T = titles(need)
    (OUTDIR / "after").mkdir(parents=True, exist_ok=True)
    for key, (pid, name, *_rest) in PILLARS.items():
        post = get(f"posts/{pid}", params={"context": "edit"})
        assert post["status"] == "publish"
        new = insert(post["content"]["raw"], block(key, T))
        (OUTDIR / "after" / f"{pid}.html").write_text(new, encoding="utf-8")
        n = len(re.findall(r"<li><a ", block(key, T)))
        print(f"{key:<3}{pid:>5} {name}: リンク{n}本 本文 {len(post['content']['raw'])}→{len(new)}字")
        if apply:
            r = requests.post(f"{WP}/wp-json/wp/v2/posts/{pid}/autosaves", auth=AUTH, timeout=120,
                              json={"title": post["title"]["raw"], "excerpt": post["excerpt"]["raw"], "content": new})
            r.raise_for_status()
            j = r.json()
            print(f"      自動保存 id={j['id']} parent={j.get('parent')}")


if __name__ == "__main__":
    main()

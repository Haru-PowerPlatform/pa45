"""個人の学習者向けの記事の末尾の案内を、個別相談の紹介記事（/spot-soudan/）への案内にする。

2026-10-14 はる方針：研修を頼む側の記事 → 研修・導入の案内（pa45/work/）／個人の学習者向けの記事 → 個別相談の紹介記事。
振り分けは data/backup-wp/cta-20261014/classification.json の kind（learner / buyer / event）。

⛔ 2026-10-15 個別相談はやめた。このスクリプトは実行しない。
⚠ 紹介記事（post 4867）を公開し、申し込みフォームができてから実行する。
⚠ articles/*/build_article.py の cta_pa() は研修・導入の案内を出すので、学習者向けの記事を作り直すときは
   そちらも学習者向けに直すこと（2026-10-14 時点で対象は copilot-studio-* 系の数本）。

  python scripts/apply-learner-cta.py            # 確認だけ
  python scripts/apply-learner-cta.py --apply    # 書き込む
"""
import json, re, sys
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
CLS = ROOT / "data/backup-wp/cta-20261014/classification.json"
BACKUP = ROOT / "data/backup-wp/cta-20261014/before_learner_cta.json"
SPOT = "https://www.automate136.com/spot-soudan/"
WORK = "https://haru-powerplatform.github.io/pa45/work/"
WORK_BLOCK = re.compile(r'<div class="mb-cta pa"[^>]*>(?:(?!</div>).)*研修・導入のご相談について.*?</div>', re.S)


def block(pid, styled):
    href = f"{SPOT}?utm_source=automate136&amp;utm_medium=blog_cta&amp;utm_content=p{pid}"
    text = ('<p{p}>1つの困りごとを1問1,000円で受け、持ち帰って確かめてから、画面つきの手順書でお返ししています。</p>')
    if styled:
        return ('<div class="mb-cta pa" data-cta="spot"><p class="cta-ttl">この手順で止まったときは</p>'
                + text.format(p="")
                + f'<a class="mb-btn pa" href="{href}" target="_blank" rel="noopener">個別相談の内容を見る</a></div>')
    return ('<div class="mb-cta pa" data-cta="spot" style="margin:42px 0;padding:18px 22px;border-radius:16px;text-align:center;background:linear-gradient(135deg,#eaf2fc,#d8e8fa);border:1px solid #b8d3ef;">'
            '<p style="font-weight:800;font-size:1.08em;margin:0 0 6px;color:#14528f;">この手順で止まったときは</p>'
            + text.format(p=' style="margin:0 0 12px;font-size:.92em;color:#475569;line-height:1.7;"')
            + f'<a href="{href}" target="_blank" rel="noopener" style="display:inline-block;background:#0B6BCB;color:#fff;text-decoration:none;font-weight:700;padding:10px 22px;border-radius:999px;">個別相談の内容を見る</a></div>')


def transform(pid, raw):
    new_blk = block(pid, ".mb-cta{" in raw)
    if WORK_BLOCK.search(raw):
        return WORK_BLOCK.sub(new_blk, raw, count=1)
    wrapped = ("\n\n<!-- wp:html -->\n" + new_blk + "\n<!-- /wp:html -->\n") if "<!-- wp:" in raw else ("\n\n" + new_blk + "\n")
    m = re.search(r'<p class="mb-disc', raw)
    return raw[:m.start()] + wrapped + "\n" + raw[m.start():] if m else raw.rstrip() + wrapped


def main():
    env = {}
    for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1); env[k.strip()] = v.strip().strip('"')
    wp = env["WP_URL"].rstrip("/"); auth = (env["WP_USER"], env["WP_PASS"])
    ids = [o["id"] for o in json.loads(CLS.read_text(encoding="utf-8")) if o["kind"] == "learner"]
    print(f"学習者向け {len(ids)} 本")
    if "--apply" not in sys.argv:
        return
    backup, ok, bad = [], 0, []
    for pid in ids:
        p = requests.get(f"{wp}/wp-json/wp/v2/posts/{pid}", params={"context": "edit", "_fields": "id,status,content"}, auth=auth).json()
        raw = p["content"]["raw"]; backup.append(p)
        if SPOT in raw:
            ok += 1; continue
        r = requests.post(f"{wp}/wp-json/wp/v2/posts/{pid}", json={"content": transform(pid, raw)}, auth=auth)
        q = requests.get(f"{wp}/wp-json/wp/v2/posts/{pid}", params={"context": "edit", "_fields": "status,content"}, auth=auth).json()
        c = q["content"]["raw"]
        if r.status_code == 200 and q["status"] == p["status"] and f"utm_content=p{pid}" in c and "研修・導入のご相談について" not in c:
            ok += 1
        else:
            bad.append(pid)
    BACKUP.write_text(json.dumps(backup, ensure_ascii=False), encoding="utf-8")
    print("ok", ok, "要確認", bad)


if __name__ == "__main__":
    main()

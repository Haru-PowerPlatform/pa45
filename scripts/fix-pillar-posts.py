"""柱記事 #553（変数）と #239（承認）の本文の問題を直す。

2026-11-03 はる指示「作業中に見つけた問題は修正しておいてください」
- #553：記事を作ったときのメモ（GitHub公開予定・X投稿案・文字数チェック）と、
  ★スクショ の仮置き、「GitHubで公開予定です」を消す
- #239：旧い文体の「まとめ」を書き直す
- 両方：話題と合わない機械的な「→ 関連記事：」3本を外す
  （柱の「このテーマの記事」一覧が代わりになる）
- 両方：末尾の旧い案内（Xフォロー・PA45）を、研修・相談の案内に差し替える
  （文面は scripts/replace-cta-work.py の NEW_CTA と同じ）

add-pillar-links.py と同じく、公開済みなので WordPress の自動保存として保存する。
公開中の本文を元に「このテーマの記事」一覧も入れ直すので、何度実行しても同じ結果になる。

使い方:
  python scripts/fix-pillar-posts.py            # 確認だけ
  python scripts/fix-pillar-posts.py --apply
"""
import importlib.util, re, sys
from pathlib import Path
import requests

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PL = load("add-pillar-links")
NEW_CTA = load("replace-cta-work").NEW_CTA

OLD_RELATED = re.compile(
    r'\s*<p style="font-size:13px;color:#555;">&#8594; 関連記事：「<a href="https://www\.automate136\.com/'
    r'(?:x-vol-01-cs-word-integration|trigger-powerautomate-001|power-automate-aibuilder)/">[^<]*</a>」</p>\s*')
OLD_CTA = re.compile(r"<!-- pa45-cta-v1 -->.*?(?=<p class=\"mb-disc\">)", re.S)

MATOME_239 = (
    "<p>承認フローは、「開始して承認を待機」と「条件」の2つのアクションで作れます。<br>"
    "承認の種類は4つあり、全員の承認が要るか、最初の1人の応答で決めるかで選びます。<br>"
    "残業申請と同じ形で、出張申請・経費精算・休暇申請にも使えます。</p>"
)


def sub1(pattern, repl, s, flags=0, count=None):
    new, n = re.subn(pattern, repl, s, flags=flags)
    assert n and (count is None or n == count), f"{pattern[:40]}… が {n} 件"
    return new


def fix_553(s):
    s = sub1(r"<div>\s*<hr />\s*<h3>&#x2705; GitHub公開予定</h3>.*?&#x2705; 比較表を追加済み</p>\s*</div>\s*", "", s, re.S, 1)
    s = sub1(r"\s*GitHubにサンプルExcelとフロー\.zipを公開予定です。\s*", "", s, count=1)
    s = sub1(r"\s*<p>※ GitHubで公開予定です。</p>", "", s, count=1)
    s = sub1(r" ?★スクショ：トリガー設定画面", "", s, count=1)
    s = sub1(r"\s*<p>★スクショ：[^<]*</p>", "", s, count=2)
    return s


def fix_239(s):
    return sub1(r"(<h2>まとめ</h2>)\s*Power Automateで作成したフローは.*?皆さん成功願っています！",
                r"\1\n" + MATOME_239, s, re.S, 1)


FIXES = {553: fix_553, 239: fix_239}


def main():
    apply = "--apply" in sys.argv
    need = [i for v in PL.PILLARS.values() for i in v[2] + v[3]] + list(PL.PILLAR_IDS.values())
    T = PL.titles(need)
    for key, (pid, *_r) in PL.PILLARS.items():
        if pid not in FIXES:
            continue
        post = PL.get(f"posts/{pid}", params={"context": "edit"})
        assert post["status"] == "publish"
        s = FIXES[pid](post["content"]["raw"])
        s, n_rel = OLD_RELATED.subn("\n\n", s)
        assert n_rel == 3, n_rel
        s = sub1(OLD_CTA.pattern, NEW_CTA + "\n\n", s, re.S, 1)
        s = PL.insert(s, PL.block(key, T))
        assert "★" not in s and "X投稿案" not in s and "公開予定" not in s and "pa45-cta-v1" not in s
        (PL.OUTDIR / "after" / f"{pid}.html").write_text(s, encoding="utf-8")
        print(f"{pid}: 関連記事 {n_rel}本外す・案内を差し替え 本文 {len(post['content']['raw'])}→{len(s)}字")
        if apply:
            r = requests.post(f"{PL.WP}/wp-json/wp/v2/posts/{pid}/autosaves", auth=PL.AUTH, timeout=120,
                              json={"title": post["title"]["raw"], "excerpt": post["excerpt"]["raw"], "content": s})
            r.raise_for_status()
            print(f"      自動保存 id={r.json()['id']}")


if __name__ == "__main__":
    main()

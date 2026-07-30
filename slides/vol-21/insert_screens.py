# -*- coding: utf-8 -*-
"""
vol-21 スライドの「実機スクショ差込」枠に、撮影したPNGを差し込むスクリプト。

使い方:
  1. assets/screens/ に決められたファイル名でPNGを置く
  2. python insert_screens.py
  3. 置いたファイルの枠だけが画像に置き換わる（未撮影の枠はプレースホルダのまま残る）

ファイル名（すべて assets/screens/ 配下）:
  s08_office.png  … office.com サインイン／アプリ一覧（ワッフル）
  s10_forms.png   … Forms 新規作成〜質問1つ
  s11_list.png    … SharePoint「+新規 → リスト」→ 空白のリスト
  s12_teams.png   … Power Automate「チャットまたはチャネルにメッセージを投稿する」設定画面
"""
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
HTML = BASE / "index.html"

# スライドID → (画像ファイル名, 枠の高さpx)
TARGETS = {
    "s8":  ("s08_office.png", 360),
    "s10": ("s10_forms.png", 330),
    "s11": ("s11_list.png", 200),
    "s12": ("s12_teams.png", 250),
}

PH_RE = re.compile(
    r'<div class="ph" style="height:\d+px;">.*?</div>\s*</div>',
    re.DOTALL,
)


def slide_span(html: str, slide_id: str):
    """該当スライド section の開始・終了位置を返す"""
    start = html.find(f'<section class="slide" id="{slide_id}">')
    if start == -1:
        start = html.find(f'id="{slide_id}"')
        if start == -1:
            return None
        start = html.rfind("<section", 0, start)
    end = html.find("</section>", start)
    return start, end


def main() -> int:
    html = HTML.read_text(encoding="utf-8")
    done, skipped = [], []

    for slide_id, (fname, _h) in TARGETS.items():
        img = BASE / "assets" / "screens" / fname
        if not img.exists():
            skipped.append(fname)
            continue

        span = slide_span(html, slide_id)
        if span is None:
            print(f"  !! スライド {slide_id} が見つかりません")
            continue
        s, e = span
        section = html[s:e]

        new_section, n = PH_RE.subn(
            f'<img src="assets/screens/{fname}" alt="" '
            f'style="display:block;width:100%;height:auto;">',
            section,
            count=1,
        )
        if n == 0:
            print(f"  -- {slide_id}: 差込枠が見つかりません（すでに差込済み？）")
            continue

        # 「実スクショ差込」バッジを外す
        new_section = new_section.replace(
            '<span class="badge-todo">実スクショ差込</span>', ""
        )
        html = html[:s] + new_section + html[e:]
        done.append(f"{slide_id} ← {fname}")

    HTML.write_text(html, encoding="utf-8")

    print("差し込み完了:")
    for d in done or ["  （なし）"]:
        print("  " + d)
    if skipped:
        print("未撮影（プレースホルダのまま）:")
        for s in skipped:
            print("  " + s)
    print("\n※ 差込後は必ず全15枚の見切れ（overflow）チェックをすること")
    return 0


if __name__ == "__main__":
    sys.exit(main())

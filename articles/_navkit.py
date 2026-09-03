#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""記事共通の「現在地バー」「節ゴール」「はるの吹き出し」部品。

各 build_article.py から次のように使う。

    import sys as _sys
    _sys.path.insert(0, str(ROOT / "articles"))
    from _navkit import NAV_CSS, make_nav
    nav, goal = make_nav(['1つ目', '2つ目', ...], jp)
    CSS = CSS.replace("</style>", NAV_CSS + "</style>")

※ 2026-09-04 に復元。元ソースが消え __pycache__ の .pyc だけ残っていたため、
   そこから出力を突き合わせて書き戻したもの（出力は完全一致を確認済み）。
"""

HARU_AVATAR = "https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png"

NAV_CSS = (
    ".mb-nav{margin:38px 0 6px;}"
    ".mb-nav .lb{display:inline-block;font-size:11.5px;font-weight:800;color:#7c3aed;letter-spacing:.1em;margin-bottom:8px;}"
    ".mb-nav .cells{display:flex;gap:6px;flex-wrap:wrap;}"
    ".mb-nav .n{flex:1;min-width:126px;background:#f5f2fc;border:1px solid #e4dcf7;border-radius:9px;padding:9px 10px;font-size:.8em;color:#9c94b3;line-height:1.45;text-align:center;font-weight:700;}"
    ".mb-nav .n .ix{display:block;font-size:.85em;opacity:.75;margin-bottom:2px;}"
    ".mb-nav .n.done{background:#ede9fe;border-color:#d9cdf5;color:#6d28d9;}"
    ".mb-nav .n.on{background:#7c3aed;border-color:#7c3aed;color:#fff;box-shadow:0 3px 10px rgba(124,58,237,.28);}"
    ".mb-goal{background:#fff;border:2px solid #ddd0f2;border-radius:12px;padding:6px 20px;margin:14px 0 32px;}"
    ".mb-goal .row{display:flex;gap:14px;align-items:flex-start;padding:12px 0;border-top:1px solid #f0eafb;line-height:1.9;font-size:.96em;}"
    ".mb-goal .row:first-child{border-top:none;}"
    ".mb-goal .g{flex:none;width:112px;font-size:11.5px;font-weight:800;color:#7c3aed;background:#f3eefc;border-radius:999px;padding:4px 0;text-align:center;margin-top:5px;}"
    ".mb-goal .g.af{color:#2f855a;background:#eaf5ee;}"
    "@media(max-width:600px){.mb-nav .n{min-width:calc(50% - 3px);}.mb-goal .g{width:96px;font-size:11px;}}"
)

BUBBLE_CSS = ".speech-balloon{line-height:1.95;}"


def make_nav(steps, jp):
    """節ラベルの一覧と jp（句点改行）を受け取り、nav(i) と goal(...) を返す。

    nav(i)  : i 番目（1始まり）を現在地としたパンくずバー。手前の節にはチェックが付く。
    goal(する, なる, read=False)
            : その節のゴール。read=True で「読み物の節」用のラベルに切り替わる。
    """
    def nav(i):
        cells = ""
        for k, label in enumerate(steps, 1):
            if k < i:
                cells += f'<div class="n done"><span class="ix">{k}</span>&#x2713; {label}</div>'
            elif k == i:
                cells += f'<div class="n on"><span class="ix">{k}</span>{label}</div>'
            else:
                cells += f'<div class="n"><span class="ix">{k}</span>{label}</div>'
        return ('\n\n<div class="mb-nav"><span class="lb">いまここ</span>'
                f'<div class="cells">{cells}</div></div>')

    def goal(do, become, read=False):
        lb_do = "この節で分かること" if read else "この節ですること"
        lb_af = "読み終えるとこうなる" if read else "終わるとこうなる"
        return ('\n\n<div class="mb-goal">'
                f'<div class="row"><span class="g">{lb_do}</span><div>{jp(do)}</div></div>'
                f'<div class="row"><span class="g af">{lb_af}</span><div>{jp(become)}</div></div>'
                '</div>')

    return nav, goal


def make_bubble(jp):
    """はるのアイコン付き吹き出しを作る関数を返す。"""
    def bubble(text):
        return ('\n\n<div class="speech-wrap sb-id-14 sbs-stn sbp-l sbis-cb cf">'
                '<div class="speech-person"><figure class="speech-icon">'
                f'<img class="speech-icon-image" src="{HARU_AVATAR}" alt="" width="1024" height="1024" /></figure></div>'
                f'<div class="speech-balloon">{jp(text)}</div></div>')
    return bubble

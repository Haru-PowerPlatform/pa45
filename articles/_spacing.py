# -*- coding: utf-8 -*-
"""記事本文の余白（2026-11-22 はる「段落の前に空白を・詰まりすぎ」）。
_howtokit.CSS と wp-design/apply-spacing-v1.py の両方がここを読む。"""
MARK = "pa45:spacing-v1"
B = "body div.mb-body"
CSS = (
    f"{B} > p{{margin:2.6em 0!important;}}"
    f"{B} > h2{{margin-top:4.6em!important;margin-bottom:1.2em!important;}}"
    f"{B} > h3{{margin-top:3.8em!important;margin-bottom:1em!important;padding-left:14px;border-left:6px solid #7c3aed;}}"
    f"{B} .mb-nav{{margin-top:110px!important;padding-top:34px;border-top:2px dashed #e4dcf7;}}"
    f"{B} .mb-nav + h2{{margin-top:1.6em!important;}}"
    f"{B} figure,{B} .mb-shot,{B} .mb-fig{{margin-top:60px!important;margin-bottom:60px!important;}}"
    f"{B} .mb-step,{B} .mb-why,{B} .mb-note,{B} .mb-warn,{B} .mb-point,{B} .mb-term,{B} .mb-code,{B} .mb-tbl,"
    f"{B} .mb-link,{B} .mb-check,{B} .mb-cta,{B} .mb-learn{{margin-top:48px!important;margin-bottom:48px!important;}}"
    f"{B} .speech-wrap{{margin:48px 0!important;}}"
    "@media(max-width:600px){"
    f"{B} > p{{margin:2.2em 0!important;}}{B} > h2{{margin-top:3.6em!important;}}{B} > h3{{margin-top:3em!important;}}"
    f"{B} .mb-nav{{margin-top:80px!important;padding-top:26px;}}"
    f"{B} figure,{B} .mb-shot,{B} .mb-fig{{margin-top:44px!important;margin-bottom:44px!important;}}"
    "}"
)


# 2026-11-22 はる「進めて」→ .mb-body を使っていない古い記事（Cocoon の .entry-content 直下に本文がある型）向け。
# 指定は上と同じ。小見出しの紫の縦線はテーマ側の h3 の飾りと重なるので入れない。
MARK_PLAIN = "pa45:spacing-plain-v1"
E = "body .entry-content"
CSS_PLAIN = (
    f"{E} > p{{margin:2.6em 0!important;}}"
    f"{E} > h2{{margin-top:4.6em!important;margin-bottom:1.2em!important;}}"
    f"{E} > h3{{margin-top:3.8em!important;margin-bottom:1em!important;}}"
    f"{E} > figure,{E} > .wp-block-image,{E} > p > img{{margin-top:60px!important;margin-bottom:60px!important;}}"
    f"{E} > .blank-box,{E} > .information-box,{E} > .memo-box,{E} > .sp-box,{E} > .box,{E} > .blogcard-wrap,"
    f"{E} > table,{E} > pre,{E} > ul,{E} > ol,{E} > .speech-wrap{{margin-top:48px!important;margin-bottom:48px!important;}}"
    "@media(max-width:600px){"
    f"{E} > p{{margin:2.2em 0!important;}}{E} > h2{{margin-top:3.6em!important;}}{E} > h3{{margin-top:3em!important;}}"
    f"{E} > figure,{E} > .wp-block-image{{margin-top:44px!important;margin-bottom:44px!important;}}"
    "}"
)

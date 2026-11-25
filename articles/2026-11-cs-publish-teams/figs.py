#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2677 の図（横長1660px）。arch＝作る場所と使う場所／route＝画面のたどり方／channels＝選べるチャネル。
  python figs.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _figkit import ms, doc, route, render, AC, ARROW  # noqa: E402

ASSETS = HERE / "assets"

CSS = f"""
.rw{{display:flex;align-items:stretch}}
.bx{{flex:1;border:3px solid {AC};border-radius:24px;background:#fff;padding:16px 18px 18px;text-align:center}}
.bx.t{{border-color:#4f52b2}}
.bx img.big{{width:92px;height:92px;display:block;margin:4px auto 8px}}
.bx .t1{{font-size:28px;font-weight:800;line-height:1.4}}
.bx .d{{font-size:22px;color:#475569;line-height:1.55;margin-top:8px}}
.bx .who{{display:inline-block;font-size:21px;font-weight:800;color:#475569;background:#e2e8f0;border-radius:999px;padding:3px 16px;margin-bottom:8px}}
.mid{{flex:none;width:210px;display:flex;flex-direction:column;justify-content:center;padding:0 8px}}
.mid .lb{{font-size:21px;font-weight:800;color:{AC};text-align:center;line-height:1.4;margin-bottom:6px}}
.mid svg{{width:100%;height:26px;display:block}}
.mid line{{stroke:{AC};stroke-width:5}}
.mid polygon{{fill:{AC}}}
.g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.c{{background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:16px 18px;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.c.on{{border-color:{AC};background:{AC}0d}}
.c.off{{border-style:dashed;background:#f8fafc}}
.c .h{{display:flex;align-items:center;gap:12px;font-size:26px;font-weight:800;margin-bottom:8px}}
.c .h img{{width:56px;height:56px}}
.c .h .fb{{width:56px;height:56px;border-radius:14px;background:#e2e8f0;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:#475569}}
.c .d{{font-size:22px;color:#475569;line-height:1.55}}
.c .w{{display:inline-block;font-size:19px;font-weight:800;color:#fff;background:{AC};border-radius:999px;padding:1px 14px;margin-bottom:8px}}
.c .w.g{{color:#475569;background:#e2e8f0}}
"""


def arch():
    def mid(lb):
        return f'<div class="mid"><div class="lb">{lb}</div>{ARROW}</div>'
    b = '<h1>この記事ですること：作ったエージェントを Teams で使える場所に出す</h1>'
    b += '<div class="lead">作る場所は Copilot Studio、使う場所は Teams。あいだをつなぐのが、チャネルの追加と公開</div><div class="rw">'
    b += (f'<div class="bx"><span class="who">作る人</span><img class="big" src="{ms("copilotstudio")}">'
          '<div class="t1">Copilot Studio</div><div class="d">指示・ナレッジ・ツールを<br>作成の画面で作る。<br>プレビューは作った人だけ</div></div>')
    b += mid("① チャネルを追加<br>② 公開")
    b += (f'<div class="bx t"><span class="who">使う人</span><img class="big" src="{ms("teams")}">'
          '<div class="t1">Microsoft Teams</div><div class="d">エージェントを追加して、<br>1対1のチャットで話しかける</div></div>')
    b += '</div>'
    b += ('<div class="notes"><b>用意するもの</b>'
          f'<span class="chip"><img src="{ms("copilotstudio")}">作成済みのエージェント</span>'
          f'<span class="chip"><img src="{ms("teams")}">Teams が使えるアカウント</span>'
          '<span class="chip t">会話には Copilot クレジット</span></div>')
    return doc(b, CSS)


def route_():
    return route("Copilot Studio の画面のたどり方：チャネルの追加から公開まで",
                 "押す場所は5か所。下の番号は、この記事の節の番号と同じ",
                 [("作成", "右の <em>チャネル</em> の<br><em>＋</em> を押す", "チャネルの追加<br>が開く"),
                  ("追加", "<em style=\"white-space:nowrap\">Teams + Microsoft 365</em><br>を押す", "使う場所を<br>選ぶ画面になる"),
                  ("追加", "使う場所を選び<br><em>説明</em> を書く", "<em>チャネルを追加</em><br>を押す"),
                  ("作成", "右上の <em>公開</em><br>を押す", "確認の画面が<br>出る"),
                  ("確認", "<em style=\"white-space:nowrap;font-size:23px\">エージェントの公開</em><br>を押す", "Teams で<br>使えるようになる")],
                 ["①", "①", "②", "③", "③"])


def channels():
    def c(ico, name, d, tag, cls=""):
        i = f'<img src="{ms(ico)}">' if len(ico) > 1 else f'<div class="fb">{ico}</div>'
        return (f'<div class="c {cls}"><span class="w{"" if cls == "on" else " g"}">{tag}</span>'
                f'<div class="h">{i}{name}</div><div class="d">{d}</div></div>')
    b = '<h1>チャネルの追加で選べるもの</h1><div class="lead">「チャネルの追加」の画面に並ぶ3つ。この記事では Teams + Microsoft 365 を使う</div><div class="g3">'
    b += c("teams", "Teams + Microsoft 365", "Teams と Microsoft 365 Copilot。<br>中で、Teams のみも選べる", "この記事で使う", "on")
    b += c("web", "デモ Web サイト", "試すための Web ページ。<br>認証なしにする必要がある", "選べない状態だった", "off")
    b += c("ア", "アプリ", "押すと次の画面に進める。<br>中身は確かめていない", "選べる")
    b += '</div>'
    return doc(b, CSS)


def render_all():
    return {n: render(f(), ASSETS / f"fig-{n}.png", h) for n, f, h in
            (("arch", arch, 900), ("route", route_, 700), ("channels", channels, 700))}


if __name__ == "__main__":
    for k, v in render_all().items():
        print("fig", k, v)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2652 の図（横長1660px）。arch＝ツールを足した構成／route＝画面のたどり方／when＝ツールが動くまでの流れ。
  python figs.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _figkit import ms, doc, route, render, AC, ARROW  # noqa: E402

ASSETS = HERE / "assets"

CSS = f"""
.rw{{display:flex;align-items:stretch}}
.pp{{flex:none;width:270px;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:18px 14px;text-align:center;display:flex;flex-direction:column;justify-content:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.pp img{{width:76px;height:76px;margin:0 auto 8px;display:block}}
.pp .t{{font-size:26px;font-weight:800;line-height:1.4}}
.pp .q{{font-size:22px;color:#0c4a6e;background:#e0f2fe;border-radius:16px;padding:10px 12px;margin-top:12px;line-height:1.5;text-align:left}}
.pp .d{{font-size:22px;color:#475569;line-height:1.5;margin-top:8px}}
.mid{{flex:none;width:120px;display:flex;flex-direction:column;justify-content:center;padding:0 6px}}
.mid .lb{{font-size:21px;font-weight:800;color:{AC};text-align:center;line-height:1.35;margin-bottom:4px;white-space:nowrap}}
.mid svg{{width:100%;height:26px;display:block}}
.mid line{{stroke:{AC};stroke-width:5}}
.mid polygon{{fill:{AC}}}
.ag{{flex:1;border:3px solid {AC};border-radius:24px;background:#fff;padding:18px 20px 20px}}
.agt{{display:inline-flex;align-items:center;gap:12px;font-size:26px;font-weight:800;color:#fff;background:{AC};border-radius:999px;padding:6px 24px 6px 10px;margin-bottom:14px}}
.agt img{{width:44px;height:44px;background:#fff;border-radius:50%;padding:4px}}
.pt{{border:2.5px solid #e2e8f0;border-radius:18px;padding:12px 16px;background:#fff;margin-top:12px}}
.pt.on{{border-color:{AC};background:{AC}0d}}
.pt .h{{display:flex;align-items:center;gap:12px;font-size:25px;font-weight:800}}
.pt .h img{{width:50px;height:50px}}
.pt .d{{font-size:21px;color:#475569;line-height:1.5;margin-top:4px}}
.tag{{display:inline-block;font-size:18px;font-weight:800;border-radius:999px;padding:1px 12px;margin-left:6px;color:#fff;background:{AC}}}
.tag.g{{color:#475569;background:#e2e8f0}}
.st4{{display:flex;align-items:stretch}}
.s4{{flex:1;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:16px 14px;text-align:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.s4.on{{border-color:{AC}}}
.s4 .n{{display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:50%;background:{AC};color:#fff;font-size:25px;font-weight:800;margin-bottom:8px}}
.s4 .t{{font-size:25px;font-weight:800;line-height:1.4}}
.s4 .d{{font-size:21px;color:#475569;line-height:1.5;margin-top:8px}}
.a4{{flex:none;width:54px;display:flex;align-items:center;justify-content:center}}
.a4 svg{{width:44px;height:26px}}
.a4 line{{stroke:{AC};stroke-width:5}}
.a4 polygon{{fill:{AC}}}
"""
A4 = '<div class="a4"><svg viewBox="0 0 44 26"><line x1="0" y1="13" x2="30" y2="13"/><polygon points="26,2 44,13 26,24"/></svg></div>'


def arch():
    def mid(lb):
        return f'<div class="mid"><div class="lb">{lb}</div>{ARROW}</div>'
    b = '<h1>この記事で足すもの：エージェントに持たせる道具（ツール）</h1>'
    b += '<div class="lead">答えるだけだったエージェントに、メールを送る操作を1つ持たせる</div><div class="rw">'
    b += ('<div class="pp"><div class="t">質問する人</div>'
          '<div class="q">申し込みたいです。</div></div>')
    b += mid("会話")
    b += f'<div class="ag"><div class="agt"><img src="{ms("copilotstudio")}">Copilot Studio のエージェント</div>'
    b += (f'<div class="pt"><div class="h"><img src="{ms("agent")}">指示<span class="tag">1行足す</span></div>'
          '<div class="d">どんなときに、どのツールを使うかを書く</div></div>')
    b += (f'<div class="pt on"><div class="h"><img src="{ms("tools")}">ツール：メールの送信 (V2)<span class="tag">この記事で足す</span></div>'
          '<div class="d">Office 365 Outlook のコネクタ アクション。<br>宛先・件名・本文は AI が入れる</div></div>')
    b += (f'<div class="pt"><div class="h"><img src="{ms("web")}">ナレッジ<span class="tag g">そのまま</span></div>'
          '<div class="d">Web 検索と、前の記事で入れた資料</div></div></div>')
    b += mid("メール")
    b += ('<div class="pp"><div class="t">担当者</div>'
          '<div class="d">Outlook に<br>お問い合わせの<br>メールが届く</div></div>')
    b += '</div>'
    b += ('<div class="notes"><b>用意するもの</b>'
          f'<span class="chip"><img src="{ms("copilotstudio")}">作成済みのエージェント</span>'
          '<span class="chip t">Outlook が使える Microsoft 365 アカウント</span>'
          '<span class="chip t">テストで会話するには Copilot クレジット</span></div>')
    return doc(b, CSS)


def route_():
    return route("Copilot Studio の画面のたどり方：ツールを足して保存するまで",
                 "押す場所は5か所。下の番号は、この記事の節の番号と同じ",
                 [("作成", "右の <em>ツール</em> の<br><em>＋</em> を押す", "ツールの追加<br>が開く"),
                  ("追加", "<em style=\"white-space:nowrap\">Office 365 Outlook</em><br>を押す", "アクションの<br>一覧が出る"),
                  ("追加", "<em>メールの送信 (V2)</em><br>→ <em>追加</em>", "右のツールに<br>並ぶ"),
                  ("詳細", "ツール名を押し<br><em>AI の説明</em> を書く", "<em>完了</em> で閉じる"),
                  ("作成", "<em>指示</em> に1行足し<br><em>保存</em> を押す", "保存されました<br>と出る")],
                 ["①", "①", "②", "③", "④"])


def when():
    b = '<h1>ツールが動くまでの流れ</h1><div class="lead">ツールを置くだけでは使われなかった。説明と指示で、使う場面を伝える</div><div class="st4">'
    items = [("①", "ツールを足す", "右の「ツール」に<br>メールの送信 (V2) が並ぶ", False),
             ("②", "AI の説明を書く", "どんなときに使う<br>ツールかを書く", True),
             ("③", "指示に1行足す", "どの場面で<br>どのツールを使うかを書く", True),
             ("④", "会話で場面が来る", "エージェントが<br>ツールを選ぶ", False),
             ("⑤", "許可を確認", "送る前に、許可するか<br>を人に聞く", False)]
    for i, (n, t, d, on) in enumerate(items):
        b += f'<div class="s4{" on" if on else ""}"><div class="n">{n}</div><div class="t">{t}</div><div class="d">{d}</div></div>'
        if i < len(items) - 1:
            b += A4
    b += '</div>'
    return doc(b, CSS)


def render_all():
    return {n: render(f(), ASSETS / f"fig-{n}.png", h) for n, f, h in
            (("arch", arch, 1100), ("route", route_, 700), ("when", when, 700))}


if __name__ == "__main__":
    for k, v in render_all().items():
        print("fig", k, v)

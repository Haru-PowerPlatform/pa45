#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2583 の図（横長1660px）。arch＝作るものの構成／route＝画面のたどり方／parts＝作成画面の読み方。
  python figs.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _figkit import ms, doc, route, render, AC, ARROW  # noqa: E402

ASSETS = HERE / "assets"

ARCH_CSS = f"""
.rw{{display:flex;align-items:stretch}}
.pp{{flex:none;width:310px;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:18px 14px;text-align:center;display:flex;flex-direction:column;justify-content:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.pp .t{{font-size:27px;font-weight:800;line-height:1.4}}
.pp .q{{font-size:22px;color:#0c4a6e;background:#e0f2fe;border-radius:16px;padding:10px 12px;margin-top:12px;line-height:1.5;text-align:left}}
.pp .a{{font-size:22px;color:#334155;background:#f1f5f9;border-left:6px solid {AC};border-radius:8px;padding:10px 12px;margin-top:12px;line-height:1.5;text-align:left}}
.mid{{flex:none;width:130px;display:flex;flex-direction:column;justify-content:center;gap:60px;padding:0 6px}}
.mid .lb{{font-size:21px;font-weight:800;color:{AC};text-align:center;line-height:1.35;margin-bottom:4px;white-space:nowrap}}
.mid svg{{width:100%;height:26px;display:block}}
.mid line{{stroke:{AC};stroke-width:5}}
.mid polygon{{fill:{AC}}}
.mid .bk svg{{transform:scaleX(-1)}}
.ag{{flex:1;border:3px solid {AC};border-radius:24px;background:#fff;padding:18px 20px 20px}}
.agt{{display:inline-flex;align-items:center;gap:12px;font-size:26px;font-weight:800;color:#fff;background:{AC};border-radius:999px;padding:6px 24px 6px 10px;margin-bottom:14px}}
.agt img{{width:44px;height:44px;background:#fff;border-radius:50%;padding:4px}}
.gr{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.pt{{display:flex;gap:14px;align-items:flex-start;border:2.5px solid #e2e8f0;border-radius:18px;padding:14px 16px;background:#fff}}
.pt.on{{border-color:{AC};background:{AC}0d}}
.pt img{{flex:none;width:60px;height:60px}}
.pt b{{display:block;font-size:25px;line-height:1.35}}
.pt span.d{{display:block;font-size:21px;color:#475569;line-height:1.5;margin-top:2px}}
.tag{{display:inline-block;font-size:18px;font-weight:800;border-radius:999px;padding:1px 12px;margin-left:8px;vertical-align:middle}}
.tag.w{{color:#fff;background:{AC}}}
.tag.g{{color:#475569;background:#e2e8f0}}
"""


def arch():
    def pt(ico, name, sub, tag, on=False):
        t = f'<span class="tag {"w" if on else "g"}">{tag}</span>'
        return f'<div class="pt{" on" if on else ""}"><img src="{ms(ico)}"><div><b>{name}{t}</b><span class="d">{sub}</span></div></div>'
    b = '<h1>この記事で作るもの：質問に答えるエージェントを1体</h1>'
    b += '<div class="lead">書くのは名前と指示だけ。右側の部品は、最初から入っているものをそのまま使う</div><div class="rw">'
    b += ('<div class="pp"><div class="t">質問する人</div>'
          '<div class="q">どんな会ですか。<br>初めてでも参加できますか。</div>'
          '<div class="a">答えが文章で返る</div></div>')
    b += (f'<div class="mid"><div><div class="lb">質問</div>{ARROW}</div>'
          f'<div class="bk"><div class="lb">回答</div>{ARROW}</div></div>')
    b += f'<div class="ag"><div class="agt"><img src="{ms("copilotstudio")}">Copilot Studio のエージェント</div><div class="gr">'
    b += pt("agent", "名前と指示", "役割・口調・答える範囲・<br>わからないときの対応を書く", "この記事で書く", True)
    b += pt("copilot", "モデル", "Auto のまま", "そのまま")
    b += pt("web", "ナレッジ", "「すべての Web サイトを検索する」<br>が最初から入っている", "そのまま")
    b += pt("tools", "ツール", "Work IQ が最初から入っている", "そのまま")
    b += '</div></div></div>'
    b += ('<div class="notes"><b>用意するもの</b>'
          f'<span class="chip"><img src="{ms("copilotstudio")}">Copilot Studio が使えるアカウント</span>'
          '<span class="chip t">ブラウザー（Edge・Chrome）</span>'
          '<span class="chip t">テストで会話するには Copilot クレジット</span></div>')
    return doc(b, ARCH_CSS)


def route_():
    return route("Copilot Studio の画面のたどり方：ホームからテストまで",
                 "押す場所は5か所。下の番号は、この記事の節の番号と同じ",
                 [("ホーム", "左メニューの<br><em>エージェント</em>", "エージェントの<br>一覧が開く"),
                  ("一覧", "右上の<br><em>新しいエージェント</em>", "作成の画面が開く"),
                  ("作成", "<em>名前</em> と <em>指示</em><br>を書く", "右の部品は<br>そのまま"),
                  ("作成", "右上の<br><em>保存</em> を押す", "保存されました<br>と出る"),
                  ("プレビュー", "<em>プレビュー</em> タブで<br>質問を送る", "答えが返る")],
                 ["①", "①", "②", "③", "④"])


PARTS_CSS = f"""
.sc{{display:flex;gap:18px}}
.left{{flex:1.5;border:2.5px solid #e2e8f0;border-radius:20px;background:#fff;padding:18px 20px}}
.right{{flex:1;border:2.5px solid #e2e8f0;border-radius:20px;background:#fff;padding:14px 18px}}
.zone{{border:2.5px dashed {AC};border-radius:16px;padding:12px 16px;margin-bottom:14px;background:{AC}0a}}
.zone .zt{{font-size:25px;font-weight:800;color:{AC}}}
.zone .zd{{font-size:22px;color:#475569;line-height:1.5;margin-top:4px}}
.it{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1.5px solid #eef2f7;padding:9px 2px}}
.it:last-child{{border-bottom:none}}
.it b{{font-size:24px}}
.it span{{font-size:20px;color:#64748b}}
.hd{{font-size:22px;font-weight:800;color:#475569;background:#e2e8f0;border-radius:999px;display:inline-block;padding:3px 16px;margin-bottom:12px}}
.bar{{display:flex;gap:10px;align-items:center;margin-bottom:16px}}
.tab{{font-size:22px;font-weight:800;border:2px solid #cbd5e1;border-radius:12px;padding:5px 18px;color:#475569;background:#fff}}
.tab.on{{border-color:{AC};color:{AC}}}
.spc{{flex:1}}
"""


def parts():
    b = '<h1>作成の画面の読み方</h1><div class="lead">上にタブと保存、左に書く場所、右に持たせる部品が並ぶ</div>'
    b += ('<div class="bar"><span class="tab on">作成</span><span class="tab">プレビュー</span><span class="tab">評価</span><span class="tab">監視</span>'
          '<span class="spc"></span><span class="tab">保存</span><span class="tab">レビュー</span><span class="tab">公開</span></div>')
    b += '<div class="sc"><div class="left"><div class="hd">左：書く場所</div>'
    b += '<div class="zone"><div class="zt">名前</div><div class="zd">最初は「無題のエージェント」。押すと書き換えられる</div></div>'
    b += ('<div class="zone"><div class="zt">指示</div><div class="zd">エージェントの役割と答え方を文章で書く。<br>'
          '何も書く前は、書き方の説明と例が薄く出ている</div></div></div>')
    b += '<div class="right"><div class="hd">右：持たせる部品</div>'
    for n, d in [("モデル", "Auto"), ("チャネル", "使う場所（Teams など）"), ("スキル", "手順の型"), ("ツール", "Work IQ 入り"),
                 ("ナレッジ", "Web 検索入り"), ("接続されたエージェント", "ほかのエージェント"), ("メモリ", "プレビュー・オフ")]:
        b += f'<div class="it"><b>{n}</b><span>{d}</span></div>'
    b += '</div></div>'
    return doc(b, PARTS_CSS)


def render_all():
    return {n: render(f(), ASSETS / f"fig-{n}.png", h) for n, f, h in
            (("arch", arch, 1000), ("route", route_, 700), ("parts", parts, 1000))}


if __name__ == "__main__":
    for k, v in render_all().items():
        print("fig", k, v)

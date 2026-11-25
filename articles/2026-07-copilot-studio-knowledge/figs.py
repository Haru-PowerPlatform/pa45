#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2594 の図（横長1660px）。arch＝ナレッジを足した構成／route＝画面のたどり方／sources＝追加元の種類。
  python figs.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _figkit import ms, doc, route, render, AC, ARROW  # noqa: E402

ASSETS = HERE / "assets"

ARCH_CSS = f"""
.rw{{display:flex;align-items:stretch}}
.pp{{flex:none;width:300px;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:18px 14px;text-align:center;display:flex;flex-direction:column;justify-content:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
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
.two{{display:flex;gap:14px}}
.pt{{flex:1;border:2.5px solid #e2e8f0;border-radius:18px;padding:14px 16px;background:#fff}}
.pt.on{{border-color:{AC};background:{AC}0d}}
.pt .h{{display:flex;align-items:center;gap:12px;font-size:25px;font-weight:800;margin-bottom:8px}}
.pt .h img{{width:52px;height:52px}}
.pt .d{{font-size:21px;color:#475569;line-height:1.5}}
.src{{display:flex;align-items:center;gap:10px;font-size:22px;font-weight:700;background:#fff;border:1.5px solid #cbd5e1;border-radius:12px;padding:8px 12px;margin-top:8px}}
.src.new{{border:2.5px solid {AC}}}
.src img{{width:36px;height:36px}}
.fb{{flex:none;width:36px;height:36px;border-radius:9px;background:#e0e7ff;color:#3730a3;font-size:19px;font-weight:800;display:flex;align-items:center;justify-content:center}}
.tag{{display:inline-block;font-size:18px;font-weight:800;border-radius:999px;padding:1px 12px;margin-left:6px;color:#fff;background:{AC}}}
.tag.g{{color:#475569;background:#e2e8f0}}
"""


def arch():
    b = '<h1>この記事で足すもの：エージェントに読ませる資料（ナレッジ）</h1>'
    b += '<div class="lead">指示はそのまま。ナレッジにファイルを1つ足すと、答えの根拠が Web からその資料に変わる</div><div class="rw">'
    b += ('<div class="pp"><div class="t">質問する人</div>'
          '<div class="q">第8回のテーマは何ですか。</div>'
          '<div class="a">資料の内容で答える。<br>出典のファイル名が付く</div></div>')
    b += (f'<div class="mid"><div><div class="lb">質問</div>{ARROW}</div>'
          f'<div class="bk"><div class="lb">回答</div>{ARROW}</div></div>')
    b += f'<div class="ag"><div class="agt"><img src="{ms("copilotstudio")}">Copilot Studio のエージェント</div><div class="two">'
    b += (f'<div class="pt"><div class="h"><img src="{ms("agent")}">指示<span class="tag g">そのまま</span></div>'
          '<div class="d">どう答えるかを決める。<br>役割・口調・わからないときの対応</div></div>')
    b += (f'<div class="pt on"><div class="h"><span class="fb" style="width:52px;height:52px;font-size:24px">資</span>ナレッジ<span class="tag">この記事で足す</span></div>'
          '<div class="d">何をもとに答えるかを決める</div>'
          f'<div class="src"><img src="{ms("web")}">すべての Web サイトを検索する</div>'
          f'<div class="src new"><span class="fb">文</span>PA45 勉強会のご案内（ファイル）<span class="tag">追加</span></div></div>')
    b += '</div></div></div>'
    b += ('<div class="notes"><b>用意するもの</b>'
          f'<span class="chip"><img src="{ms("copilotstudio")}">作成済みのエージェント</span>'
          '<span class="chip t">読ませるファイル（Word・PDF・テキストなど）</span>'
          '<span class="chip t">テストで会話するには Copilot クレジット</span></div>')
    return doc(b, ARCH_CSS)


def route_():
    return route("Copilot Studio の画面のたどり方：一覧から「準備完了」まで",
                 "押す場所は5か所。下の番号は、この記事の節の番号と同じ",
                 [("一覧", "<em>エージェント</em> 一覧で<br>対象を押す", "作成の画面が開く"),
                  ("作成", "右の <em>ナレッジ</em> の<br><em>＋</em> を押す", "ナレッジの追加<br>が開く"),
                  ("追加", "上の枠に<br><em>ファイル</em> を入れる", "ファイルの<br>アップロードに進む"),
                  ("追加", "<em>名前</em> と <em>説明</em> を書き<br><em>追加する</em> を押す", "右のナレッジに<br>並ぶ"),
                  ("作成", "並んだ <em>資料の名前</em><br>を押す", "状態が<br>準備完了になる")],
                 ["①", "①", "②", "③", "④"])


SRC_CSS = f"""
.g3{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.c{{background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:16px 18px;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.c.on{{border-color:{AC};background:{AC}0d}}
.c .h{{display:flex;align-items:center;gap:12px;font-size:26px;font-weight:800;margin-bottom:8px}}
.c .h img{{width:56px;height:56px}}
.c .h .bx{{width:56px;height:56px;border-radius:14px;background:#e2e8f0;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:#475569}}
.c .d{{font-size:22px;color:#475569;line-height:1.55}}
.c .w{{display:inline-block;font-size:19px;font-weight:800;color:#fff;background:{AC};border-radius:999px;padding:1px 14px;margin-bottom:8px}}
.c .w.g{{color:#475569;background:#e2e8f0}}
"""


def sources():
    def c(ico, name, d, where, on=False):
        i = f'<img src="{ms(ico)}">' if len(ico) > 1 else f'<div class="bx">{ico}</div>'
        return (f'<div class="c{" on" if on else ""}"><span class="w{"" if on else " g"}">{where}</span>'
                f'<div class="h">{i}{name}</div><div class="d">{d}</div></div>')
    b = '<h1>ナレッジの追加で選べる追加元</h1><div class="lead">「ナレッジの追加」の画面に並ぶもの。この記事では、いちばん上のファイルを使う</div><div class="g3">'
    b += c("文", "ファイル", "手元の Word・PDF・テキストを<br>上の枠に入れる", "上の枠（この記事）", True)
    b += c("web", "公開 Web サイト", "公開されているページの<br>URL を指定する", "おすすめ")
    b += c("sharepoint", "SharePoint", "部署のサイトやライブラリを<br>指定する", "おすすめ")
    b += c("onedrive", "OneDrive for Business", "OneDrive にあるファイルや<br>フォルダーを指定する", "おすすめ")
    b += c("表", "Dataverse", "テーブルに入っている<br>業務データを指定する", "おすすめ")
    b += c("他", "そのほか", "「詳細設定」のタブに<br>ほかの接続先が並ぶ", "詳細設定")
    b += '</div>'
    return doc(b, SRC_CSS)


def render_all():
    return {n: render(f(), ASSETS / f"fig-{n}.png", h) for n, f, h in
            (("arch", arch, 1000), ("route", route_, 700), ("sources", sources, 900))}


if __name__ == "__main__":
    for k, v in render_all().items():
        print("fig", k, v)

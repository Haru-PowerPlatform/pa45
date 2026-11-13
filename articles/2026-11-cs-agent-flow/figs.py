#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2675 の図（横長1660px）。arch＝エージェントとワークフローの構成／route＝画面のたどり方／flow＝ワークフローの中身。
  python figs.py
"""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _figkit import ms, doc, route, render, AC, ARROW  # noqa: E402

ASSETS = HERE / "assets"

CSS = f"""
.rw{{display:flex;align-items:stretch}}
.pp{{flex:none;width:250px;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:18px 14px;text-align:center;display:flex;flex-direction:column;justify-content:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.pp img{{width:76px;height:76px;margin:0 auto 8px;display:block}}
.pp .t{{font-size:26px;font-weight:800;line-height:1.4}}
.pp .q{{font-size:22px;color:#0c4a6e;background:#e0f2fe;border-radius:16px;padding:10px 12px;margin-top:12px;line-height:1.5;text-align:left}}
.pp .d{{font-size:21px;color:#475569;line-height:1.5;margin-top:8px}}
.mid{{flex:none;width:128px;display:flex;flex-direction:column;justify-content:center;gap:50px;padding:0 6px}}
.mid .lb{{font-size:20px;font-weight:800;color:{AC};text-align:center;line-height:1.35;margin-bottom:4px;white-space:nowrap}}
.mid svg{{width:100%;height:26px;display:block}}
.mid line{{stroke:{AC};stroke-width:5}}
.mid polygon{{fill:{AC}}}
.mid .bk svg{{transform:scaleX(-1)}}
.bx{{flex:1;border:3px solid {AC};border-radius:24px;background:#fff;padding:16px 18px 18px}}
.bx.g{{border-color:#0f8a6a}}
.bxt{{display:inline-flex;align-items:center;gap:12px;font-size:24px;font-weight:800;color:#fff;background:{AC};border-radius:999px;padding:6px 22px 6px 10px;margin-bottom:12px}}
.bx.g .bxt{{background:#0f8a6a}}
.bxt img{{width:42px;height:42px;background:#fff;border-radius:50%;padding:4px}}
.it{{border:2.5px solid #e2e8f0;border-radius:16px;padding:10px 14px;background:#fff;margin-top:10px}}
.it.on{{border-color:{AC};background:{AC}0d}}
.it b{{display:block;font-size:23px;line-height:1.4}}
.it span{{display:block;font-size:20px;color:#475569;line-height:1.5}}
.f3{{display:flex;align-items:stretch}}
.nd{{flex:1;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:16px 14px;text-align:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.nd img{{width:72px;height:72px;display:block;margin:0 auto 8px}}
.nd .n{{display:inline-flex;align-items:center;justify-content:center;width:46px;height:46px;border-radius:50%;background:{AC};color:#fff;font-size:25px;font-weight:800;margin-bottom:8px}}
.nd .t{{font-size:24px;font-weight:800;line-height:1.4}}
.nd .e{{font-size:20px;color:#64748b;margin-top:2px}}
.nd .d{{font-size:21px;color:#334155;line-height:1.5;margin-top:10px;background:#f1f5f9;border-radius:12px;padding:8px}}
.ar{{flex:none;width:150px;display:flex;flex-direction:column;justify-content:center;padding:0 6px}}
.ar .lb{{font-size:20px;font-weight:800;color:{AC};text-align:center;line-height:1.35;margin-bottom:4px;white-space:nowrap}}
.ar svg{{width:100%;height:26px;display:block}}
.ar line{{stroke:{AC};stroke-width:5}}
.ar polygon{{fill:{AC}}}
.tk{{display:inline-block;background:#e0e7ff;color:#3730a3;border-radius:8px;padding:0 8px;font-weight:800}}
"""


def arch():
    b = '<h1>この記事で作るもの：エージェントから呼ぶワークフロー</h1>'
    b += '<div class="lead">会話で受けた質問を、ワークフローが Excel に1行ずつ記録する</div><div class="rw">'
    b += '<div class="pp"><div class="t">質問する人</div><div class="q">第8回のテーマは<br>何ですか。</div></div>'
    b += f'<div class="mid"><div><div class="lb">質問</div>{ARROW}</div><div class="bk"><div class="lb">回答</div>{ARROW}</div></div>'
    b += f'<div class="bx"><div class="bxt"><img src="{ms("copilotstudio")}">エージェント</div>'
    b += '<div class="it"><b>指示・ナレッジ</b><span>質問に答える</span></div>'
    b += '<div class="it on"><b>ツール：質問を記録する</b><span>ワークフローをツールとして持つ。<br>AI の説明に、使う場面を書く</span></div></div>'
    b += f'<div class="mid"><div><div class="lb">質問の文章</div>{ARROW}</div><div class="bk"><div class="lb">結果</div>{ARROW}</div></div>'
    b += f'<div class="bx g"><div class="bxt"><img src="{ms("flow")}">ワークフロー</div>'
    b += '<div class="it"><b>エージェントが呼び出す</b><span>入力：質問</span></div>'
    b += '<div class="it"><b>表に行を追加</b><span>日時と質問を1行足す</span></div>'
    b += '<div class="it"><b>エージェントに返す</b><span>出力：結果</span></div></div>'
    b += f'<div class="mid"><div><div class="lb">1行追加</div>{ARROW}</div></div>'
    b += f'<div class="pp"><img src="{ms("excel")}"><div class="t">質問箱</div><div class="d">OneDrive の Excel<br>テーブル：質問ログ</div></div>'
    b += '</div>'
    b += ('<div class="notes"><b>用意するもの</b>'
          f'<span class="chip"><img src="{ms("copilotstudio")}">作成済みのエージェント</span>'
          f'<span class="chip"><img src="{ms("excel")}">テーブルにした Excel（OneDrive）</span>'
          '<span class="chip t">公開と実行には Copilot Studio の容量（クレジット）</span></div>')
    return doc(b, CSS)


def route_():
    return route("Copilot Studio の画面のたどり方：ワークフローを作ってエージェントにつなぐ",
                 "前半はワークフローの画面、後半はエージェントの画面。下の番号は節の番号と同じ",
                 [("ワークフロー", "<em>新しいワークフロー</em><br>→ トリガーを変える", "入口と出口の<br>2つが並ぶ"),
                  ("編集画面", "入口に <em>入力</em> を足し<br><em>＋</em> で Excel を足す", "行に日時と質問<br>を入れる"),
                  ("編集画面", "出口に <em>出力</em> を足し<br><em>保存</em> → <em>公開</em>", "公開済みになる"),
                  ("エージェント", "<em>ツール</em> の <em>＋</em> →<br><em>ワークフロー</em> タブ", "公開済みのもの<br>だけ選べる"),
                  ("エージェント", "<em>AI の説明</em> を書き<br><em>保存</em>", "ツールに並ぶ")],
                 ["①", "②", "③", "④", "④"])


def flow():
    def a(lb):
        return f'<div class="ar"><div class="lb">{lb}</div>{ARROW}</div>'
    b = '<h1>ワークフローの中身：3つのステップ</h1><div class="lead">トリガーを変えると、入口と出口が最初から並ぶ。そのあいだに Excel のステップを1つ足す</div><div class="f3">'
    b += (f'<div class="nd"><div class="n">①</div><img src="{ms("agent")}"><div class="t">エージェントが呼び出す</div>'
          '<div class="e">When an agent calls the flow</div><div class="d">入力：<span class="tk">質問</span>（Text）</div></div>')
    b += a("質問")
    b += (f'<div class="nd"><div class="n">②</div><img src="{ms("excel")}"><div class="t">表に行を追加</div>'
          '<div class="e">Excel Online (Business)</div><div class="d">日時＝現在時刻の式<br>質問＝<span class="tk">質問</span></div></div>')
    b += a("")
    b += (f'<div class="nd"><div class="n">③</div><img src="{ms("flow")}"><div class="t">エージェントに返す</div>'
          '<div class="e">Respond to the agent</div><div class="d">出力：<span class="tk">結果</span>（Text）</div></div>')
    b += '</div>'
    return doc(b, CSS)


def render_all():
    return {n: render(f(), ASSETS / f"fig-{n}.png", h) for n, f, h in
            (("arch", arch, 1100), ("route", route_, 700), ("flow", flow, 800))}


if __name__ == "__main__":
    for k, v in render_all().items():
        print("fig", k, v)

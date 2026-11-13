#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post 2710 の図（横長1660px・Microsoft の製品アイコン入り）。
  arch  … 冒頭の構成図（どの製品をどう組み合わせるか）
  route … 画面のたどり方（どこを押して編集画面に着くか）
  data  … ステップの間で受け渡すデータ（どの出力をどの欄に入れるか）
アイコン＝assets-icons\\ms（改変しない）。「繰り返し」の時計は撮った実画面から切り出した。
  python figs.py
"""
import base64, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _archkit import render_html, icon  # noqa: E402

AC = "#7c3aed"
W = 1660
ASSETS = HERE / "assets"
MS_LOCAL = HERE.parent / "2026-11-cs-case-hr-rules-help" / "assets" / "ms"


def clock():
    f = ASSETS / "ic-recurrence.png"
    if not f.exists():
        from PIL import Image
        im = Image.open(HERE.parent / "_shots" / "raw-nav" / "07-recurrence-done.png")
        im.crop((760, 797, 828, 863)).resize((192, 192), Image.LANCZOS).save(f)
    return "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode()


def ms(name):
    if name == "recurrence":
        return clock()
    f = MS_LOCAL / f"{name}.png"
    if f.exists():
        return "data:image/png;base64," + base64.b64encode(f.read_bytes()).decode()
    return icon(name)


BASE = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;background:#fff;font-family:'Noto Sans JP','Yu Gothic UI','Meiryo',sans-serif;color:#1f2937}}
.wrap{{margin:8px;padding:30px 34px 30px;border:3px solid {AC}33;border-radius:26px;background:linear-gradient(180deg,#fff,#faf8ff)}}
h1{{font-size:36px;font-weight:800;color:{AC};display:flex;align-items:center;gap:14px;line-height:1.35;margin-bottom:6px}}
h1:before{{content:"";flex:none;width:10px;height:40px;border-radius:5px;background:{AC}}}
.lead{{font-size:25px;color:#475569;margin:0 0 22px 24px;line-height:1.6}}
.band{{border:3px solid {AC};border-radius:24px;background:#fff;padding:20px 22px 24px;position:relative}}
.bandt{{display:inline-flex;align-items:center;gap:12px;font-size:27px;font-weight:800;color:#fff;background:{AC};border-radius:999px;padding:6px 24px 6px 10px;margin-bottom:18px}}
.bandt img{{width:46px;height:46px;background:#fff;border-radius:50%;padding:4px}}
.row{{display:flex;align-items:stretch;justify-content:space-between}}
.nd{{flex:1;min-width:0;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:16px 14px 18px;text-align:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.nd.hl{{border-color:{AC}}}
.num{{display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:50%;background:{AC};color:#fff;font-size:27px;font-weight:800;margin-bottom:8px}}
.nd img.ic{{width:84px;height:84px;display:block;margin:0 auto 8px}}
.nm{{font-size:27px;font-weight:800;line-height:1.35}}
.ac{{white-space:nowrap;font-size:21px;color:#334155;line-height:1.5;margin-top:8px;background:#f1f5f9;border-radius:12px;padding:8px 8px}}
.tx{{white-space:nowrap;font-size:23px;color:#475569;line-height:1.55;margin-top:8px}}
.ar{{flex:none;width:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 4px}}
.ar .lb{{white-space:nowrap;font-size:21px;font-weight:800;color:{AC};text-align:center;line-height:1.35;margin-bottom:6px;min-height:58px;display:flex;align-items:flex-end}}
.ar svg{{width:100%;height:26px;display:block}}
.ar line{{stroke:{AC};stroke-width:5}}
.ar polygon{{fill:{AC}}}
.below{{display:flex;justify-content:space-between;margin-top:0}}
.bl{{flex:1;display:flex;flex-direction:column;align-items:center}}
.gap{{flex:none;width:150px}}
.stem{{width:4px;height:30px;background:repeating-linear-gradient(180deg,#94a3b8 0 6px,transparent 6px 11px)}}
.att{{display:flex;align-items:center;gap:12px;background:#f8fafc;border:2.5px dashed #cbd5e1;border-radius:18px;padding:12px 14px;width:100%;text-align:left}}
.att img{{flex:none;width:56px;height:56px}}
.att b{{white-space:nowrap;display:block;font-size:22px;line-height:1.35}}
.att span{{white-space:nowrap;display:block;font-size:19px;color:#64748b;line-height:1.45}}
.notes{{margin-top:22px;padding:16px 20px;background:#f1f5f9;border-radius:18px;display:flex;flex-wrap:wrap;align-items:center;gap:12px}}
.notes b{{font-size:24px;color:#0f172a;margin-right:6px}}
.chip{{display:inline-flex;align-items:center;gap:10px;background:#fff;border:1.5px solid #cbd5e1;border-radius:999px;padding:6px 18px 6px 10px;font-size:23px;font-weight:700}}
.chip img{{width:38px;height:38px}}
.chip.t{{padding-left:18px}}
"""
ARROW = '<svg viewBox="0 0 100 26" preserveAspectRatio="none"><line x1="0" y1="13" x2="84" y2="13"/><polygon points="80,2 100,13 80,24"/></svg>'


def ar(label=""):
    return f'<div class="ar"><div class="lb">{label}</div>{ARROW}</div>'


def nd(n, ico, name, action, text, hl=False):
    return (f'<div class="nd{" hl" if hl else ""}"><div class="num">{n}</div><img class="ic" src="{ms(ico)}">'
            f'<div class="nm">{name}</div><div class="ac">{action}</div><div class="tx">{text}</div></div>')


def att(ico, title, sub):
    return f'<div class="stem"></div><div class="att"><img src="{ms(ico)}"><div><b>{title}</b><span>{sub}</span></div></div>'


def doc(body, extra=""):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE}{extra}</style></head><body><div class="wrap">{body}</div></body></html>'


def arch():
    b = '<h1>この記事で作るもの：毎朝9時に、質問箱の要約が Teams に届く</h1>'
    b += '<div class="lead">Copilot Studio のワークフロー1本の中で、4つのステップを左から順につなぐ</div>'
    b += f'<div class="band"><div class="bandt"><img src="{ms("copilotstudio")}">Copilot Studio のワークフロー</div><div class="row">'
    b += nd("①", "recurrence", "繰り返し<br>&nbsp;", "トリガーの種類<br>＝繰り返し", "毎日 9時0分に起動<br>タイム ゾーンは東京", True)
    b += ar("時刻が<br>来たら")
    b += nd("②", "excel", "Excel Online<br>(Business)", "表内に存在する行を<br>一覧表示", "質問箱のテーブルを<br>全行読む")
    b += ar("Value<br>質問の一覧")
    b += nd("③", "copilot", "Copilot<br>&nbsp;", "Copilot Chatを実行<br>&nbsp;", "一覧を3行以内に<br>要約する")
    b += ar("Response<br>要約の文章")
    b += nd("④", "teams", "Microsoft<br>Teams", '<span style="font-size:18.5px">チャットまたはチャネルで<br>メッセージを投稿する</span>', "フロー ボットから<br>担当者へ届く")
    b += '</div><div class="below">'
    b += '<div class="bl"></div><div class="gap"></div>'
    b += f'<div class="bl">{att("onedrive", "OneDrive for Business", "コパスタ45_質問箱.xlsx<br>テーブル：質問ログ")}</div><div class="gap"></div>'
    b += f'<div class="bl">{att("copilot", "接続：M365 Copilot", "Microsoft 365 Copilot の<br>ライセンスで動く")}</div><div class="gap"></div>'
    b += f'<div class="bl">{att("teams", "担当者の Teams", "フロー ボットとの<br>チャットに表示")}</div>'
    b += '</div></div>'
    b += ('<div class="notes"><b>用意するもの</b>'
          f'<span class="chip"><img src="{ms("copilotstudio")}">Copilot Studio が使えるアカウント</span>'
          f'<span class="chip"><img src="{ms("excel")}">テーブルにした Excel（OneDrive）</span>'
          f'<span class="chip"><img src="{ms("copilot")}">Microsoft 365 Copilot ライセンス</span>'
          f'<span class="chip"><img src="{ms("teams")}">Teams</span>'
          '<span class="chip t">公開して動かすときは Copilot クレジット</span></div>')
    return doc(b)


ROUTE_CSS = f"""
.rt{{display:flex;align-items:stretch}}
.st{{flex:1;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:16px 12px 16px;text-align:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.st .where{{font-size:21px;font-weight:800;color:#475569;background:#e2e8f0;border-radius:999px;display:inline-block;padding:3px 14px;margin-bottom:10px}}
.st .do{{font-size:26px;font-weight:800;line-height:1.4}}
.st .do em{{font-style:normal;color:{AC}}}
.st .res{{font-size:22px;color:#475569;line-height:1.5;margin-top:10px}}
.ar2{{flex:none;width:54px;display:flex;align-items:center;justify-content:center}}
.ar2 svg{{width:44px;height:26px}}
.ar2 line{{stroke:{AC};stroke-width:5}}
.ar2 polygon{{fill:{AC}}}
.sec{{display:flex;margin-top:14px}}
.sec div{{flex:1;text-align:center;font-size:22px;font-weight:800;color:{AC}}}
.sec .sp{{flex:none;width:54px}}
"""
A2 = '<div class="ar2"><svg viewBox="0 0 44 26"><line x1="0" y1="13" x2="30" y2="13"/><polygon points="26,2 44,13 26,24"/></svg></div>'


def route():
    steps = [("ホーム", "左メニューの<br><em>ワークフロー</em>", "ワークフローの<br>一覧が開く"),
             ("一覧", "右上の<br><em>新しいワークフロー</em>", "編集画面が開く<br>「開始」が1つある"),
             ("編集画面", "<em>開始</em> を押して<br>トリガーを変える", "「繰り返し」になる"),
             ("編集画面", "右の <em>＋</em> で<br>ステップを足す", "Excel・Copilot・Teams<br>の順に3回"),
             ("編集画面", "名前を付けて<br><em>保存</em> を押す", "一覧に「ドラフト」<br>で並ぶ")]
    b = f'<h1><img src="{ms("copilotstudio")}" style="width:52px;height:52px">Copilot Studio の画面のたどり方：ホームから保存まで</h1><div class="lead">押す場所は5か所。下の番号は、この記事の節の番号と同じ</div><div class="rt">'
    for i, (w, d, r) in enumerate(steps):
        b += f'<div class="st"><div class="where">{w}</div><div class="do">{d}</div><div class="res">{r}</div></div>'
        if i < len(steps) - 1:
            b += A2
    b += '</div><div class="sec"><div>準備</div><div class="sp"></div><div>準備</div><div class="sp"></div><div>①</div><div class="sp"></div><div>②③④</div><div class="sp"></div><div>⑤</div></div>'
    return doc(b, ROUTE_CSS)


DATA_CSS = f"""
.dt{{display:flex;align-items:center}}
.bx{{flex:1;background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:16px 16px 18px;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.bx .hd{{display:flex;align-items:center;gap:12px;font-size:26px;font-weight:800;margin-bottom:12px}}
.bx .hd img{{width:54px;height:54px}}
.io{{font-size:22px;line-height:1.5;border-radius:12px;padding:8px 12px;margin-top:8px}}
.io b{{display:block;font-size:19px;color:#64748b}}
.in{{background:#f1f5f9}}
.out{{background:{AC}14;border:2px solid {AC}55}}
.tk{{display:inline-block;background:#e0e7ff;color:#3730a3;border-radius:8px;padding:1px 10px;font-weight:800}}
.ar3{{flex:none;width:150px;text-align:center}}
.ar3 .lb{{font-size:21px;font-weight:800;color:{AC};line-height:1.35;margin-bottom:6px}}
.ar3 svg{{width:100%;height:26px}}
.ar3 line{{stroke:{AC};stroke-width:5}}
.ar3 polygon{{fill:{AC}}}
.hint{{margin-top:20px;font-size:24px;color:#334155;background:#f1f5f9;border-radius:16px;padding:14px 20px;line-height:1.6}}
.hint b{{color:{AC}}}
"""


def data():
    def a3(lb):
        return f'<div class="ar3"><div class="lb">{lb}</div>{ARROW}</div>'
    b = '<h1>ステップの間で受け渡すもの</h1><div class="lead">前のステップの出力を、次のステップの入力欄に差し込む。差し込みは2か所</div><div class="dt">'
    b += (f'<div class="bx"><div class="hd"><img src="{ms("excel")}">② Excel</div>'
          '<div class="io in"><b>設定する欄</b>場所・ドキュメント ライブラリ<br>ファイル・テーブル</div>'
          '<div class="io out"><b>出力</b><span class="tk">Value</span> 全行のまとまり</div></div>')
    b += a3("Message 欄に<br>差し込む")
    b += (f'<div class="bx"><div class="hd"><img src="{ms("copilot")}">③ Copilot</div>'
          '<div class="io in"><b>Message 欄</b>要約の指示文 ＋ <span class="tk">Value</span></div>'
          '<div class="io out"><b>出力</b><span class="tk">Response</span> 要約の文章</div></div>')
    b += a3("メッセージ欄に<br>差し込む")
    b += (f'<div class="bx"><div class="hd"><img src="{ms("teams")}">④ Teams</div>'
          '<div class="io in"><b>メッセージ欄</b>見出しの文 ＋ <span class="tk">Response</span></div>'
          '<div class="io in"><b>Recipient 欄</b>通知する担当者</div></div>')
    b += '</div><div class="hint">入力欄で半角の <b>/</b> を打つと、前のステップの出力の一覧（動的コンテンツ）が開く</div>'
    return doc(b, DATA_CSS)


def render_all():
    out = {}
    for name, fn, h in (("arch", arch, 1100), ("route", route, 700), ("data", data, 800)):
        out[name] = render_html(fn(), ASSETS / f"fig-{name}.png", width=W, height=h)
    return out


if __name__ == "__main__":
    for k, v in render_all().items():
        print("fig", k, v)

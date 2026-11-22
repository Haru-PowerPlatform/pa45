#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""AB-730 勉強法の記事の図。
  arch / arch_sp … 勉強の構成（Learn → Claude → M365 Copilot の実画面 → 復習カード）
  loop           … 1問の回し方（5手）
  map            … 学習ガイドの4分野と、実画面で確かめた場所
  python figs.py
"""
import base64, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _figkit import ms, doc, route, render, AC, ARROW  # noqa: E402
from _archkit import render_html  # noqa: E402

ASSETS = HERE / "assets"
SVG_DIR = pathlib.Path(r"C:\Users\isamu\Documents\pa45\assets\x\pptx\_assets\icons\ms")


def svg(name):
    return "data:image/svg+xml;base64," + base64.b64encode((SVG_DIR / f"{name}.svg").read_bytes()).decode()


# Claude はアイコンを使わず、文字の札にする（他社のロゴを図に入れない）
AI_BADGE = '<div class="aib">AI</div>'
CARD_BADGE = '<div class="aib cd"><span></span><span></span><span></span></div>'

CSS = f"""
.rw{{display:flex;align-items:stretch}}
.bx{{flex:1;min-width:0;border:2.5px solid #e2e8f0;border-radius:22px;background:#fff;padding:16px 14px 18px;text-align:center;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.bx.hl{{border:3px solid {AC};background:{AC}08}}
.bx .who{{display:inline-block;font-size:20px;font-weight:800;color:#475569;background:#e2e8f0;border-radius:999px;padding:3px 16px;margin-bottom:8px}}
.bx.hl .who{{background:{AC};color:#fff}}
.bx img.big{{width:84px;height:84px;display:block;margin:2px auto 8px}}
.aib{{width:84px;height:84px;margin:2px auto 8px;border-radius:22px;background:#334155;color:#fff;font-size:34px;font-weight:900;display:flex;align-items:center;justify-content:center;letter-spacing:.04em}}
.aib.cd{{background:#fff;border:4px solid #94a3b8;flex-direction:column;gap:8px;padding:0 14px}}
.aib.cd span{{display:block;width:100%;height:6px;border-radius:3px;background:#94a3b8}}
.bx .t1{{font-size:27px;font-weight:800;line-height:1.35}}
.bx .d{{font-size:21px;color:#475569;line-height:1.6;margin-top:8px;white-space:nowrap}}
.mid{{flex:none;width:150px;display:flex;flex-direction:column;justify-content:center;padding:0 6px}}
.mid .lb{{font-size:20px;font-weight:800;color:{AC};text-align:center;line-height:1.4;margin-bottom:6px}}
.mid svg{{width:100%;height:26px;display:block}}
.mid line{{stroke:{AC};stroke-width:5}}
.mid polygon{{fill:{AC}}}
.apps{{display:flex;justify-content:center;gap:10px;margin-top:12px}}
.apps img{{width:46px;height:46px;background:#fff;border:1.5px solid #e2e8f0;border-radius:12px;padding:5px}}
.back{{margin:12px 0 0;position:relative;height:66px}}
.back svg{{position:absolute;inset:0;width:100%;height:46px}}
.back path{{fill:none;stroke:#94a3b8;stroke-width:4;stroke-dasharray:10 8}}
.back polygon{{fill:#94a3b8}}
.back .bl{{position:absolute;left:50%;top:22px;transform:translateX(-50%);background:#fff;padding:2px 18px;font-size:22px;font-weight:800;color:#475569;white-space:nowrap}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
.c{{background:#fff;border:2.5px solid #e2e8f0;border-radius:20px;padding:16px 20px 18px;box-shadow:0 4px 14px rgba(15,23,42,.07)}}
.c .h{{display:flex;align-items:center;gap:14px;margin-bottom:10px}}
.c .h img{{width:54px;height:54px;flex:none}}
.c .h b{{font-size:25px;line-height:1.35}}
.c .h small{{display:block;font-size:19px;color:{AC};font-weight:800}}
.c ul{{list-style:none;display:flex;flex-wrap:wrap;gap:8px}}
.c li{{font-size:20px;font-weight:700;background:#f1f5f9;border-radius:999px;padding:5px 14px;color:#334155}}
.c li.lr{{background:#fff;border:1.5px dashed #94a3b8;color:#64748b}}
"""


def _nodes():
    learn = ('<div class="bx"><span class="who">① 解く</span>'
             f'<img class="big" src="{ms("web")}"><div class="t1">Microsoft Learn</div>'
             '<div class="d">学習ガイドと<br>練習問題を解く</div></div>')
    ai = ('<div class="bx"><span class="who">② 聞く</span>' + AI_BADGE +
          '<div class="t1">Claude</div>'
          '<div class="d">選択肢ごとの ○× と理由、<br>たとえの図を<br>出してもらう</div></div>')
    cop = ('<div class="bx hl"><span class="who">③ 画面で確かめる</span>'
           f'<img class="big" src="{ms("copilot")}"><div class="t1">Microsoft 365 Copilot</div>'
           '<div class="d">その画面を開いて押す。<br>Copilot にも聞いて<br>出典を開く</div>'
           f'<div class="apps"><img src="{svg("word")}"><img src="{svg("excel")}"><img src="{svg("outlook")}"><img src="{svg("teams")}"></div></div>')
    card = ('<div class="bx"><span class="who">④ 残す</span>' + CARD_BADGE +
            '<div class="t1">復習カード</div>'
            '<div class="d">1問を1行に。<br>決め手の言葉だけ書く</div></div>')
    return learn, ai, cop, card


def arch():
    def mid(lb):
        return f'<div class="mid"><div class="lb">{lb}</div>{ARROW}</div>'
    learn, ai, cop, card = _nodes()
    b = '<h1>AB-730 を例にした勉強の構成：試験の言葉と、実際の画面を1問ずつ結び付ける</h1>'
    b += '<div class="lead">知識は Learn と Claude で、操作は Microsoft 365 Copilot の実画面で。1問ごとに ①〜④ を回した</div>'
    b += '<div class="rw">' + learn + mid("説明できない<br>問題") + ai + mid("画面の名前が<br>分かったら") + cop + mid("決め手を<br>1行で") + card + '</div>'
    b += ('<div class="back"><svg viewBox="0 0 1000 46" preserveAspectRatio="none"><path d="M935 0 V30 H65 V8"/>'
          '<polygon points="57,12 65,0 73,12"/></svg><div class="bl">次の回の練習問題へ（くり返す）</div></div>')
    b += ('<div class="notes"><b>前提</b>'
          f'<span class="chip"><img src="{ms("copilot")}">Microsoft 365 Copilot のライセンスがあるテナント</span>'
          '<span class="chip t">管理者側の画面は Learn のページで確認</span>'
          '<span class="chip t">問題文は外に出さない</span></div>')
    return doc(b, CSS)


def arch_sp():
    learn, ai, cop, card = _nodes()
    dn = ('<div style="text-align:center;margin:6px 0"><svg viewBox="0 0 26 40" style="width:26px;height:40px">'
          f'<line x1="13" y1="0" x2="13" y2="26" stroke="{AC}" stroke-width="5"/><polygon points="2,22 13,40 24,22" fill="{AC}"/></svg></div>')
    b = '<h1>AB-730 の勉強の構成</h1><div class="lead">1問ごとに ①〜④ を回した</div>'
    b += learn + dn + ai + dn + cop + dn + card
    extra = CSS + "body{width:720px}.lead{margin-left:24px}.bx .d{font-size:24px}"
    return doc(b, extra)


def loop():
    return route("1問の回し方：解く → 聞く → 開く → 聞き直す → 残す",
                 "練習問題の1問ごとに、この5手を回した。③と④が、知識だけの勉強との違い",
                 [("Learn", "練習問題を<br><em>解く</em>", "理由を説明でき<br>ない問題に印"),
                  ("Claude", "<em>選択肢ごと</em>に<br>○× と理由を聞く", "出てくる画面の<br>名前が分かる"),
                  ("Copilot", "その画面を<br><em>開いて押す</em>", "言葉と画面が<br>結び付く"),
                  ("Copilot", "Copilot にも聞き<br><em>出典</em>を開く", "公式の言葉で<br>裏が取れる"),
                  ("カード", "決め手を<br><em>1行</em>で残す", "次の回の前に<br>見直す")],
                 ["①", "②", "③", "④", "⑤"], product="copilot")


def dmap():
    def c(icons, name, pct, items, learn_only=()):
        ims = "".join(f'<img src="{i}">' for i in icons)
        lis = "".join(f"<li>{x}</li>" for x in items) + "".join(f'<li class="lr">{x}</li>' for x in learn_only)
        return f'<div class="c"><div class="h">{ims}<div><small>{pct}</small><b>{name}</b></div></div><ul>{lis}</ul></div>'
    b = '<h1>学習ガイドの4つの分野と、実画面で確かめた場所</h1>'
    b += '<div class="lead">分野の名前は 2026年10月20日 改訂後の学習ガイド。点線は自分のテナントで画面を出せず、Learn のページで確かめたもの</div><div class="g2">'
    b += c([ms("copilot")], "生成 AI の基礎を理解する", "分野1",
           ["Work IQ のオン・オフ", "エンタープライズ データ保護の盾", "モデルの選択", "答えの出典"],
           ["Copilot Cowork", "秘密度ラベル・DLP"])
    b += c([ms("copilot")], "プロンプトとチャットを管理する", "分野2",
           ["プロンプトの保存", "保存済みのプロンプト", "スケジュール", "ノートブック"])
    b += c([svg("word"), svg("excel")], "ビジネス コンテンツとコラボレーションを管理する", "分野3",
           ["Word で下書き", "Excel で分析", "Pages で編集", "会議の準備"],
           ["会議の要約・ファシリテーター"])
    b += c([ms("agent")], "エージェントを使用してビジネス成果を実現する", "分野4",
           ["エージェントの一覧", "リサーチ ツール", "アナリスト"])
    b += '</div>'
    return doc(b, CSS)


# ---------------------------------------------------------------- 流れの図（レーン型）
LANE_CSS = f"""
.lanes{{display:flex;flex-direction:column;gap:22px}}
.lane{{display:flex;align-items:stretch;background:#f8fafc;border:2px solid #e2e8f0;border-radius:22px;padding:16px 16px}}
.lane.ac{{background:{AC}0a;border-color:{AC}66}}
.lane.ng{{background:#f8fafc;border-style:dashed}}
.ll{{flex:none;width:190px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:6px;padding-right:12px}}
.ll b{{font-size:25px;line-height:1.35;color:#0f172a}}
.ll span{{font-size:19px;color:#64748b;line-height:1.4}}
.ll .tg{{font-size:18px;font-weight:800;color:#fff;background:{AC};border-radius:999px;padding:2px 14px}}
.lane.ng .ll .tg{{background:#94a3b8}}
.nd2{{flex:1;min-width:0;background:#fff;border:2.5px solid #e2e8f0;border-radius:18px;padding:12px 10px 14px;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 3px 10px rgba(15,23,42,.06)}}
.nd2.hl{{border-color:{AC};border-width:3px}}
.nd2.ok{{border-color:#16a34a;border-width:3px;background:#f0fdf4}}
.nd2.bad{{border-color:#cbd5e1;border-style:dashed;background:#f8fafc;color:#64748b}}
.nd2 .ics{{display:flex;gap:6px;justify-content:center;margin-bottom:6px}}
.nd2 .ics img{{width:50px;height:50px}}
.nd2 .ics .tx{{height:50px;display:flex;align-items:center;font-size:20px;font-weight:900;color:#fff;background:#334155;border-radius:12px;padding:0 12px}}
.nd2 .t{{font-size:23px;font-weight:800;line-height:1.35;white-space:nowrap}}
.nd2 .s{{font-size:19px;color:#475569;line-height:1.45;margin-top:5px}}
.nd2 .ch{{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin-top:8px}}
.nd2 .ch i{{font-style:normal;font-size:17px;font-weight:700;background:#f1f5f9;border:1.5px solid #e2e8f0;border-radius:999px;padding:2px 10px;white-space:nowrap}}
.ar3{{flex:none;width:96px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 4px}}
.ar3 .lb{{font-size:17px;font-weight:800;color:{AC};text-align:center;line-height:1.3;margin-bottom:4px;white-space:nowrap}}
.ar3 svg{{width:70px;height:24px}}
.ar3 line{{stroke:{AC};stroke-width:5}}
.ar3 polygon{{fill:{AC}}}
.lane.ng .ar3 line{{stroke:#94a3b8}}
.lane.ng .ar3 polygon{{fill:#94a3b8}}
.lane.ng .ar3 .lb{{color:#64748b}}
.foot{{margin-top:20px;font-size:23px;font-weight:800;color:#0f172a;background:#fff;border:2.5px solid {AC};border-radius:18px;padding:12px 20px;text-align:center}}
.foot em{{font-style:normal;color:{AC}}}
"""
AR3 = '<svg viewBox="0 0 70 24"><line x1="0" y1="12" x2="54" y2="12"/><polygon points="50,2 70,12 50,22"/></svg>'


def N(t, s="", icons=(), cls="", chips=()):
    """レーンの箱。icons は data URI か ('tx', '文字')。"""
    ic = ""
    for i in icons:
        ic += f'<div class="tx">{i[1]}</div>' if isinstance(i, tuple) else f'<img src="{i}">'
    ic = f'<div class="ics">{ic}</div>' if ic else ""
    ch = "".join(f"<i>{c}</i>" for c in chips)
    return (f'<div class="nd2 {cls}">{ic}<div class="t">{t}</div>'
            f'{f"<div class=s>{s}</div>" if s else ""}{f"<div class=ch>{ch}</div>" if ch else ""}</div>')


def lane(tag, name, sub, items, cls="ac"):
    """items = [N(...), '矢印のラベル', N(...), ...]（箱と矢印ラベルを交互に）"""
    b = f'<div class="lane {cls}"><div class="ll"><span class="tg">{tag}</span><b>{name}</b><span>{sub}</span></div>'
    for k, it in enumerate(items):
        b += it if k % 2 == 0 else f'<div class="ar3"><div class="lb">{it}</div>{AR3}</div>'
    return b + "</div>"


def flow(title, lead, lanes_html, foot="", icon=None):
    h = f'<img src="{icon}" style="width:52px;height:52px">' if icon else ""
    b = f'<h1>{h}{title}</h1><div class="lead">{lead}</div><div class="lanes">{"".join(lanes_html)}</div>'
    if foot:
        b += f'<div class="foot">{foot}</div>'
    return doc(b, LANE_CSS)


CL = ("tx", "AI")  # Claude の札


def f_compare():
    return flow("知識だけの勉強と、画面で確かめる勉強の違い",
                "同じ練習問題でも、③④を足すと、試験の言葉が職場の操作につながる",
                [lane("A", "知識だけ", "答えを覚える", [
                    N("練習問題を解く", "答え合わせ", [ms("web")]), "",
                    N("答えを覚える", "正解の選択肢だけ"), "",
                    N("試験", "同じ言い回しなら解ける"), "",
                    N("職場で使う", "画面と結び付かない", cls="bad")], cls="ng"),
                 lane("B", "画面で確かめる", "この記事の進め方", [
                    N("練習問題を解く", "説明できない問題に印", [ms("web")]), "",
                    N("理由を聞く", "選択肢ごとの ○×", [CL]), "",
                    N("画面で押す", "何が変わるかを見る", [ms("copilot")], cls="hl"), "",
                    N("出典を開く", "Learn の言葉で確認", [ms("web")]), "",
                    N("試験と職場", "どちらでも使える", cls="ok")])],
                foot="違いは <em>③ 画面で押す</em> と <em>④ 出典を開く</em> の2手")


def f_claude():
    return flow("Claude に出してもらう解説の形",
                "1問を、選択肢ごとの理由・たとえ・決め手・画面の名前に分けて返してもらう",
                [lane("②", "Claude に聞く", "1問ずつ", [
                    N("練習問題の1問", "自分の言葉で伝える", [ms("web")]), "聞く",
                    N("選択肢ごとの ○×", "ほかがちがう理由", [CL], chips=["A ○", "B ×", "C ×", "D ×"]), "",
                    N("たとえの図", "例：防犯カメラ", [CL]), "",
                    N("決め手の言葉", "答えを決める1語", [CL]), "",
                    N("画面の名前", "③で開く場所", [ms("copilot")], cls="hl")])],
                foot="最後の <em>画面の名前</em> が、次の ③ 実画面で確かめる につながる")


def f_workiq():
    return flow("Work IQ のオン・オフで、答えの材料が変わる",
                "入力欄の上に出る候補の違いは、Copilot が何を材料にするかの違い",
                [lane("オフ", "Work IQ オフ", "一般の材料", [
                    N("質問を入力", "チャット画面", [ms("copilot")]), "材料",
                    N("Web など", "一般の情報", [ms("web")]), "",
                    N("一般の候補", "", chips=["学習", "検索", "要約する", "提案"])], cls="ng"),
                 lane("オン", "Work IQ オン", "職場の材料", [
                    N("質問を入力", "チャット画面", [ms("copilot")]), "材料",
                    N("職場のデータ", "メール・会議・ファイル", [svg("outlook"), svg("teams"), ms("onedrive"), ms("sharepoint")], cls="hl"), "",
                    N("職場の候補", "", chips=["会議準備", "人物検索", "プロジェクト管理"])])],
                foot="問題で <em>職場のメールや会議を材料に</em> と出たら、この切り替えの話")


def f_verify():
    return flow("Copilot の答えを確かめる流れ",
                "Copilot に聞いた答えも、そのまま覚えずに出典で読み直す。これ自体が試験範囲の検証手順",
                [lane("④", "聞き直す", "出典を開く", [
                    N("Copilot に聞く", "公式情報を出典に3行で", [ms("copilot")]), "",
                    N("答えを読む", "記号の残り・言葉の抜け", cls="bad"), "",
                    N("「ソース」を押す", "出典の一覧が開く", [ms("copilot")], cls="hl"), "",
                    N("Learn で読み直す", "公式の言葉で確認", [ms("web")]), "",
                    N("決め手を1行に", "復習カード", cls="ok")])],
                foot="試験範囲の <em>引用文献チェック・人的レビュー</em> を、勉強の中で毎回やっていることになる")


def f_prompt():
    return flow("プロンプトの保存とスケジュールの違い",
                "どちらも答えの近くから始まる。違いは、自分で呼び出すか、決まった時刻に動くか",
                [lane("保存", "保存", "あとで自分で使う", [
                    N("答えの近くで保存", "タイトルを付ける", [ms("copilot")]), "",
                    N("保存済みのプロンプト", "プロンプトの一覧", cls="hl"), "",
                    N("自分で呼び出す", "必要なときに", cls="ok")]),
                 lane("予定", "スケジュール", "決まった時刻に動く", [
                    N("答えの下の …", "このプロンプトをスケジュールする", [ms("copilot")]), "",
                    N("曜日・時刻・終了日", "スケジュールの画面", cls="hl"), "",
                    N("自動で実行", "準備できたらメール", [svg("outlook")], cls="ok")])],
                foot="場面が <em>毎週同じことを頼む</em> ならスケジュール、<em>あとで使い回す</em> なら保存")


def f_note():
    return flow("ノートブックと Pages の違い",
                "ノートブックは材料をためる冷蔵庫、Pages は答えに手を入れるまな板",
                [lane("冷蔵庫", "ノートブック", "材料をためる", [
                    N("ファイル・過去のチャット", "参照 / Copilot チャット", [ms("onedrive")]), "足す",
                    N("ノートブック", "名前を付けて作る", [ms("copilot")], cls="hl"), "",
                    N("まとめて聞く", "ためた材料を前提に", cls="ok")]),
                 lane("まな板", "Pages", "答えに手を入れる", [
                    N("Copilot の答え", "チャット画面", [ms("copilot")]), "…",
                    N("Pages で編集", "答えの下のメニュー", cls="hl"), "",
                    N("手を入れて仕上げる", "その場で編集", cls="ok")])])


def f_apps():
    return flow("アプリの中の Copilot は、開いているファイルを材料に動く",
                "チャット画面の Copilot と違い、Word や Excel の Copilot は目の前のファイルに直接書き込む",
                [lane("Word", "Word", "文書を作る", [
                    N("文書を開く", "Word", [svg("word")]), "",
                    N("条件を書いて頼む", "目的・日時・枚数", [ms("copilot")]), "",
                    N("文書に下書きが入る", "", cls="hl"), "",
                    N("完了 / 元に戻す", "取り込むかを決める", cls="ok")]),
                 lane("Excel", "Excel", "表を分析する", [
                    N("表を開く", "Excel", [svg("excel")]), "",
                    N("分析を頼む", "グラフにして など", [ms("copilot")]), "",
                    N("グラフ・表が入る", "", cls="hl"), "",
                    N("パネルで手順を確認", "何をしたか読める", cls="ok")])])


def f_agents():
    return flow("リサーチ ツールとアナリストの違い",
                "どちらもエージェントの一覧から開く。調べてまとめるか、データを分析するか",
                [lane("調べる", "リサーチ ツール", "調べものをまとめる", [
                    N("エージェントの一覧", "Microsoft によるビルド", [ms("agent")]), "",
                    N("何を調査しますか?", "テーマを入れる", [ms("copilot")], cls="hl"), "",
                    N("職場のデータと Web", "を調べる", [svg("outlook"), ms("web")]), "",
                    N("まとめの文書", "", cls="ok")]),
                 lane("分析", "アナリスト", "データを分析する", [
                    N("エージェントの一覧", "Microsoft によるビルド", [ms("agent")]), "",
                    N("ファイルを渡す", "表・データ", [svg("excel")], cls="hl"), "",
                    N("データを分析", "複雑な集計も", [ms("copilot")]), "",
                    N("表・グラフ", "", cls="ok")])])


def f_bridge():
    return flow("試験の勉強が、そのまま実務と人に伝える準備になる",
                "学習ガイドの1行を画面まで結び付けておくと、取得したあとも使い道が続く",
                [lane("流れ", "1行ずつ", "学習ガイドから", [
                    N("学習ガイドの1行", "何ができればよいか", [ms("web")]), "",
                    N("練習問題", "どう問われるか", [ms("web")]), "",
                    N("実画面で押す", "どこを押すか", [ms("copilot")], cls="hl"), "",
                    N("試験", "言い回しが変わっても", cls="ok"), "",
                    N("職場・講座", "画面と手順をそのまま", [svg("teams")], cls="ok")])])


FIGS = {"compare": f_compare, "claude": f_claude, "workiq": f_workiq, "verify": f_verify,
        "prompt": f_prompt, "note": f_note, "apps": f_apps, "agents": f_agents, "bridge": f_bridge}


def render_all():
    out = {}
    out["arch"] = render(arch(), ASSETS / "fig-arch.png", 1000)
    out["arch_sp"] = render_html(arch_sp(), ASSETS / "fig-arch_sp.png", width=736, height=2400)
    out["loop"] = render(loop(), ASSETS / "fig-loop.png", 700)
    out["map"] = render(dmap(), ASSETS / "fig-map.png", 900)
    for k, f in FIGS.items():
        out[k] = render(f(), ASSETS / f"fig-{k}.png", 900)
    return out


if __name__ == "__main__":
    for k, v in render_all().items():
        print("fig", k, v)

# -*- coding: utf-8 -*-
"""PA45 Vol.15 スライド生成（実フロー：トリガー条件→メール送信＋3つの工夫 に沿った版）"""
import io, os

CSS = r"""
  :root{
    --blue-bg:#eaf2fc;--blue-mid:#2a7dd4;--blue-text:#14528f;--blue-light:#b8d3ef;
    --orange:#e06030;--red:#c03520;--surface:#fff;--bg:#f3f6fa;--text:#1f2937;
    --muted:#475569;--hint:#94a3b8;--border:#e2e8f0;--green-bg:#ecfdf5;--green-text:#065f46;
    --yellow-bg:#fffbeb;--yellow-text:#92400e;
  }
  body{margin:0;padding:24px 24px 24px 280px;background:#1a2233;
    font-family:"Meiryo UI","Yu Gothic UI","Segoe UI",sans-serif;color:var(--text);font-size:16px;}
  .deck-header{color:#fff;max-width:1280px;margin:0 auto 24px;font-size:16px;opacity:.85;}
  .deck-header h1{margin:0 0 4px;font-size:24px;}
  .toc{position:fixed;top:0;left:0;bottom:0;width:260px;background:#0f172a;color:#cbd5e1;
    padding:22px 0;overflow-y:auto;z-index:100;border-right:1px solid #1e293b;box-shadow:4px 0 16px rgba(0,0,0,.3);}
  .toc-header{padding:0 22px 14px;border-bottom:1px solid #1e293b;margin-bottom:10px;}
  .toc-header .title{font-size:14px;font-weight:800;color:#fff;}
  .toc-header .sub{font-size:11px;color:#64748b;margin-top:4px;}
  .toc ol{list-style:none;padding:0;margin:0;}
  .toc li a{display:block;padding:9px 22px 9px 18px;color:#cbd5e1;text-decoration:none;font-size:13px;
    line-height:1.45;border-left:3px solid transparent;transition:background .15s,border-color .15s,color .15s;}
  .toc li a:hover{background:#1e293b;color:#fff;}
  .toc li a.active{background:#1e293b;color:#fff;border-left-color:#2a7dd4;}
  .toc li a .n{display:inline-block;width:22px;color:#64748b;font-weight:700;font-size:12px;}
  .toc li a.active .n{color:#2a7dd4;}
  .toc-toggle{position:fixed;top:10px;left:270px;z-index:101;background:#1e293b;color:#fff;border:none;
    padding:8px 14px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600;}
  body.toc-collapsed{padding-left:24px;}
  body.toc-collapsed .toc{transform:translateX(-100%);}
  body.toc-collapsed .toc-toggle{left:10px;}
  .toc,.toc-toggle{transition:transform .2s,left .2s;}
  .slide{width:1280px;height:720px;margin:0 auto 28px;background:#fff;box-shadow:0 12px 40px rgba(0,0,0,.35);
    border-radius:6px;overflow:hidden;position:relative;display:flex;flex-direction:column;}
  .slide-num{position:absolute;top:10px;right:14px;font-size:14px;color:var(--hint);
    background:rgba(255,255,255,.9);padding:3px 10px;border-radius:12px;z-index:10;}
  .slide-head{padding:24px 48px 22px;background:linear-gradient(135deg,#14528f 0%,#2a7dd4 100%);
    color:#fff;border-bottom:4px solid #fbbf24;}
  .slide-eyebrow{font-size:15px;color:#93c5fd;font-weight:700;letter-spacing:.04em;text-transform:uppercase;}
  .slide-title{font-size:38px;font-weight:800;line-height:1.2;margin:4px 0 0;color:#fff;letter-spacing:-.01em;}
  .slide-title small{font-size:23px;color:rgba(255,255,255,.85);font-weight:600;}
  .concept-dot{position:absolute;top:30px;right:60px;display:flex;align-items:center;gap:8px;
    font-size:15px;color:#fbbf24;font-weight:700;}
  .concept-dot::before{content:'';width:10px;height:10px;border-radius:50%;background:#fbbf24;}
  .title-slide .slide-head,.anchor .slide-head{background:transparent;color:inherit;border-bottom:none;}
  .title-slide .slide-eyebrow,.anchor .slide-eyebrow{color:var(--blue-mid);text-transform:none;letter-spacing:0;}
  .anchor .slide-eyebrow{color:#92400e;}
  .title-slide .slide-title,.anchor .slide-title{color:var(--text);}
  .anchor .slide-title{color:#78350f;}
  .title-slide .slide-title small,.anchor .slide-title small{color:var(--muted);}
  .slide-body{flex:1;padding:22px 48px 0;display:flex;flex-direction:column;font-size:18px;}
  .slide-footer{margin-top:auto;padding:14px 48px 18px;display:flex;justify-content:space-between;
    align-items:center;font-size:14px;color:var(--hint);background:#fff;}
  .slide-footer .chat-reminder{background:var(--blue-bg);color:var(--blue-text);padding:7px 16px;
    border-radius:20px;font-weight:600;font-size:14px;}
  .cards-3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:16px;}
  .cards-2{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;margin-top:16px;}
  .card{background:#fff;border:1px solid var(--border);border-radius:14px;padding:20px 22px;box-shadow:0 2px 6px rgba(0,0,0,.04);}
  .card.blue{background:var(--blue-bg);border-color:rgba(42,125,212,.25);}
  .card.green{background:var(--green-bg);border-color:rgba(6,95,70,.25);}
  .card.yellow{background:var(--yellow-bg);border-color:rgba(146,64,14,.25);}
  .card.purple{background:#f5f3ff;border-color:rgba(124,58,237,.25);}
  .card .num{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;
    border-radius:50%;background:var(--blue-mid);color:#fff;font-weight:800;font-size:22px;margin-bottom:12px;}
  .card .ico{font-size:36px;margin-bottom:8px;display:block;}
  .card h3{margin:0 0 10px;font-size:21px;font-weight:700;color:var(--text);line-height:1.35;}
  .card p,.card ul{font-size:16px;line-height:1.7;color:var(--muted);margin:0;}
  .card ul{padding-left:20px;}.card li{margin-bottom:6px;}
  code,.code{font-family:"DM Mono","Consolas",monospace;background:#f1f5f9;padding:3px 9px;border-radius:5px;font-size:.94em;color:#0f172a;}
  .code-block{background:#0f172a;color:#e2e8f0;padding:14px 18px;border-radius:10px;
    font-family:"DM Mono","Consolas",monospace;font-size:16px;line-height:1.6;margin:12px 0;overflow-x:auto;white-space:pre-wrap;word-break:break-all;}
  .code-block .hl{color:#fbbf24;}.code-block .key{color:#7dd3fc;}.code-block .str{color:#86efac;}
  .code-block .br{color:#fca5a5;font-weight:700;}.code-block .cm{color:#64748b;font-size:14px;}
  .title-slide{background:linear-gradient(135deg,#eaf2fc 0%,#d4e6f7 100%);}
  .title-slide .badge-row{display:flex;gap:14px;margin-bottom:20px;}
  .title-slide .pill{background:rgba(255,255,255,.85);color:var(--blue-text);padding:8px 20px;border-radius:22px;font-size:16px;font-weight:700;}
  .title-slide .pill.alt{background:#fff;color:var(--blue-mid);border:2px solid var(--blue-mid);}
  .title-slide h1{font-size:44px;font-weight:800;line-height:1.18;color:var(--blue-text);margin:0 0 20px;letter-spacing:-.02em;}
  .title-slide .lead{font-size:21px;color:var(--muted);margin:0 0 22px;line-height:1.6;}
  .meta-table{background:rgba(255,255,255,.7);border-left:5px solid var(--blue-mid);padding:16px 26px;border-radius:8px;max-width:900px;}
  .meta-table dt{display:inline-block;width:110px;color:var(--blue-mid);font-weight:700;font-size:16px;}
  .meta-table dd{display:inline;margin:0;font-size:18px;color:var(--text);}
  .meta-table dl{margin:9px 0;}
  ul.check{padding:0;list-style:none;}
  ul.check li{padding-left:30px;position:relative;font-size:17px;line-height:1.7;margin-bottom:9px;color:var(--text);}
  ul.check li::before{content:'✓';position:absolute;left:4px;top:0;color:var(--blue-mid);font-weight:800;font-size:19px;}
  ul.cross li::before{content:'✕';color:var(--red);}
  .callout{background:var(--yellow-bg);border-left:6px solid #f59e0b;padding:14px 22px;border-radius:6px;
    font-size:16px;line-height:1.7;color:#78350f;margin:12px 0;}
  .callout strong{color:#78350f;}
  .callout.blue{background:var(--blue-bg);border-left-color:#2a7dd4;color:#14528f;}
  .callout.blue strong{color:#14528f;}
  .anchor{background:linear-gradient(135deg,#fde68a 0%,#fcd34d 100%);}
  .haru-img{width:230px;height:230px;border-radius:50%;object-fit:cover;box-shadow:0 8px 24px rgba(42,125,212,.3);}
  .opening-bar{background:var(--blue-mid);color:#fff;padding:12px 48px;display:flex;justify-content:space-between;font-size:16px;font-weight:700;}
  .pull-quote{font-size:22px;font-weight:700;color:var(--blue-text);text-align:center;background:var(--blue-bg);padding:14px;border-radius:12px;margin:12px 0;}
  .pathpill{display:inline-block;background:#0f172a;color:#fbbf24;font-family:"DM Mono","Consolas",monospace;font-weight:700;padding:4px 12px;border-radius:8px;font-size:16px;}
  .stepflow{display:grid;grid-template-columns:1fr 28px 1fr 28px 1fr;align-items:stretch;gap:6px;margin-top:16px;}
  .stepflow .arr{display:flex;align-items:center;justify-content:center;font-size:26px;color:var(--hint);}
  .stepbox{border-radius:14px;padding:16px;text-align:center;display:flex;flex-direction:column;align-items:center;border:2px solid;}
  .stepbox .badge{font-size:13px;font-weight:800;letter-spacing:.04em;padding:2px 12px;border-radius:12px;margin-bottom:8px;}
  .stepbox h3{margin:0 0 6px;font-size:20px;line-height:1.3;}
  .stepbox p{margin:0;font-size:15px;line-height:1.55;color:var(--muted);}
  .stepbox .act{font-family:"DM Mono","Consolas",monospace;font-size:13px;background:#0f172a;color:#7dd3fc;padding:3px 10px;border-radius:6px;margin-top:8px;}
  .ba{display:grid;grid-template-columns:1fr 40px 1fr;align-items:center;gap:8px;margin-top:14px;}
  .ba .arrow{text-align:center;font-size:28px;color:var(--blue-mid);font-weight:800;}
  .ba .box{border-radius:12px;padding:14px 16px;font-size:15px;line-height:1.6;}
  .ba .bad{background:#fff1f2;border:1px solid #fecdd3;color:#9f1239;}
  .ba .good{background:var(--green-bg);border:1px solid #86efac;color:#065f46;}
  .ba .lab{font-weight:800;font-size:13px;display:block;margin-bottom:4px;}
  .maillink{color:#1d4ed8;text-decoration:underline;font-weight:700;}
  .emailcard{background:#f8fafc;border:1px solid var(--border);border-radius:12px;padding:18px 22px;font-size:16px;line-height:1.9;}
  .emailcard .sub{font-weight:800;color:#0f172a;border-bottom:1px solid var(--border);padding-bottom:8px;margin-bottom:8px;}
  .emailcard .tag{display:inline-block;background:#dbeafe;color:#1e40af;font-size:12px;font-weight:700;padding:1px 8px;border-radius:8px;margin-left:6px;}
  .steplist{counter-reset:s;list-style:none;padding:0;margin:8px 0 0;}
  .steplist li{counter-increment:s;position:relative;padding:8px 0 8px 44px;font-size:17px;line-height:1.55;border-bottom:1px dashed var(--border);}
  .steplist li::before{content:counter(s);position:absolute;left:0;top:6px;width:30px;height:30px;border-radius:50%;
    background:var(--blue-mid);color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center;font-size:15px;}
  .steplist li:last-child{border-bottom:none;}
  .deco{position:absolute;pointer-events:none;z-index:1;}
  .illus{display:block;width:auto;}
  .introrow{display:grid;grid-template-columns:150px 1fr;gap:24px;align-items:center;margin:6px 0 12px;}
  .introrow .illus{max-height:140px;margin:0 auto;}
"""

JS = r"""
  var toc=document.getElementById('toc');
  var toggle=document.getElementById('tocToggle');
  toggle.addEventListener('click',function(){document.body.classList.toggle('toc-collapsed');});
  var links=Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  var slides=links.map(function(a){return document.querySelector(a.getAttribute('href'));});
  function onScroll(){var y=window.scrollY+140;var idx=0;
    for(var i=0;i<slides.length;i++){if(slides[i]&&slides[i].offsetTop<=y)idx=i;}
    links.forEach(function(a){a.classList.remove('active');});
    if(links[idx])links[idx].classList.add('active');}
  window.addEventListener('scroll',onScroll);onScroll();
  var cur=0;
  function go(n){cur=Math.max(0,Math.min(slides.length-1,n));
    if(slides[cur])slides[cur].scrollIntoView({behavior:'smooth'});}
  document.addEventListener('keydown',function(e){
    if(['ArrowRight','PageDown',' '].indexOf(e.key)>=0){e.preventDefault();go(cur+1);}
    else if(['ArrowLeft','PageUp'].indexOf(e.key)>=0){e.preventDefault();go(cur-1);}});
"""

CHAT = '<span class="chat-reminder">💬 学んだこと・気づいたことを #PA45 でリアルタイムに投稿しよう！スクショOK！</span>'
FOOT = f'<div class="slide-footer"><span>Power Automate for Beginners</span>{CHAT}</div>'

# (id, toc_label, extra_class, inner_html_without_footer)
slides = []

def head(eyebrow, title, small="", dot=""):
    s = f'<small>{small}</small>' if small else ''
    d = f'<div class="concept-dot">{dot}</div>' if dot else ''
    return f'<div class="slide-head"><div class="slide-eyebrow">{eyebrow}</div><h1 class="slide-title">{title} {s}</h1>{d}</div>'

# S1 オープニング
slides.append(("s1","20:15 START","title-slide", f'''
  <div class="opening-bar"><span>PA45 — Power Automate 45 ｜ 第15回 / Vol.15</span><span>20:15 START</span></div>
  <div class="slide-body" style="justify-content:center;align-items:center;text-align:center;">
    <div style="font-size:20px;color:var(--blue-mid);font-weight:700;margin-bottom:14px;">まもなく開始します</div>
    <h1 style="font-size:44px;color:var(--blue-text);font-weight:800;line-height:1.25;margin:0 0 18px;">第15回｜共有フォルダ監視 → リンク付き自動メール通知</h1>
    <p style="font-size:21px;color:var(--muted);margin:0;">フォルダに届いたファイルを、担当者へ <strong>クリックできるリンク付き</strong>でお知らせする45分</p>
  </div>
  <div class="slide-footer"><span>Power Automate for Beginners</span><span style="color:var(--hint);">Copyright © PA45</span></div>'''))

# S2 事前準備
slides.append(("s2","事前準備","", head("PA45｜第15回","事前準備","（サインインだけでOK）") + f'''
  <div class="slide-body">
    <div class="introrow">
      <img class="illus" src="assets/irasutoya_robot.png" alt="">
      <p style="font-size:18px;color:var(--muted);margin:0;">今日は <strong>共有フォルダにファイルが届いたら、担当者へリンク付きでメール通知する</strong>フローを、その場で一緒に作ります。手を動かす方は SharePoint のテスト用フォルダがあると◎。見るだけ参加もOKです。</p>
    </div>
    <div class="cards-2">
      <div class="card blue"><div class="num">1</div><h3>Power Automate にサインイン</h3><p><span class="pathpill">make.powerautomate.com</span> を開いて、サインインできる状態に。</p></div>
      <div class="card green"><div class="num">2</div><h3>テスト用の SharePoint フォルダ <span style="font-size:14px;color:var(--muted);">（任意）</span></h3><p>ドキュメント内に <strong>「見積書」フォルダ</strong>を作ると、その場で動かせます。無くても画面を一緒に見ればOK。</p></div>
    </div>
    <div class="callout blue" style="margin-top:14px;"><strong>📥 今日のゴール：</strong> 見積書フォルダにPDFを置く → 担当者に <strong>「ファイル名・日本時間・クリックできるリンク」付き</strong>のメールが自動で飛ぶ仕組みを作る。</div>
  </div>''' + FOOT))

# S3 PA45とは
slides.append(("s3","PA45とは？","", head("INTRODUCTION","PA45 とは？","",'Concept') + f'''
  <div class="slide-body">
    <div style="text-align:center;color:var(--blue-text);font-weight:800;">忙しい人のための 45分ハンズオン</div>
    <div class="cards-3">
      <div class="card blue"><div class="ico">⏱️</div><h3>45分完結</h3><p>長時間の研修は不要。要点だけを凝縮して最短でスキル習得。</p></div>
      <div class="card green"><div class="ico">💻</div><h3>実践型ハンズオン</h3><p>座学だけではありません。その場で手を動かし「使える」技術を学びます。</p></div>
      <div class="card yellow"><div class="ico">👥</div><h3>一緒に作る</h3><p>ゼロから一緒に作ることで仕組みを理解します。</p></div>
    </div>
    <div style="text-align:center;color:var(--green-text);font-weight:700;margin-top:auto;padding:14px;background:var(--green-bg);border-radius:10px;">✓ Power Automate 未経験・知識ゼロでも大丈夫！</div>
  </div>''' + FOOT))

# S4 講師自己紹介
slides.append(("s4","講師自己紹介（Haru）","", head("SPEAKER","Power Automate 45 (PA45)","",'Speaker') + f'''
  <div class="slide-body">
    <div style="display:grid;grid-template-columns:230px 1fr;gap:30px;align-items:center;">
      <img class="haru-img" src="https://www.automate136.com/wp-content/uploads/2026/04/haru-profile.png" alt="Haru">
      <div>
        <div style="font-size:26px;font-weight:800;color:var(--blue-text);">Haru</div>
        <div style="color:var(--muted);margin:2px 0 14px;">💻 Power Platform / DX 推進</div>
        <ul class="check" style="font-size:18px;">
          <li>🏢 社内で PA／Copilot ハンズオン講座を開催し、DXを推進</li>
          <li>🎤 広島コミュニティ「PLUG」運営・外部コミュニティ登壇</li>
          <li>📱 X で初心者向け Power Automate チップスを継続発信</li>
          <li>🕐 PA45（45分の "1粒ハンズオン"）を毎週開催・運営</li>
        </ul>
      </div>
    </div>
    <div class="pull-quote" style="margin-top:auto;">今日も一緒に「できた！」を作っていきましょう 😊</div>
  </div>''' + FOOT))

# S5 ご参加にあたって
slides.append(("s5","ご参加にあたって","", head("PA45 Online Course","ご参加にあたってのお願い","（ルール）",'Guidelines') + f'''
  <div class="slide-body">
    <div class="cards-3">
      <div class="card blue"><div class="ico">🤝</div><h3>気持ちよく学ぶ</h3><ul><li>誹謗中傷・不適切な発言は禁止</li><li>お互いを尊重し合いましょう</li></ul></div>
      <div class="card green"><div class="ico">🎥</div><h3>録画について</h3><ul><li>後日 YouTube 公開予定</li><li>匿名参加で表示名を隠せます</li></ul></div>
      <div class="card yellow"><div class="ico">💬</div><h3>チャットは気軽に</h3><ul><li>「できました！」大歓迎</li><li>小さな質問でもOK</li></ul></div>
    </div>
    <div class="cards-2" style="margin-top:14px;">
      <div class="card"><h3 style="color:var(--blue-text);">🖌️ アウトプットで定着</h3><p><strong>#PA45</strong> をつけて投稿しよう！「気づき」「これ便利！」何でもOK。</p></div>
      <div class="card"><h3 style="color:var(--green-text);">🎓 初心者大歓迎</h3><p>🚫 難しい専門用語は使いません／🚶 置いてけぼりにしないようゆっくり進行。</p></div>
    </div>
  </div>''' + FOOT))

# S6 タイトル
slides.append(("s6","第15回タイトル","title-slide", head("Power Automate 入門講座","Vol.15") + f'''
  <div class="slide-body">
    <div class="badge-row"><span class="pill">SharePoint</span><span class="pill alt">ファイル作成トリガー</span><span class="pill alt">トリガー条件</span><span class="pill alt">クリックできるリンク</span></div>
    <h1>第15回：「更新、気づかなかった…」を もう繰り返さない<br>共有フォルダにファイルが届いたら、担当者へリンク付きで自動メール</h1>
    <div class="meta-table">
      <dl><dt>Theme</dt><dd>SharePoint監視 → <strong>トリガー条件で絞る</strong> → リンク付き自動メール</dd></dl>
      <dl><dt>Target</dt><dd>資料の更新に気づくのが遅れがちな方／連絡漏れをなくしたい方（知識ゼロOK）</dd></dl>
      <dl><dt>Time</dt><dd>解説＋その場で一緒に作る 約45分</dd></dl>
    </div>
    <img class="deco" src="assets/irasutoya_programming.png" alt="" style="right:46px;bottom:34px;height:190px;">
  </div>''' + FOOT))

# S7 今日やること
slides.append(("s7","今日やること（3つ）","", head("PA45｜第15回","今日やること","（3つだけ）",'Agenda') + f'''
  <div class="slide-body">
    <div class="cards-3">
      <div class="card blue"><div class="num">1</div><div class="ico">📥</div><h3>フォルダを見張る</h3><p>「ファイルが作成されたとき」で共有フォルダを自動で監視。</p></div>
      <div class="card purple"><div class="num">2</div><div class="ico">🎯</div><h3>対象だけに絞る</h3><p><strong>トリガー条件</strong>で「見積書フォルダだけ」起動。ムダな実行を防ぐ。</p></div>
      <div class="card green"><div class="num">3</div><div class="ico">🔗</div><h3>リンク付きで知らせる</h3><p>「メールの送信(V2)」で <strong>クリックできるリンク</strong>付きの通知を送る。</p></div>
    </div>
    <div class="callout" style="margin-top:auto;"><strong>🎯 ゴール：</strong> 見積書フォルダにPDFを置く → 数十秒後に担当者へ、ファイル名・日本時間・<strong>青いリンク</strong>付きメールが自動で飛ぶ。</div>
  </div>''' + FOOT))

# S8 困りごと
slides.append(("s8","こんな困りごと","", head("PA45｜第15回 ／ はじめに","こんな困りごと、ありませんか？","── 共有フォルダ あるある",'Why') + f'''
  <div class="slide-body">
    <div class="introrow">
      <img class="illus" src="assets/irasutoya_search.png" alt="">
      <p style="margin:0;color:var(--muted);">共有フォルダに資料を入れてもらったのに、気づいたのは数日後…。「アップしました」の一言を待って、何度もフォルダを開いて確認。その手間、まるごと無くせます。</p>
    </div>
    <div class="cards-3">
      <div class="card"><h3 style="color:#991b1b;">気づくのが遅れる</h3><p>通知がないので「いつ更新された？」と何度もフォルダを開いてしまう。</p></div>
      <div class="card"><h3 style="color:#92400e;">連絡が属人的</h3><p>「入れたら連絡してね」が抜ける。連絡する側・される側、どちらの手間にも。</p></div>
      <div class="card green"><h3 style="color:#15803d;">だから自動化</h3><p>「届いたら自動で通知」。しかも<strong>リンクから即開ける</strong>。今日それを作ります。</p></div>
    </div>
    <div class="callout blue" style="margin-top:auto;"><strong>🎯 今日のゴール：</strong> 「更新、気づかなかった…」を仕組みでゼロに。45分で動くフローまで持って帰りましょう。</div>
  </div>''' + FOOT))

# S9 全体像
slides.append(("s9","今日作るフロー（全体像）","", head("PA45｜第15回","今日作るフロー","── 3ステップの全体像",'Overview') + f'''
  <div class="slide-body">
    <div class="stepflow">
      <div class="stepbox" style="border-color:#2a7dd4;background:var(--blue-bg);">
        <span class="badge" style="background:#2a7dd4;color:#fff;">TRIGGER</span>
        <h3>① ファイルが<br>作成されたとき</h3><p>SharePointの共有フォルダを自動で監視。</p><span class="act">SharePoint</span></div>
      <div class="arr">▶</div>
      <div class="stepbox" style="border-color:#7c3aed;background:#f5f3ff;">
        <span class="badge" style="background:#7c3aed;color:#fff;">条件</span>
        <h3>② トリガー条件<br>で絞る</h3><p>「見積書フォルダだけ」起動。条件アクション不要。</p><span class="act">設定 → トリガーの条件</span></div>
      <div class="arr">▶</div>
      <div class="stepbox" style="border-color:#15803d;background:var(--green-bg);">
        <span class="badge" style="background:#15803d;color:#fff;">ACTION</span>
        <h3>③ メールの<br>送信(V2)</h3><p>ファイル名・日本時間・<strong>リンク</strong>付きで通知。</p><span class="act">Office 365 Outlook</span></div>
    </div>
    <div class="cards-2" style="margin-top:18px;">
      <div class="card purple"><h3 style="font-size:19px;">💡 今日の山場①：トリガー条件</h3><p>「条件」アクションは動いてから捨てる。<strong>トリガー条件はそもそも起動しない</strong>＝実行回数を節約できる中級ワザ。</p></div>
      <div class="card green"><h3 style="font-size:19px;">💡 今日の山場②：メールにひと工夫</h3><p>本文に<strong>3つの工夫</strong>（ファイル名／日本時間／<strong>クリックできるリンク</strong>）を入れて、実務で使えるメールにします。</p></div>
    </div>
  </div>''' + FOOT))

# S10 STEP1 トリガー
slides.append(("s10","STEP① トリガー","", head("STEP ① TRIGGER","ファイルが作成されたとき","（SharePoint・プロパティのみ）",'SharePoint') + f'''
  <div class="slide-body">
    <div class="cards-2">
      <div class="card"><h3>設定するのはこれだけ</h3>
        <ul class="check" style="font-size:17px;">
          <li><strong>サイトのアドレス</strong>：対象の SharePoint サイトを選ぶ</li>
          <li><strong>ライブラリ名</strong>：ドキュメント など</li>
        </ul>
        <p style="margin-top:8px;">フォルダーは指定せず<strong>ライブラリ全体</strong>を監視 → 絞り込みは次の「トリガー条件」で行います。</p>
      </div>
      <div class="card blue"><h3>🔑 ポイント</h3>
        <p>「<strong>プロパティのみ</strong>」は軽くて速い版。ファイルの中身ではなく情報だけを受け取ります。<br><br>「変更されたとき」ではなく <strong>「作成されたとき」</strong>を選ぶと、新規ファイルだけに反応します。</p>
      </div>
    </div>
    <div class="callout" style="margin-top:auto;"><strong>ここで取れる値（次のステップで使います）：</strong> ファイル名 ／ フォルダーのパス ／ 作成日時 ／ <strong>リンク</strong>。</div>
  </div>''' + FOOT))

# S11 STEP2 トリガー条件（山場①）
slides.append(("s11","STEP② トリガー条件で絞る","", head("STEP ② CONDITION ★","トリガー条件で絞る","── 見積書フォルダだけ起動",'Trigger Condition') + f'''
  <div class="slide-body">
    <div class="cards-2">
      <div class="card"><h3>なぜ「条件アクション」じゃないの？</h3>
        <p>「条件」アクションは<strong>一度フローが動いてから</strong>対象外を捨てます。対して<strong>トリガー条件</strong>は、対象外なら<strong>そもそもフローを起動しない</strong>。<br><br>＝ ムダな実行回数を減らせる、ちょっと上級の絞り込みワザ。</p>
      </div>
      <div class="card purple"><h3>設定場所</h3>
        <p>トリガーの <strong>… → 設定 → 「トリガーの条件」</strong> に、次の式を1つ追加するだけ：</p>
        <div class="code-block"><span class="hl">@</span>contains(triggerOutputs()?[<span class="str">'body/{{Path}}'</span>],<span class="str">'見積書'</span>)</div>
        <p style="font-size:14px;">＝ ファイルのパスに「見積書」を含むときだけ起動。</p>
      </div>
    </div>
    <div class="callout blue" style="margin-top:auto;"><strong>効果：</strong> 「見積書」フォルダに置いたファイルだけがフローを動かす。他のフォルダのファイルでは通知が飛びません。<span style="color:var(--muted);">（パスの綴りは実機のフォルダ名に合わせてね）</span></div>
  </div>''' + FOOT))

# S12 STEP3 メール送信＋3つの工夫
slides.append(("s12","STEP③ メール送信(V2)","", head("STEP ③ ACTION","メールの送信(V2)","── 担当者へお知らせ",'Outlook') + f'''
  <div class="slide-body">
    <div class="cards-2">
      <div class="card"><h3>まず3つを入れる</h3>
        <ul class="check" style="font-size:17px;">
          <li><strong>宛先</strong>：担当者のメールアドレス</li>
          <li><strong>件名</strong>：【新着】共有フォルダーにファイルが届きました</li>
          <li><strong>本文</strong>：あいさつ ＋ これから入れる3つの工夫</li>
        </ul>
      </div>
      <div class="card green"><h3>本文の3つの工夫 ✨</h3>
        <ul class="check" style="font-size:17px;">
          <li>① <strong>ファイル名</strong>を差し込む（動的コンテンツ）</li>
          <li>② <strong>作成日時を日本時間</strong>に（convertTimeZone）</li>
          <li>③ <strong>クリックできるリンク</strong>（今日の山場）</li>
        </ul>
      </div>
    </div>
    <div class="callout" style="margin-top:auto;"><strong>このあと：</strong> ①②を次のスライドで、③（リンク）はそのあとの<strong>「今日の山場」</strong>でじっくり作ります。</div>
  </div>''' + FOOT))

# S13 工夫①②
slides.append(("s13","工夫①② ファイル名・日本時間","", head("本文の工夫 ①②","ファイル名 ＆ 日本時間","── まずはこの2つ",'Dynamic & Expression') + f'''
  <div class="slide-body">
    <div class="cards-2">
      <div class="card blue"><h3>① ファイル名を差し込む</h3>
        <p>本文の「ファイル名：」の後ろにカーソル → 半角 <span class="code">/</span> →「動的コンテンツを挿入する」→ <strong>「拡張子付きのファイル名」</strong>を選ぶ。</p>
        <p style="font-size:14px;color:var(--muted);">※「タイトル」だと空になりがち。<strong>拡張子付きのファイル名</strong>を選ぶのがコツ。</p>
      </div>
      <div class="card green"><h3>② 作成日時を日本時間に</h3>
        <p>既定の作成日時は <strong>UTC（世界標準時）</strong>。そのままだと <strong>9時間ズレ</strong>て見えます。<span class="code">convertTimeZone</span> で日本時間＋好きな書式に。</p>
        <div class="code-block"><span class="key">convertTimeZone</span>(&lt;作成日時&gt;,<span class="str">'UTC'</span>,<span class="str">'Tokyo Standard Time'</span>,<span class="str">'yyyy/MM/dd HH:mm'</span>)</div>
      </div>
    </div>
    <div class="ba">
      <div class="box bad"><span class="lab">Before（UTCのまま）</span>2026-06-18T08:03:00<strong>Z</strong></div>
      <div class="arrow">→</div>
      <div class="box good"><span class="lab">After（日本時間）</span>2026/06/18 17:03</div>
    </div>
  </div>''' + FOOT))

# S14 工夫③ リンク（山場）
slides.append(("s14","★ クリックできるリンクの作り方","", head("本文の工夫 ③ ★★ 今日の山場","クリックできるリンクの作り方","── 生URLを青リンクに",'Hyperlink') + f'''
  <div class="slide-body">
    <div class="cards-2" style="margin-top:8px;">
      <div class="card"><h3>なぜ生URLじゃダメ？</h3>
        <p>動的コンテンツ「リンク」をそのまま入れると、長いURLが表示されるだけで<strong>クリックできません</strong>。これを「ここを開く」という<strong>青いリンク</strong>にします。</p>
        <h3 style="margin-top:12px;font-size:19px;">仕組み（HTMLの &lt;a&gt; タグ）</h3>
        <div class="code-block">&lt;a href=<span class="str">"行き先のURL"</span>&gt;<span class="hl">見せる文字</span>&lt;/a&gt;
<span class="cm">  href＝ジャンプ先 ／ 文字＝ボタンの名前</span></div>
      </div>
      <div class="card green"><h3>作り方（4ステップ）</h3>
        <ol class="steplist">
          <li>本文ツールバー右端の <span class="code">&lt;/&gt;</span>（コードビュー）を押す</li>
          <li>半角で <span class="code">&lt;a href="</span> と打つ</li>
          <li>半角 <span class="code">/</span> →「動的コンテンツ」→ <strong>「リンク」</strong>を選ぶ（href の中に入る）</li>
          <li><span class="code">"&gt;ここを開く&lt;/a&gt;</span> と打つ → <span class="code">&lt;/&gt;</span> で戻す</li>
        </ol>
      </div>
    </div>
    <div class="ba">
      <div class="box bad"><span class="lab">Before</span>https://…%E8%A6%8B%E7%A9%8D…/見積書.pdf</div>
      <div class="arrow">→</div>
      <div class="box good"><span class="lab">After</span><span class="maillink">ここを開く</span> ← クリックでファイルが開く！</div>
    </div>
  </div>''' + FOOT))

# S15 いっしょに作ろう
slides.append(("s15","★ いっしょに作ろう（手順）","", head("★ HANDS-ON","いっしょに作ろう","── クリック手順の通し","Let's build") + f'''
  <div class="slide-body">
    <div class="cards-2">
      <div class="card"><ul class="check" style="font-size:16px;">
        <li><strong>①</strong> 新規 → 自動化したクラウドフロー</li>
        <li><strong>②</strong> トリガー「ファイルが作成されたとき(プロパティのみ)」</li>
        <li><strong>③</strong> サイト・ライブラリを指定</li>
        <li><strong>④</strong> 設定 →「トリガーの条件」に <span class="code">@contains(…'見積書')</span></li>
      </ul></div>
      <div class="card"><ul class="check" style="font-size:16px;">
        <li><strong>⑤</strong> 「メールの送信(V2)」を追加（宛先・件名）</li>
        <li><strong>⑥</strong> 本文に ファイル名 ／ 日本時間(式) を差し込む</li>
        <li><strong>⑦</strong> <span class="code">&lt;/&gt;</span> でリンクを <span class="code">&lt;a href&gt;</span> 化</li>
        <li><strong>⑧</strong> 保存 → 見積書フォルダにPDFを置いてテスト🎉</li>
      </ul></div>
    </div>
    <div class="callout" style="margin-top:auto;"><strong>⚠️ つまずきポイント：</strong> ①通知が来ない→トリガー条件のフォルダ名（綴り）を確認。②リンクが空→「リンク」動的コンテンツを選べているか。③日時が変→convertTimeZone の項目名を確認。</div>
  </div>''' + FOOT))

# S16 完成イメージ
slides.append(("s16","完成イメージ（届くメール）","", head("PA45｜第15回","完成イメージ","── 届くメールはこうなる",'Result') + f'''
  <div class="slide-body">
    <div style="display:grid;grid-template-columns:1fr 170px;gap:22px;align-items:center;">
      <div class="emailcard">
        <div class="sub">件名：【新着】共有フォルダーにファイルが届きました <span class="tag">自動送信</span></div>
        お疲れさまです。共有フォルダーに新しいファイルが届きました。<br>
        ファイル名：<strong>見積書_サンプル.pdf</strong><br>
        作成日時（日本時間）：<strong>2026/06/18 17:03</strong><br>
        ファイルを開く：<span class="maillink">ここを開く</span><br>
        ご確認をお願いいたします。
      </div>
      <img class="illus" src="assets/irasutoya_email.png" alt="" style="max-height:180px;margin:0 auto;">
    </div>
    <div class="cards-3" style="margin-top:16px;">
      <div class="card blue"><h3 style="font-size:18px;">① ファイル名</h3><p>何が届いたか一目で分かる。</p></div>
      <div class="card green"><h3 style="font-size:18px;">② 日本時間</h3><p>UTCのズレなし。そのまま読める。</p></div>
      <div class="card yellow"><h3 style="font-size:18px;">③ クリックリンク</h3><p>探さず1クリックで開ける。</p></div>
    </div>
  </div>''' + FOOT))

# S17 活用例
slides.append(("s17","実務での活用例","", head("PA45｜第15回","実務での活用例","── このフロー、こう使える",'Use cases') + f'''
  <div class="slide-body">
    <div class="cards-3">
      <div class="card blue"><div class="ico">📑</div><h3 style="font-size:20px;">提出物の受領通知</h3><p>取引先や他部署が資料を入れたら、担当者へ自動連絡。確認漏れを防ぐ。</p></div>
      <div class="card green"><div class="ico">🧾</div><h3 style="font-size:20px;">納品・見積の到着</h3><p>見積書・納品書フォルダを監視。届いた瞬間に経理・営業へお知らせ。</p></div>
      <div class="card yellow"><div class="ico">👥</div><h3 style="font-size:20px;">チームへ共有</h3><p>宛先を複数にすれば、関係メンバー全員に一斉通知。連絡係いらず。</p></div>
    </div>
    <div class="cards-2" style="margin-top:16px;">
      <div class="card"><h3 style="font-size:19px;">🔁 ちょい足しアイデア</h3><p>メールの代わりに <strong>Teams 通知</strong>にしたり、<strong>承認フロー</strong>（第8回）につなげたり。今日の3ステップが土台になります。</p></div>
      <div class="card blue"><h3 style="font-size:19px;">🌱 シリーズのつながり</h3><p>第7回・第9回と同じ "きっかけ→処理→通知" の形。今日は<strong>トリガー条件</strong>と<strong>リンク</strong>の引き出しが増えました。</p></div>
    </div>
  </div>''' + FOOT))

# S18 クロージング
slides.append(("s18","クロージング＆アンケート","anchor", f'''
  <div class="slide-head"><div class="slide-eyebrow">Thank you!</div><h1 class="slide-title">おつかれさまでした！ <small>── アンケートのお願い</small></h1></div>
  <div class="slide-body">
    <div class="pull-quote" style="background:rgba(255,255,255,.6);">📥 共有フォルダ監視 → リンク付き自動メール ── 今日であなたのものになりました！</div>
    <div class="cards-2" style="margin-top:8px;">
      <div class="card"><h3>📝 アンケートにご協力ください</h3><p>2分で終わります。いただいた声が次回に直結します。回答者には<strong>参加バッジ</strong>をお送りします🏅</p></div>
      <div class="card blue"><h3>📚 復習・次回</h3><p>🌐 受講生サイト：<span class="code">haru-powerplatform.github.io/pa45/</span><br>📅 次回もぜひ：<span class="code">powerautomate-create.connpass.com</span></p></div>
    </div>
    <div style="text-align:center;font-size:20px;color:#78350f;font-weight:700;margin-top:auto;">また次回、一緒に「できた！」を作りましょう 😊</div>
  </div>
  <img class="deco" src="assets/irasutoya_businessman.png" alt="" style="left:34px;bottom:24px;height:150px;">
  <div class="slide-footer"><span>Power Automate for Beginners</span>{CHAT}</div>'''))

# ---- アセンブル ----
total = len(slides)
toc_items = "\n".join(
    f'    <li><a href="#{sid}"><span class="n">{i+1:02d}</span>{label}</a></li>'
    for i,(sid,label,_,_) in enumerate(slides))

sections = []
for i,(sid,label,extra,inner) in enumerate(slides):
    cls = "slide" + (f" {extra}" if extra else "")
    num = f'<span class="slide-num">{i+1} / {total}</span>'
    sections.append(f'<!-- ===== S{i+1}: {label} ===== -->\n<section class="{cls}" id="{sid}">\n  {num}\n  {inner}\n</section>')

html = f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>PA45 第15回 スライド｜共有フォルダ監視→リンク付き自動メール通知</title>
<style>{CSS}</style>
</head>
<body>
<nav class="toc" id="toc">
  <div class="toc-header">
    <div class="title">📑 目次 — PA45 第15回</div>
    <div class="sub">クリックでジャンプ</div>
  </div>
  <ol>
{toc_items}
  </ol>
</nav>
<button class="toc-toggle" id="tocToggle" type="button">≡ 目次</button>

<div class="deck-header">
  <h1>PA45 第15回 スライド</h1>
  <div>2026-06-18（木）20:15〜 ／ 共有フォルダ監視 → トリガー条件で絞る → リンク付き自動メール通知</div>
</div>

{chr(10).join(sections)}

<script>
{JS}
</script>
</body>
</html>
'''

OUT = os.path.join(os.path.dirname(__file__), "index.html")
with io.open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("OK:", OUT, "/ slides:", total)

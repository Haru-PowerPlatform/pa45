# -*- coding: utf-8 -*-
# Build slides/index.html : XスライドVol順ギャラリー(目次+検索)
# 情報源 = assets/x/html/vol-*/index.html の<title>(実Vol番号) + 旧チップ Vol.1-30
# 新しいVolを作ったら: python scripts/build-slides-gallery.py で再生成
TEMPLATE = r"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="PA45がXで投稿しているPower Automate / Copilot Studioの技術チップスVol.1〜95をVol順に一覧。目次と検索で目的の回にすぐたどり着けます。スライド画像はそのまま大きく表示。">
  <title>Xスライド一覧（Vol順・目次つき）｜PA45 Power Automate 技術チップス</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../assets/css/style.css?v=20260718">
  <style>
    /* ===== 検索バー ===== */
    .x-toolbar { position: sticky; top: 0; z-index: 40; background: var(--c-bg); padding: 12px 0 10px; margin-bottom: 6px; border-bottom: 1px solid var(--c-border-md); }
    .x-searchwrap { position: relative; }
    .x-search {
      width: 100%; box-sizing: border-box; font-size: 15px; font-family: var(--font-base);
      padding: 12px 40px 12px 42px; border-radius: 12px; border: 1px solid var(--c-border-md);
      background: var(--c-surface); color: var(--c-text);
    }
    .x-search:focus { outline: none; border-color: var(--c-blue-mid); box-shadow: 0 0 0 3px var(--c-blue-bg); }
    .x-search-ico { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--c-hint); pointer-events: none; }
    .x-clear { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; font-size: 20px; color: var(--c-hint); cursor: pointer; display: none; }
    .x-count { font-size: 12px; color: var(--c-muted); margin: 8px 2px 0; font-family: var(--font-mono); }

    /* ===== 目次 ===== */
    .toc { margin: 14px 0 26px; border: 1px solid var(--c-border-md); border-radius: var(--radius-lg); background: var(--c-surface); overflow: hidden; }
    .toc summary { cursor: pointer; padding: 13px 16px; font-weight: 700; font-size: 14px; list-style: none; display: flex; align-items: center; gap: 8px; }
    .toc summary::-webkit-details-marker { display: none; }
    .toc summary .chev { transition: transform .2s; color: var(--c-hint); }
    .toc[open] summary .chev { transform: rotate(90deg); }
    .toc-list { display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 2px 10px; padding: 4px 16px 16px; }
    .toc-item { display: flex; gap: 8px; align-items: baseline; padding: 5px 4px; border-radius: 6px; text-decoration: none; color: var(--c-text); font-size: 12.5px; line-height: 1.4; }
    .toc-item:hover { background: var(--c-blue-bg); }
    .toc-vol { font-family: var(--font-mono); font-weight: 500; font-size: 11px; color: var(--c-blue-text); min-width: 26px; text-align: right; flex-shrink: 0; }
    .toc-ttl { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .toc-item.hidden { display: none; }
    @media (max-width: 900px) { .toc-list { grid-template-columns: repeat(2, minmax(0,1fr)); } }
    @media (max-width: 560px) { .toc-list { grid-template-columns: 1fr; } }

    /* ===== ギャラリー ===== */
    .x-grid { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 18px; }
    .x-card {
      margin: 0; background: var(--c-surface); border-radius: var(--radius-lg);
      overflow: hidden; box-shadow: var(--shadow-card); cursor: zoom-in;
      transition: box-shadow .2s, transform .2s; outline: none; scroll-margin-top: 90px;
    }
    .x-card:hover, .x-card:focus-visible { box-shadow: var(--shadow-hover); transform: translateY(-2px); }
    .x-card:focus-visible { box-shadow: 0 0 0 3px var(--c-blue-mid); }
    .x-card.flash { animation: flash 1.4s ease; }
    @keyframes flash { 0%,100% { box-shadow: var(--shadow-card); } 25% { box-shadow: 0 0 0 3px var(--c-blue-mid); } }
    .x-shot { aspect-ratio: 16 / 9; background: var(--c-blue-bg); }
    .x-shot img { width: 100%; height: 100%; object-fit: cover; display: block; }
    .x-cap { display: flex; align-items: baseline; gap: 8px; padding: 10px 14px; }
    .x-vol { font-family: var(--font-mono); font-weight: 500; font-size: 12px; color: var(--c-blue-text); background: var(--c-blue-bg); padding: 2px 8px; border-radius: 5px; flex-shrink: 0; }
    .x-ttl { font-size: 13px; font-weight: 500; line-height: 1.45; color: var(--c-text); }
    .x-card.hidden { display: none; }
    .x-empty { display: none; text-align: center; color: var(--c-muted); padding: 40px 0; font-size: 14px; }

    /* ===== ライトボックス ===== */
    .lb { position: fixed; inset: 0; z-index: 999; background: rgba(12,20,32,.92); display: none; align-items: center; justify-content: center; padding: 24px; }
    .lb.open { display: flex; }
    .lb-img { max-width: min(1200px, 94vw); max-height: 78vh; width: auto; border-radius: 10px; box-shadow: 0 20px 60px rgba(0,0,0,.5); }
    .lb-cap { position: absolute; bottom: 18px; left: 50%; transform: translateX(-50%); color: #fff; font-size: 14px; text-align: center; max-width: 90vw; line-height: 1.5; }
    .lb-cap b { color: #9ecbff; font-family: var(--font-mono); margin-right: 8px; }
    .lb-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(255,255,255,.14); color: #fff; border: none; width: 52px; height: 52px; border-radius: 50%; font-size: 26px; cursor: pointer; transition: background .15s; }
    .lb-btn:hover { background: rgba(255,255,255,.28); }
    .lb-prev { left: 18px; } .lb-next { right: 18px; }
    .lb-close { position: absolute; top: 16px; right: 20px; background: none; border: none; color: #fff; font-size: 34px; cursor: pointer; line-height: 1; }
    @media (max-width: 720px) {
      .x-grid { grid-template-columns: 1fr; gap: 14px; }
      .lb-btn { width: 42px; height: 42px; font-size: 22px; }
      .lb-prev { left: 6px; } .lb-next { right: 6px; }
    }
  </style>

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="PA45 — Power Automate 45">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:url" content="https://haru-powerplatform.github.io/pa45/slides/">
  <meta property="og:title" content="Xスライド一覧（Vol順・目次つき）— Power Automate 技術チップス">
  <meta property="og:description" content="Xで投稿しているPower Automate / Copilot Studioの技術チップスVol.1〜95をVol順に一覧。目次と検索ですぐ見つかります。">
  <meta property="og:image" content="https://haru-powerplatform.github.io/pa45/assets/ogp/og-slides.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@isamu_Automate">
  <meta name="twitter:title" content="Xスライド一覧（Vol順・目次つき）— Power Automate 技術チップス">
  <meta name="twitter:description" content="Xで投稿しているPower Automate / Copilot Studioの技術チップスVol.1〜95をVol順に一覧。目次と検索ですぐ見つかります。">
  <meta name="twitter:image" content="https://haru-powerplatform.github.io/pa45/assets/ogp/og-slides.png">
  <link rel="canonical" href="https://haru-powerplatform.github.io/pa45/slides/">
</head>
<body>

<header class="site-header">
  <div class="container header-inner">
    <a href="../" class="site-logo">PA45<span>Power Automate 45</span></a>
    <nav class="header-nav">
      <a href="../sessions/">参加する</a>
      <a href="../sessions/#archive">講座アーカイブ</a>
      <a href="../videos/">動画</a>
      <a href="../achievements/">活動</a>
      <a href="../achievements/survey.html">アンケート</a>
      <a href="../about/">About</a>
    </nav>
    <a href="../sessions/" class="header-cta">次回PA45に参加する →</a>
    <button class="hamburger" aria-label="メニュー" onclick="toggleMenu()"><span></span><span></span><span></span></button>
  </div>
  <nav class="mobile-nav" id="mobileNav">
    <a href="../sessions/">参加する（Sessions）</a>
    <a href="../sessions/#archive">講座アーカイブ（Archive）</a>
    <a href="../videos/">動画（Videos）</a>
    <a href="../achievements/">活動（Activity）</a>
    <a href="../method/">PA45とは（Method）</a>
    <a href="../about/">About</a>
    <a href="../sessions/" style="color:#0b3e72;font-weight:600;margin-top:4px;">→ 次回PA45に参加する</a>
  </nav>
</header>

<section class="page-hero">
  <div class="container">
    <span class="page-hero-eyebrow">X Slides</span>
    <h1 class="page-hero-h1">Xのスライド投稿を、Vol順に全部</h1>
    <p class="page-hero-sub">Xで投稿しているPower Automate / Copilot Studioの技術チップスをVol順に並べました。<br>目次と検索で目的の回にすぐたどり着けます。カードをクリックすると拡大して、パラパラと見比べられます。</p>
  </div>
</section>

<section class="section" style="padding-bottom:0;">
  <div class="container">
    <a href="../sessions/" style="display:flex;align-items:center;gap:16px;text-decoration:none;background:linear-gradient(135deg,#14528f,#2a7dd4);color:#fff;border-radius:14px;padding:18px 22px;box-shadow:0 6px 18px rgba(20,82,143,.25);">
      <svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><rect x="3" y="4" width="18" height="13" rx="2"/><line x1="8" y1="20" x2="16" y2="20"/><line x1="12" y1="17" x2="12" y2="20"/></svg>
      <div style="flex:1;min-width:0;">
        <div style="font-size:12px;letter-spacing:.06em;opacity:.85;font-weight:700;">📚 各回の講座スライド（復習用）はこちら</div>
        <div style="font-size:17px;font-weight:700;margin-top:3px;line-height:1.4;">第1〜23回の解説スライド・サンプルフロー・アンケート結果をまとめています</div>
      </div>
      <div style="flex-shrink:0;font-weight:700;background:rgba(255,255,255,.18);padding:9px 18px;border-radius:24px;white-space:nowrap;">Sessionsで見る →</div>
    </a>
  </div>
</section>

<section class="section">
  <div class="container">

    <div class="x-toolbar">
      <div class="x-searchwrap">
        <svg class="x-search-ico" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input type="search" class="x-search" id="xSearch" placeholder="Vol番号やキーワードで検索（例：Teams、JSON、会議、Vol.85）" autocomplete="off" aria-label="スライドを検索">
        <button class="x-clear" id="xClear" aria-label="クリア">×</button>
      </div>
      <div class="x-count" id="xCount"></div>
    </div>

    <details class="toc" id="toc">
      <summary><svg class="chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 6 15 12 9 18"/></svg>目次（全__COUNT__本）— タップで開閉</summary>
      <div class="toc-list" id="tocList">
__TOC__
      </div>
    </details>

    <div class="x-grid" id="slidesGrid">
__CARDS__
    </div>
    <p class="x-empty" id="xEmpty">該当するスライドが見つかりませんでした。別のキーワードでお試しください。</p>

    <div class="cta-bar">
      <p>スライドを見て興味が出たら、次回セッションで実際に手を動かしてみませんか</p>
      <a href="../sessions/" class="btn-small">次回セッションを確認 →</a>
    </div>
  </div>
</section>

<div class="lb" id="lb" aria-hidden="true">
  <button class="lb-close" aria-label="閉じる" onclick="lbClose()">×</button>
  <button class="lb-btn lb-prev" aria-label="前へ" onclick="lbStep(-1)">‹</button>
  <img class="lb-img" id="lbImg" src="" alt="">
  <button class="lb-btn lb-next" aria-label="次へ" onclick="lbStep(1)">›</button>
  <div class="lb-cap" id="lbCap"></div>
</div>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <div class="footer-col-title">学ぶ</div>
        <a href="../slides/">Slides（スライド一覧）</a>
        <a href="https://www.automate136.com" target="_blank" rel="noopener">Blog（WordPress）</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">参加する</div>
        <a href="../sessions/">Sessions（次回・過去回）</a>
        <a href="https://powerautomate-create.connpass.com/" target="_blank" rel="noopener">connpass（外部）</a>
      </div>
      <div class="footer-col">
        <div class="footer-col-title">このサイトについて</div>
        <a href="../achievements/">Achievements（活動の記録）</a>
        <a href="../method/">PA45 Method（設計思想）</a>
        <a href="../about/">About（問い合わせ）</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>PA45 — Power Automate 45</span>
      <span>GitHub Pages で公開 · 静的サイト</span>
    </div>
  </div>
</footer>

<script>
function toggleMenu() { document.getElementById('mobileNav').classList.toggle('open'); }
document.addEventListener('click', function(e) {
  const nav = document.getElementById('mobileNav'), btn = document.querySelector('.hamburger');
  if (nav.classList.contains('open') && !nav.contains(e.target) && !btn.contains(e.target)) nav.classList.remove('open');
});

// ===== 検索（カード＋目次を同時に絞り込み） =====
var cards = Array.prototype.slice.call(document.querySelectorAll('#slidesGrid .x-card'));
var tocItems = Array.prototype.slice.call(document.querySelectorAll('#tocList .toc-item'));
var totalCount = cards.length;
var searchEl = document.getElementById('xSearch');
var clearEl = document.getElementById('xClear');
var countEl = document.getElementById('xCount');
var emptyEl = document.getElementById('xEmpty');

function normalize(s){ return (s||'').toLowerCase().replace(/\s+/g,''); }
function applyFilter() {
  var q = normalize(searchEl.value);
  clearEl.style.display = searchEl.value ? 'block' : 'none';
  var shown = 0;
  cards.forEach(function(c){
    var hit = !q || normalize(c.dataset.search).indexOf(q) !== -1;
    c.classList.toggle('hidden', !hit);
    if (hit) shown++;
  });
  tocItems.forEach(function(t){
    var hit = !q || normalize(t.dataset.search).indexOf(q) !== -1;
    t.classList.toggle('hidden', !hit);
  });
  emptyEl.style.display = shown ? 'none' : 'block';
  countEl.textContent = q ? (shown + ' / ' + totalCount + ' 本を表示') : ('全 ' + totalCount + ' 本');
}
searchEl.addEventListener('input', applyFilter);
clearEl.addEventListener('click', function(){ searchEl.value=''; applyFilter(); searchEl.focus(); });

// 目次クリック → 該当カードへスクロール＆ハイライト
tocItems.forEach(function(t){
  t.addEventListener('click', function(e){
    var id = t.getAttribute('href').slice(1);
    var card = document.getElementById(id);
    if (!card) return;
    e.preventDefault();
    if (card.classList.contains('hidden')) { searchEl.value=''; applyFilter(); }
    card.scrollIntoView({behavior:'smooth', block:'center'});
    card.classList.remove('flash'); void card.offsetWidth; card.classList.add('flash');
  });
});

// ===== ライトボックス =====
var lbIndex = -1;
function visibleCards() { return cards.filter(function(c){ return !c.classList.contains('hidden'); }); }
function lbShow(i) {
  var v = visibleCards();
  if (!v.length) return;
  lbIndex = (i + v.length) % v.length;
  var card = v[lbIndex];
  var img = card.querySelector('img');
  document.getElementById('lbImg').src = img.src;
  document.getElementById('lbImg').alt = img.alt;
  document.getElementById('lbCap').innerHTML = '<b>Vol.' + card.dataset.vol + '</b>' + card.dataset.title;
  document.getElementById('lb').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function lbStep(d) { lbShow(lbIndex + d); }
function lbClose() {
  document.getElementById('lb').classList.remove('open');
  document.body.style.overflow = '';
  lbIndex = -1;
}
cards.forEach(function(card){
  card.addEventListener('click', function(){ lbShow(visibleCards().indexOf(card)); });
  card.addEventListener('keydown', function(e){
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); card.click(); }
  });
});
document.getElementById('lb').addEventListener('click', function(e){ if (e.target.id === 'lb') lbClose(); });
document.addEventListener('keydown', function(e){
  if (lbIndex < 0) return;
  if (e.key === 'Escape') lbClose();
  else if (e.key === 'ArrowRight') lbStep(1);
  else if (e.key === 'ArrowLeft') lbStep(-1);
});

applyFilter();
</script>
<script src="../assets/js/motion.js?v=20260718" defer></script>
</body>
</html>
"""

import os, re, glob, io, html as H
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(REPO, "assets", "x", "html")
OUT  = os.path.join(REPO, "slides", "index.html")

def clean_title(t):
    t = t.strip()
    t = re.sub(r'^X技術Tips\s*', '', t)
    t = re.sub(r'^Vol\.?\s*\d+(-\d+)?\s*', '', t)
    t = re.sub(r'^[（(]Layout\s*[A-Z][^）)]*[）)]\s*', '', t)
    t = re.sub(r'^[（(][^）)]*[）)]\s*', '', t) if t.startswith('（') or t.startswith('(') else t
    return t.strip()

def rel(p):
    # path relative to slides/index.html
    p = os.path.abspath(p)
    return "../" + os.path.relpath(p, REPO).replace("\\", "/")

def main_png(folder_abs, folder_name):
    num = folder_name.split('-')[1]
    cand = os.path.join(folder_abs, "vol%s.png" % num)
    if os.path.isfile(cand):
        return cand
    pngs = sorted(glob.glob(os.path.join(folder_abs, "*.png")), key=len)
    return pngs[0] if pngs else None

def title_of(idx):
    t = io.open(idx, encoding="utf-8", errors="ignore").read()
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    return H.unescape(m.group(1).strip()) if m else ""

items = []  # (vol, title, imgrel)

# --- old chips Vol.1-30 ---
OLD = [
 (1,"2026-02-15","Copilot Studio × Power Automate × Word連携　つまずきポイント3選","2026-02-15-x-vol01.png"),
 (2,"2026-02-17","Copilot Studio × Power Automateの連携ステップ","2026-02-17-x-vol02.png"),
 (3,"2026-02-19","Wordのコンテンツコントロール設定方法（前編）","2026-02-19-x-vol03.png"),
 (4,"2026-02-21","Wordのコンテンツコントロール設定方法（後編）","2026-02-21-x-vol04.png"),
 (5,"2026-02-23","Copilot Studio｜質問ノードは聞く順番を意識すると会話が自然になる","2026-02-23-x-vol05.png"),
 (6,"2026-02-25","Copilot Studio｜Topicsの左右の使い方","2026-02-25-x-vol06.png"),
 (7,"2026-02-27","Copilot Studio｜ホーム画面4つのアイコンの役割","2026-02-27-x-vol07.png"),
 (8,"2026-03-01","Copilot Studio｜ツール（エージェントフロー）の役割","2026-03-01-x-vol08.png"),
 (9,"2026-03-03","Copilot Studio｜カスタムプロンプト画面の役割","2026-03-03-x-vol09.png"),
 (10,"2026-03-05","Copilot Studio｜カスタム変数とシステム変数の違い","2026-03-05-x-vol10.png"),
 (12,"2026-03-07","Power Automate：結合(JOIN)で配列を1本の文字列にまとめる","2026-03-07-x-vol12.png"),
 (13,"2026-03-09","Power Automate：1アクションでTeams通知を自動化する","2026-03-09-x-vol13.png"),
 (14,"2026-03-10","Power Automate：Teams通知・送信1アクションでできること","2026-03-10-x-vol14.png"),
 (15,"2026-03-11","Power Automate：会議の作成アクションで予定を自動化する","2026-03-11-x-vol15.png"),
 (16,"2026-03-12","Power Automate：JSONの解析が苦手な人向け・Composeで軽量処理","2026-03-12-x-vol16.png"),
 (17,"2026-03-13","Power Automate：【作成】アクションでライトなJSON処理をする","2026-03-13-x-vol17.png"),
 (18,"2026-03-14","Power Automate：JSONの構造をイラストで理解する","2026-03-14-x-vol18.png"),
 (19,"2026-03-15","Power Automate：【JSONの解析】アクションで動的コンテンツを使う","2026-03-15-x-vol19.png"),
 (20,"2026-03-16","Power Automate：【フィルターアレイ】で必要なデータだけを残す","2026-03-16-x-vol20.png"),
 (21,"2026-03-17","Power Automate：ハマりがちな7つの問題と解決方法","2026-03-17-x-vol21.png"),
 (22,"2026-03-18","Power Automate：条件(Condition)のequalsとcontainsを正しく使い分ける","2026-03-18-x-vol22.png"),
 (23,"2026-03-19","Power Automate：実務で効く通知設計・Before→After","2026-03-19-x-vol23.png"),
 (24,"2026-03-20","Power Automate：Condition（条件）は「質問をつくるアクション」","2026-03-20-x-vol24.png"),
 (25,"2026-03-21","Power Automate：翌月1日を毎月自動で出す方法","2026-03-21-x-vol25.png"),
 (26,"2026-03-22","Power Automate：前月末は「月初から1日戻る」で一発","2026-03-22-x-vol26.png"),
 (27,"2026-03-11","Power Automate：今月の最終営業日を出す方法","__vol27__"),
 (28,"2026-03-23","Power Automate：毎月の「◯営業日目」を自動で出す方法","2026-03-23-x-vol28.png"),
 (29,"2026-03-24","Power Automate：if()で条件分岐をシンプルに書く","2026-03-24-x-vol29.png"),
 (30,"2026-03-25","Power Automate：空欄のせいでフローが止まる問題を解決する","2026-03-25-x-vol30.png"),
]
for vol,date,title,fn in OLD:
    if fn == "__vol27__":
        img = "../assets/img/slide-vol27-date.png"
    else:
        img = "../assets/x/" + fn
    items.append((vol, title, img))

# --- new series folders (vol-NN primary) + _archive ---
scan_dirs = [(HTML, "")]
arch = os.path.join(HTML, "_archive")
if os.path.isdir(arch):
    scan_dirs.append((arch, "_archive"))

for base, _tag in scan_dirs:
    for folder in sorted(os.listdir(base)):
        if not re.fullmatch(r'vol-\d+', folder):
            continue
        fabs = os.path.join(base, folder)
        idx = os.path.join(fabs, "index.html")
        if not os.path.isfile(idx):
            continue
        title = title_of(idx)
        mv = re.search(r'Vol\.?\s*(\d+)', title)
        if not mv:
            continue  # templates without a Vol number
        dvol = int(mv.group(1))
        png = main_png(fabs, folder)
        if not png:
            continue
        items.append((dvol, clean_title(title), rel(png)))

# de-dup exact (vol,img) just in case; keep collisions (same vol, different img)
seen = set(); uniq = []
for v,t,img in items:
    key = (v, img)
    if key in seen: continue
    seen.add(key); uniq.append((v,t,img))
items = uniq
items.sort(key=lambda r: (r[0], r[2]))

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

cards=[]; toc=[]
counter={}
for vol,title,img in items:
    counter[vol]=counter.get(vol,0)+1
    cid = "vol%d" % vol if counter[vol]==1 else "vol%d-%d" % (vol,counter[vol])
    t = esc(title)
    search = ("vol.%d vol%d %s" % (vol, vol, title)).lower()
    search = esc(search)
    cards.append(
'      <figure class="x-card" id="%s" data-vol="%d" data-title="%s" data-search="%s" tabindex="0" role="button" aria-label="Vol.%d %s を拡大">\n'
'        <div class="x-shot"><img src="%s" alt="Vol.%d %s" loading="lazy" width="1200" height="675"></div>\n'
'        <figcaption class="x-cap"><span class="x-vol">Vol.%d</span><span class="x-ttl">%s</span></figcaption>\n'
'      </figure>' % (cid, vol, t, search, vol, t, img, vol, t, vol, t))
    toc.append(
'        <a class="toc-item" href="#%s" data-search="%s"><span class="toc-vol">%d</span><span class="toc-ttl">%s</span></a>'
        % (cid, search, vol, t))

CARDS="\n".join(cards)
TOC="\n".join(toc)
COUNT=str(len(items))

tpl = TEMPLATE
out = tpl.replace("__CARDS__", CARDS).replace("__TOC__", TOC).replace("__COUNT__", COUNT)
io.open(OUT, "w", encoding="utf-8").write(out)
print("total items:", len(items))
vols=[i[0] for i in items]
print("range:", min(vols), "-", max(vols))
from collections import Counter
dups={k:v for k,v in Counter(vols).items() if v>1}
print("dup vols:", dups)

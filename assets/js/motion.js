/* =====================================================
   PA45 Motion Layer — スクロール連動アニメーション
   ・スクロール・リベール（.rv 自動付与 → .in で出現）
   ・数字カウントアップ（.hero-stat-n / .proof-n）
   ・ヘッダーのスクロール影（.site-header.scrolled）
   IntersectionObserver 非依存（scrollイベント方式）／
   prefers-reduced-motion 尊重／JS無効でも通常表示。
   ===================================================== */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = document.querySelector('.site-header');

  /* ---- スクロール進捗バー ---- */
  var progress = document.createElement('div');
  progress.className = 'scroll-progress';
  document.body.appendChild(progress);
  function updateProgress() {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
  }

  /* ---- リベール対象を自動収集 ---- */
  var SELECTORS = [
    '.card', '.proof-card', '.voice-card', '.event-card', '.fork-card',
    '.slide-mini-card', '.past-card', '.hero-stat', '.section-label',
    '.archive-intro', '.next-event'
  ].join(',');
  var els = [];
  if (!reduce) {
    els = Array.prototype.slice.call(document.querySelectorAll(SELECTORS))
      .filter(function (e) { return !e.classList.contains('fade-up') && !e.closest('.fade-up'); });
    els.forEach(function (e, i) {
      e.classList.add('rv');
      e.style.setProperty('--rvd', ((i % 5) * 0.07) + 's');
    });
  }

  /* ---- カウントアップ対象 ---- */
  var nums = Array.prototype.slice.call(document.querySelectorAll('.hero-stat-n, .proof-n'));
  var counted = [];

  function countUp(el) {
    var m = (el.textContent || '').trim().match(/^([0-9][0-9,.]*)(.*)$/);
    if (!m) return; // 「無料」など数値でないものはそのまま
    var target = parseFloat(m[1].replace(/,/g, ''));
    var suffix = m[2] || '';
    var dec = (m[1].split('.')[1] || '').length;
    if (reduce || isNaN(target)) return;
    var dur = 1100, t0 = performance.now();
    function step(t) {
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = (target * e).toFixed(dec) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
    setTimeout(function () { el.textContent = m[1] + suffix; }, dur + 150); // 最終値保証
  }

  /* ---- スクロールハンドラ ---- */
  function onScroll() {
    updateProgress();
    if (header) header.classList.toggle('scrolled', window.scrollY > 8);
    var vh = window.innerHeight;
    els.forEach(function (e) {
      if (e.classList.contains('in')) return;
      var r = e.getBoundingClientRect();
      if (r.top < vh * 0.92 && r.bottom > 0) e.classList.add('in');
    });
    nums.forEach(function (el) {
      if (counted.indexOf(el) !== -1) return;
      var r = el.getBoundingClientRect();
      if (r.top < vh * 0.95 && r.bottom > 0) { counted.push(el); countUp(el); }
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onScroll);
  } else { onScroll(); }
  window.addEventListener('load', onScroll);

  /* 保険：4秒後に未発火分をすべて表示（どんな環境でも欠けない） */
  setTimeout(function () { els.forEach(function (e) { e.classList.add('in'); }); }, 4000);
})();

// PA45 共通JavaScript

// ハンバーガーメニュー開閉
function toggleMenu() {
  const nav = document.getElementById('mobileNav');
  nav.classList.toggle('open');
}

// メニュー外クリックで閉じる
document.addEventListener('click', function(e) {
  const nav = document.getElementById('mobileNav');
  const btn = document.querySelector('.hamburger');
  if (nav && nav.classList.contains('open') && !nav.contains(e.target) && btn && !btn.contains(e.target)) {
    nav.classList.remove('open');
  }
});

// 現在のページのナビリンクに .current クラスを付ける
document.addEventListener('DOMContentLoaded', function() {
  const links = document.querySelectorAll('.header-nav a, .mobile-nav a');
  const path  = window.location.pathname;
  links.forEach(function(link) {
    const href = link.getAttribute('href');
    if (href && path.includes(href) && href !== '../' && href !== './') {
      link.classList.add('current');
    }
  });
});

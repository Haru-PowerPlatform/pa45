/* PA45 インサイトページ共通スクリプト（achievements/insights/*.html から読み込み） */

function esc(s) {
  return (s || '').replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
}

/** heroの数字カード1枚 */
function stat(n, unit, label) {
  return `<div class="ins-stat"><div class="n">${n}<span>${unit}</span></div><div class="l">${label}</div></div>`;
}

/** 積み上げ横バー + 凡例（pcts: {選択肢:％}, keys: [[選択肢,色]], counts: [[選択肢,人数]] 任意） */
function stackBar(pcts, keys, counts) {
  const cmap = Object.fromEntries(counts || []);
  const seg = keys.map(([k, c]) => {
    const p = pcts[k] || 0;
    return p > 0
      ? `<div class="ins-seg" style="width:${p}%;background:${c};" title="${k} ${p}%">${p >= 8 ? p + '%' : ''}</div>`
      : '';
  }).join('');
  const legend = keys.filter(([k]) => (pcts[k] || 0) > 0).map(([k, c]) => {
    const n = cmap[k] != null ? `（${cmap[k]}人）` : '';
    return `<span><i style="background:${c}"></i>${esc(k)} ${pcts[k]}%${n}</span>`;
  }).join('');
  return `<div class="ins-bar">${seg}</div><div class="ins-legend">${legend}</div>`;
}

/** ランキングリスト（rows: [[ラベル, 件数]]） */
function rankList(rows, opts) {
  const o = opts || {};
  const max = Math.max(1, ...rows.map(r => r[1]));
  return '<ul class="ins-rank">' + rows.map(([label, n], i) =>
    `<li><span class="rk">${i + 1}</span>`
    + `<span><span class="lb">${esc(label)}</span><span class="tr"><span style="width:${Math.round(n / max * 100)}%"></span></span></span>`
    + `<span class="nm">${n}${o.unit || '人'}</span></li>`
  ).join('') + '</ul>';
}

/** data/insights.json を取得（GitHub Pages / ローカル両対応） */
async function loadInsights() {
  for (const u of ['../../data/insights.json', '/pa45/data/insights.json']) {
    try {
      const r = await fetch(u);
      if (r.ok) return await r.json();
    } catch (e) { /* 次の候補へ */ }
  }
  document.querySelectorAll('[data-ins-fallback]').forEach(el => {
    el.innerHTML = '<p style="color:var(--c-muted);">データの読み込みに失敗しました。時間をおいて再読み込みしてください。</p>';
  });
  return null;
}

const TYPE_CONFIG = {
  X:    { label: "X 投稿",  color: "#0f172a" },
  PA45: { label: "PA45",    color: "#2563eb" },
  blog: { label: "ブログ",  color: "#059669" },
  登壇: { label: "登壇",    color: "#d97706" },
};

function typeConfig(type) {
  return TYPE_CONFIG[type] ?? { label: type ?? "活動", color: "#64748b" };
}

async function loadLatestActivities(limit = 5) {
  const listEl = document.getElementById("latest-activities-list");
  if (!listEl) return;

  const indexRes = await fetch("data/meta/activities-index.json");
  if (!indexRes.ok) {
    listEl.innerHTML = "<p style='color:#999;font-size:14px;'>読み込みに失敗しました。</p>";
    return;
  }

  const paths = await indexRes.json();
  const items = await Promise.all(
    paths.map(async (p) => {
      const res = await fetch(p);
      if (!res.ok) return null;
      return await res.json();
    })
  );

  const valid = items.filter(Boolean);
  valid.sort((a, b) => (b.date || "").localeCompare(a.date || ""));
  const latest = valid.slice(0, limit);

  listEl.innerHTML = "";

  for (const a of latest) {
    const cfg = typeConfig(a.type);

    // リンク先を決定
    let href = null;
    if (a.evidence) {
      href = a.evidence.blog || a.evidence.connpass || a.evidence.slide || null;
    }

    const card = document.createElement(href ? "a" : "div");
    card.className = "act-feed-card";
    if (href) {
      card.href = href;
      card.target = "_blank";
      card.rel = "noopener";
    }

    // タグ一覧（最大3件）
    const tags = (a.tags || []).slice(0, 3)
      .map(t => `<span class="act-feed-tag">${t}</span>`)
      .join("");

    // エビデンスリンク
    const links = [];
    if (a.evidence?.blog)      links.push(`<a href="${a.evidence.blog}" target="_blank" rel="noopener" class="act-feed-link">📖 ブログ</a>`);
    if (a.evidence?.slide)     links.push(`<a href="${a.evidence.slide}" target="_blank" rel="noopener" class="act-feed-link">📊 スライド</a>`);
    if (a.evidence?.connpass)  links.push(`<a href="${a.evidence.connpass}" target="_blank" rel="noopener" class="act-feed-link">🔗 connpass</a>`);

    card.innerHTML = `
      <div class="act-feed-top">
        <span class="act-feed-badge" style="background:${cfg.color};">${cfg.label}</span>
        <span class="act-feed-date">${a.date ?? ""}</span>
      </div>
      <div class="act-feed-title">${a.title ?? ""}</div>
      <div class="act-feed-desc">${a.summary ?? ""}</div>
      ${tags ? `<div class="act-feed-tags">${tags}</div>` : ""}
      ${links.length ? `<div class="act-feed-links">${links.join("")}</div>` : ""}
    `;
    listEl.appendChild(card);
  }
}

loadLatestActivities(5).catch(console.error);

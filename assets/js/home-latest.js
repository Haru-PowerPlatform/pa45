console.log("home-latest.js loaded");

const TYPE_CONFIG = {
  X:    { label: "X 投稿",  color: "#0f172a" },
  PA45: { label: "PA45",    color: "#2563eb" },
  blog: { label: "ブログ",  color: "#059669" },
  登壇: { label: "登壇",    color: "#d97706" },
};

function typeConfig(type) {
  return TYPE_CONFIG[type] ?? { label: type ?? "活動", color: "#64748b" };
}

async function loadLatestActivities(limit = 3) {
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
  listEl.style.cssText = "display:flex;flex-direction:column;gap:10px;";

  for (const a of latest) {
    const cfg = typeConfig(a.type);
    const card = document.createElement("div");
    card.className = "act-feed-card";
    card.innerHTML = `
      <div class="act-feed-top">
        <span class="act-feed-badge" style="background:${cfg.color};">${cfg.label}</span>
        <span class="act-feed-date">${a.date ?? ""}</span>
      </div>
      <div class="act-feed-title">${a.title ?? ""}</div>
      <div class="act-feed-desc">${a.summary ?? ""}</div>
    `;
    listEl.appendChild(card);
  }
}

loadLatestActivities(3).catch(console.error);

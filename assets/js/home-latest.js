console.log("home-latest.js loaded");

async function loadLatestActivities(limit = 3) {
  const listEl = document.getElementById("latest-activities-list");
  if (!listEl) return;

  const indexRes = await fetch("data/meta/activities-index.json");
  if (!indexRes.ok) {
    listEl.innerHTML = "<li>最新実績の読み込みに失敗しました。</li>";
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
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>${a.date ?? ""}</strong> — ${a.title ?? ""}<br>
      <small>${a.summary ?? ""}</small>
    `;
    listEl.appendChild(li);
  }
}

loadLatestActivities(3).catch(console.error);

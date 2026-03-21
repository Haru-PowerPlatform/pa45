console.log("activities.js loaded"); // 動作確認用

async function main() {
  const listEl = document.getElementById("activity-list");
  if (!listEl) throw new Error("ul#activity-list が見つかりません");

  // 目次ファイルを取得（activities/ から見て ../data/...）
  const indexRes = await fetch("../data/meta/activities-index.json");
  if (!indexRes.ok) throw new Error("index json の取得に失敗: " + indexRes.status);

  const paths = await indexRes.json(); // ["data/activities/xxx.json", ...]
  if (!Array.isArray(paths)) throw new Error("activities-index.json は配列にしてください");

  // 各実績JSONを取得して配列にする
  const items = await Promise.all(
    paths.map(async (p) => {
      const res = await fetch("../" + p);
      if (!res.ok) throw new Error("activity json の取得に失敗: " + p + " status=" + res.status);
      return await res.json();
    })
  );

  // 新しい順に並べる
  items.sort((a, b) => (b.date || "").localeCompare(a.date || ""));

  // 表示
  listEl.innerHTML = "";
  for (const data of items) {
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>${data.date ?? ""}</strong><br>
      ${data.title ?? ""}<br>
      <small>${data.summary ?? ""}</small>
    `;
    listEl.appendChild(li);
  }
}

main().catch((e) => {
  console.error(e);
});

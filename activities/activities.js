async function main() {
  const listEl = document.getElementById("activity-list");

  // 目次ファイルを取得
  const indexRes = await fetch("../data/meta/activities-index.json");
  const paths = await indexRes.json(); // ["data/activities/xxx.json", ...]

  // 各実績JSONを取得して配列にする
  const items = await Promise.all(
    paths.map(async (p) => {
      const res = await fetch("../" + p);
      return await res.json();
    })
  );

  // 日付で新しい順に並べる
  items.sort((a, b) => (b.date || "").localeCompare(a.date || ""));

  // 表示
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

main().catch(console.error);

fetch('../data/activities/2026-03-test.json')
  .then(response => response.json())
  .then(data => {
    const list = document.getElementById('activity-list');

    const li = document.createElement('li');
    li.innerHTML = `
      <strong>${data.date}</strong><br>
      ${data.title}<br>
      <small>${data.summary}</small>
    `;

    list.appendChild(li);
  });

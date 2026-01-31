const API = "http://127.0.0.1:8000";

function showTab(tab) {
  document.getElementById("generate").style.display = tab === "generate" ? "block" : "none";
  document.getElementById("history").style.display = tab === "history" ? "block" : "none";

  if (tab === "history") loadHistory();
}

async function generateQuiz() {
  const url = document.getElementById("wikiUrl").value;
  const res = await fetch(`${API}/generate-quiz?url=${encodeURIComponent(url)}`, {
    method: "POST"
  });
  const data = await res.json();

  document.getElementById("quizResult").innerHTML =
    `<p><b>${data.title}</b> – ${data.quiz_count} questions generated</p>`;
}

async function loadHistory() {
  const res = await fetch(`${API}/history`);
  const data = await res.json();

  const table = document.getElementById("historyTable");
  table.innerHTML = "";

  data.forEach(item => {
    table.innerHTML += `
      <tr>
        <td>${item.id}</td>
        <td>${item.title}</td>
        <td><button onclick="openDetails(${item.id})">Details</button></td>
      </tr>
    `;
  });
}

async function openDetails(id) {
  const res = await fetch(`${API}/quiz/${id}`);
  const data = await res.json();

  let html = `<h2>${data.title}</h2><p>${data.summary}</p>`;

  data.quiz.forEach(q => {
    html += `<hr><p><b>${q.question}</b></p>`;
    for (let key in q.options) {
      html += `<p>${key}: ${q.options[key]}</p>`;
    }
    html += `<p><i>Answer:</i> ${q.answer}</p>`;
  });

  document.getElementById("modalBody").innerHTML = html;
  document.getElementById("modal").style.display = "block";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
}
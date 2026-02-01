const API = "http://127.0.0.1:8000";

function showTab(tab) {
  document.getElementById("generate").style.display = tab === "generate" ? "block" : "none";
  document.getElementById("history").style.display = tab === "history" ? "block" : "none";

  if (tab === "history") loadHistory();
}

async function generateQuiz() {
  const url = document.getElementById("wikiUrl").value;

  // Step 1: generate & store quiz
  const res = await fetch(`${API}/generate-quiz?url=${encodeURIComponent(url)}`, {
    method: "POST"
  });
  const genData = await res.json();

  // Step 2: fetch full quiz using article_id
  const quizRes = await fetch(`${API}/quiz/${genData.article_id}`);
  const quizData = await quizRes.json();

  // Step 3: render quiz
  let html = `<h2>${quizData.title}</h2><p>${quizData.summary}</p>`;

  quizData.quiz.forEach((q, index) => {
    html += `<div style="border:1px solid #ccc; padding:10px; margin:10px 0">
      <p><b>Q${index + 1}. ${q.question}</b></p>`;

    for (let key in q.options) {
      html += `<p>${key}: ${q.options[key]}</p>`;
    }

    html += `<p><i>Answer:</i> ${q.answer}</p>
             <p><i>Difficulty:</i> ${q.difficulty}</p>
             <p><i>Explanation:</i> ${q.explanation}</p>
    </div>`;
  });

  document.getElementById("quizResult").innerHTML = html;
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

/* ✅ NEW DETAILS FUNCTION (NO MODAL) */
async function openDetails(id) {
  const res = await fetch(`${API}/quiz/${id}`);
  const data = await res.json();

  let html = `<h2>${data.title}</h2><p>${data.summary}</p>`;

  data.quiz.forEach((q, index) => {
    html += `
      <div style="border:1px solid #ccc; padding:15px; margin:15px 0;">
        <p><b>Q${index + 1}. ${q.question}</b></p>
    `;

    for (let key in q.options) {
      html += `<p>${key}: ${q.options[key]}</p>`;
    }

    html += `
        <p><i>Answer:</i> ${q.answer}</p>
        <p><i>Difficulty:</i> ${q.difficulty}</p>
        <p><i>Explanation:</i> ${q.explanation}</p>
      </div>
    `;
  });

  document.getElementById("detailsSection").innerHTML = html;

  // scroll to details automatically
  document.getElementById("detailsSection").scrollIntoView({ behavior: "smooth" });
}

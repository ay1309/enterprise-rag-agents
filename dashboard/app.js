async function loadStats() {
  const res = await fetch("/api/sessions");
  const data = await res.json();
  document.getElementById("doc-count").textContent = data.document_count;
  document.getElementById("chunk-count").textContent = data.total_chunks;
  const grid = document.getElementById("doc-grid");
  grid.innerHTML = data.documents.length
    ? data.documents.map(d => `
        <div class="doc-card">
          <div class="doc-icon">📄</div>
          <div class="doc-name">${d}</div>
        </div>`).join("")
    : "<p style='color:#999;font-size:14px'>No documents uploaded yet. :c </p>";
}

loadStats();
setInterval(loadStats, 10000); // refresca cada 10 segundos
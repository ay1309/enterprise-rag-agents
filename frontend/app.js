const clientId = crypto.randomUUID();
const ws = new WebSocket(`ws://${location.host}/ws/chat/${clientId}`);
const chatWindow = document.getElementById("chat-window");
const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const statusEl = document.getElementById("status");

let currentBubble = null;

ws.onopen = () => {
  statusEl.textContent = "Connected";
  statusEl.className = "status online";
  loadDocuments();
};
ws.onclose = () => {
  statusEl.textContent = "Disconnected";
  statusEl.className = "status offline";
};

ws.onmessage = ({ data }) => {
  const msg = JSON.parse(data);
  if (msg.type === "chunk") {
    currentBubble.textContent += msg.text;
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }
  if (msg.type === "done") {
    currentBubble = null;
    sendBtn.disabled = false;
  }
};

function addMessage(text, role) {
  document.querySelector(".welcome")?.remove();
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = text;
  chatWindow.appendChild(div);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return div;
}

function sendMessage() {
  const text = input.value.trim();
  if (!text || sendBtn.disabled) return;
  addMessage(text, "user");
  input.value = "";
  input.style.height = "auto";
  currentBubble = addMessage("", "assistant");
  sendBtn.disabled = true;
  ws.send(JSON.stringify({ message: text }));
}

sendBtn.onclick = sendMessage;
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});
input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = input.scrollHeight + "px";
});

document.getElementById("pdf-input").onchange = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  addMessage(`Uploading: ${file.name}...`, "system");
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/documents/upload", { method: "POST", body: form });
  const data = await res.json();
  addMessage(data.message || data.error, "system");
  loadDocuments();
};

async function loadDocuments() {
  const res = await fetch("/api/documents");
  const data = await res.json();
  const list = document.getElementById("doc-list");
  list.innerHTML = data.documents.map(d => `<span class="doc-tag">📄 ${d}</span>`).join("");
}
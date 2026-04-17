const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const status = document.getElementById("status");

userInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

userInput.addEventListener("input", () => {
  userInput.style.height = "auto";
  userInput.style.height = Math.min(userInput.scrollHeight, 120) + "px";
});

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  userInput.value = "";
  userInput.style.height = "auto";
  setLoading(true);

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();

    if (data.error) {
      appendMessage("assistant", "Error: " + data.error);
    } else {
      appendMessage("assistant", data.reply, data.tool_results);
    }
    loadFiles();
  } catch (err) {
    appendMessage("assistant", "Connection error. Is the Flask server running?");
  } finally {
    setLoading(false);
  }
}

function formatReply(text) {
  const div = document.createElement("div");

  const parts = text.split(/(```[\w]*\n[\s\S]*?```)/g);
  parts.forEach((part) => {
    if (part.startsWith("```")) {
      const lines = part.split("\n");
      const lang = lines[0].replace("```", "").trim() || "plaintext";
      const code = lines.slice(1, -1).join("\n");

      const wrapper = document.createElement("div");
      wrapper.className = "code-block";

      const header = document.createElement("div");
      header.className = "code-header";

      const langLabel = document.createElement("span");
      langLabel.textContent = lang;

      const copyBtn = document.createElement("button");
      copyBtn.className = "copy-btn";
      copyBtn.textContent = "Copy";
      copyBtn.onclick = () => {
        navigator.clipboard.writeText(code);
        copyBtn.textContent = "Copied!";
        setTimeout(() => (copyBtn.textContent = "Copy"), 2000);
      };

      header.appendChild(langLabel);
      header.appendChild(copyBtn);

      const pre = document.createElement("pre");
      const codeEl = document.createElement("code");
      codeEl.className = `language-${lang}`;
      codeEl.textContent = code;
      hljs.highlightElement(codeEl);

      pre.appendChild(codeEl);
      wrapper.appendChild(header);
      wrapper.appendChild(pre);
      div.appendChild(wrapper);
    } else if (part.trim()) {
      const p = document.createElement("p");
      p.textContent = part;
      div.appendChild(p);
    }
  });

  return div;
}

function appendMessage(role, text, toolResults = []) {
  const msg = document.createElement("div");
  msg.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "You" : "AI";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  if (role === "assistant") {
    bubble.appendChild(formatReply(text));
  } else {
    bubble.textContent = text;
  }

  if (toolResults.length > 0) {
    toolResults.forEach((t) => {
      const isError = t.result.startsWith("Error:");

      const label = document.createElement("div");
      label.className = "tool-label";
      label.textContent = `⚙ ${t.tool}(${Object.values(t.args).join(", ")})`;

      const resultWrapper = document.createElement("div");
      resultWrapper.className = `code-block ${isError ? "tool-error" : ""}`;

      const header = document.createElement("div");
      header.className = "code-header";

      const langLabel = document.createElement("span");
      langLabel.textContent = isError ? "error" : "output";

      const copyBtn = document.createElement("button");
      copyBtn.className = "copy-btn";
      copyBtn.textContent = "Copy";
      copyBtn.onclick = () => {
        navigator.clipboard.writeText(t.result);
        copyBtn.textContent = "Copied!";
        setTimeout(() => (copyBtn.textContent = "Copy"), 2000);
      };

      header.appendChild(langLabel);
      header.appendChild(copyBtn);

      const pre = document.createElement("pre");
      const code = document.createElement("code");
      code.textContent = t.result;
      pre.appendChild(code);

      resultWrapper.appendChild(header);
      resultWrapper.appendChild(pre);

      bubble.appendChild(label);
      bubble.appendChild(resultWrapper);
    });
  }

  msg.appendChild(avatar);
  msg.appendChild(bubble);
  chatWindow.appendChild(msg);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function setLoading(loading) {
  sendBtn.disabled = loading;
  status.textContent = loading ? "● Thinking..." : "● Ready";
  status.className = loading ? "status thinking" : "status";
}

async function loadFiles() {
  const list = document.getElementById("file-list");
  try {
    const res = await fetch("/files");
    const data = await res.json();
    list.innerHTML = "";
    if (data.files.length === 0 || data.files[0] === "No files in workspace.") {
      list.innerHTML = "<li class='loading'>No files yet.</li>";
      return;
    }
    data.files.forEach((f) => {
      const ext = f.split(".").pop();
      const icon = ext === "py" ? "🐍" : ext === "sh" ? "⚡" : ext === "txt" ? "📝" : "📄";
      const li = document.createElement("li");
      li.textContent = `${icon} ${f}`;
      li.title = "Click to view";
      li.onclick = () => openFileModal(f);
      list.appendChild(li);
    });
  } catch {
    list.innerHTML = "<li class='loading'>Unable to load files.</li>";
  }
}

async function openFileModal(filename) {
  document.getElementById("modal-filename").textContent = filename;
  const codeEl = document.getElementById("modal-content");
  codeEl.textContent = "Loading...";
  delete codeEl.dataset.highlighted;
  document.getElementById("file-modal").style.display = "flex";

  try {
    const res = await fetch(`/file/${encodeURIComponent(filename)}`);
    const data = await res.json();
    codeEl.textContent = data.content;
    delete codeEl.dataset.highlighted;
    hljs.highlightElement(codeEl);
  } catch {
    codeEl.textContent = "Error loading file.";
  }
}

function closeModal() {
  document.getElementById("file-modal").style.display = "none";
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeModal();
});

async function clearMemory() {
  await fetch("/clear", { method: "POST" });
  chatWindow.innerHTML = "";
  appendMessage("assistant", "Memory cleared. Starting a fresh session.");
}

loadFiles();

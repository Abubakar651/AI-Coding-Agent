# 🤖 AI Coding Agent

An autonomous coding assistant that writes, executes, and debugs Python code through natural language — powered by **Groq API (LLaMA 3.3 70B)** and a recursive agentic loop with custom tools.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=flat-square&logo=flask)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

- **Natural language interface** — just describe what you want built
- **Autonomous code execution** — writes, runs, and reads files without you lifting a finger
- **Self-healing agent** — detects errors and auto-fixes code up to 3 times before asking for help
- **Inline code runner** — execute Python snippets directly without saving a file
- **File viewer** — click any workspace file in the sidebar to preview its contents
- **Persistent memory** — conversation history carried across the session
- **VS Code-inspired UI** — dark theme, syntax highlighting, copy buttons

---

## 🖥️ Demo

```
You:  Write a Python script that scrapes the top 5 headlines from a news site

AI:   → install_package(requests, beautifulsoup4)
      → write_file(scraper.py)
      → run_file(scraper.py)
      ✓ Here are the top 5 headlines: ...
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI Model | Groq API — LLaMA 3.3 70B |
| Tool Calling | Groq native function calling |
| Memory | JSON-based conversation history |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Config | python-dotenv |

---

## 📁 Project Structure

```
AI-Coding-Agent/
├── app.py              # Flask server + agentic loop
├── tools.py            # Custom tools (read, write, run, delete, install)
├── memory.py           # Conversation history management
├── config.py           # Groq client configuration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── ui/
    ├── index.html      # VS Code-style chat interface
    ├── style.css       # Dark theme styling
    └── script.js       # Frontend logic
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Abubakar651/AI-Coding-Agent.git
cd AI-Coding-Agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
GROQ_API_KEY=your_groq_api_key_here
WORKSPACE_DIR=/path/to/your/workspace
```

> Get a free Groq API key at [console.groq.com](https://console.groq.com)

### 5. Run the app

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧰 Available Tools

| Tool | Description |
|---|---|
| `write_file` | Create or update a file in the workspace |
| `read_file` | Read the contents of a file |
| `run_file` | Execute a `.py` or `.sh` file and return output |
| `run_code` | Run a Python snippet directly without saving |
| `delete_file` | Delete a file from the workspace |
| `list_files` | List all files and folders in the workspace |
| `create_folder` | Create a new folder |
| `install_package` | Install a Python package via pip |

---

## ⚙️ How It Works

```
User sends a message
        │
        ▼
Flask receives POST /chat
        │
        ▼
LLaMA 3.3 70B decides which tool(s) to call
        │
        ▼
Tool executes in the workspace
        │
        ▼
If error → agent analyzes, fixes, and retries (up to 3x)
        │
        ▼
Final response displayed in the UI
```

---

## 💬 Example Prompts

```
Write a Python script that generates a random password
Run the script and show me the output
Install the pandas library and create a CSV file with dummy data
List all files in my workspace
What is a recursive function? Explain with an example
```

---

## 📄 License

This project is licensed under the MIT License.

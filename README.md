# AI Coding Agent

An AI-powered coding assistant with a VS Code-inspired interface. Ask it to write, read, run, or debug code files — it handles everything autonomously using tool-calling with Groq's LLaMA 3.3 70B. If the code breaks, the agent detects the error and auto-fixes it without any human intervention.

---

## Features

- Natural language interface for file operations (read, write, run, delete)
- Real-time code execution with output displayed in the UI
- **Self-healing agent** — automatically detects errors and re-runs fixed code (up to 3 attempts)
- **run_code** — execute Python snippets directly without saving a file
- **Click-to-view files** — click any file in the sidebar to preview its contents
- Persistent conversation memory across sessions
- VS Code dark-theme UI served via Flask
- Tool-calling agent — the LLM decides which tool to use automatically

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Flask |
| **AI Model** | Groq API — LLaMA 3.3 70B |
| **Tool Calling** | Groq native function calling |
| **Memory** | JSON-based conversation history |
| **UI** | HTML, CSS, JavaScript |
| **Config** | python-dotenv |

---

## Project Structure

```
AI-Coding-Agent/
├── app.py              # Flask server + agentic loop
├── tools.py            # File read/write/run/delete + run_code tools
├── memory.py           # Conversation history management
├── config.py           # Groq client + environment config
├── requirements.txt
├── .env.example
└── ui/
    ├── index.html      # VS Code-style interface
    ├── style.css       # Dark theme
    └── script.js       # API communication + file viewer
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Abubakar651/AI-Coding-Agent.git
cd AI-Coding-Agent
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
WORKSPACE_DIR=/path/to/your/workspace
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

---

## Running the App

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Example Commands

```
Write a Python script that prints the Fibonacci sequence up to 100
Run fibonacci.py
Write a buggy script and watch the agent auto-fix it
Run this code: print(2 ** 10)
List all files in my workspace
Install the requests library
```

---

## How It Works

```
User types a request
         │
         ▼
Flask receives POST /chat
         │
         ▼
Groq LLaMA 3.3 70B decides which tool to call
         │
         ▼
Tool executes (read / write / run / delete / run_code)
         │
         ▼
If error → agent auto-fixes and retries (up to 3x)
         │
         ▼
Final response + tool output displayed in UI
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serves the UI |
| `/chat` | POST | Send a message to the agent |
| `/clear` | POST | Clear conversation memory |
| `/files` | GET | List workspace files |
| `/file/<name>` | GET | Read a specific file |

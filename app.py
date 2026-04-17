import json
from flask import Flask, request, jsonify, send_from_directory
from groq import BadRequestError
from config import client, MODEL
from memory import load_history, add_message, clear_history, get_context
from tools import TOOL_DEFINITIONS, TOOL_MAP

app = Flask(__name__, static_folder="ui", static_url_path="/static")

SYSTEM_PROMPT = """You are an AI Coding Agent and a friendly assistant running inside a developer's workspace.

IMPORTANT: Only use tools when the user explicitly asks you to write, run, read, delete, or manage files and code. For greetings, general questions, or casual chat — respond in plain text with NO tool calls at all.

When the user asks you to do something with code or files, you have these tools:
- read_file: Read any file in the workspace
- write_file: Create or update files (Python, Bash, text, etc.)
- delete_file: Remove a file
- run_file: Execute Python (.py) or Bash (.sh) files and return output
- run_code: Execute a Python snippet directly without saving a file
- list_files: Show all files and folders in the workspace
- create_folder: Create a new folder to organize files
- install_package: Install any Python package via pip

When code execution returns an error, automatically analyze the error, fix the code
using write_file, and re-run it. Try up to 3 times before asking the user for help.
Always explain what you did in simple terms and show the output."""


@app.route("/")
def index():
    return send_from_directory("ui", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message."}), 400

    history = load_history()
    history = add_message(history, "user", user_message)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_context(history)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
            max_tokens=2048,
        )
    except BadRequestError as e:
        return jsonify({"error": "The model had trouble with that request. Please rephrase and try again."}), 200

    assistant_message = response.choices[0].message
    tool_results = []

    while assistant_message.tool_calls:
        tool_calls_data = []
        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments) or {}
            result = TOOL_MAP[name](**args)
            tool_results.append({"tool": name, "args": args, "result": result})
            tool_calls_data.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": name,
                "content": str(result),
            })

        messages.append(assistant_message)
        messages.extend(tool_calls_data)

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
                max_tokens=2048,
            )
        except BadRequestError:
            return jsonify({"reply": "I ran into an issue generating the next step. Please try again.", "tool_results": tool_results})
        assistant_message = response.choices[0].message

    final_reply = assistant_message.content or "Done."
    history = add_message(history, "assistant", final_reply)

    return jsonify({"reply": final_reply, "tool_results": tool_results})


@app.route("/clear", methods=["POST"])
def clear():
    clear_history()
    return jsonify({"status": "Memory cleared."})


@app.route("/files", methods=["GET"])
def files():
    from tools import list_files
    return jsonify({"files": list_files()})


@app.route("/file/<path:filename>", methods=["GET"])
def get_file(filename):
    from tools import read_file
    return jsonify({"filename": filename, "content": read_file(filename)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

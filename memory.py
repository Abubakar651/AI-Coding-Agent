import json
import os
from config import MEMORY_FILE

MAX_HISTORY = 20


def load_history():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history[-MAX_HISTORY:], f, indent=2)


def add_message(history, role, content):
    history.append({"role": role, "content": content})
    save_history(history)
    return history


def clear_history():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    return []


def get_context(history):
    return history[-MAX_HISTORY:]

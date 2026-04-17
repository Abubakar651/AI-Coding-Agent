import os
import subprocess
import tempfile
from config import WORKSPACE_DIR

RUNNERS = {
    ".py": "python3",
    ".sh": "bash",
}


def _safe_path(path):
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    full = os.path.join(WORKSPACE_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    return full


def read_file(filename):
    path = _safe_path(filename)
    if not os.path.exists(path):
        return f"Error: '{filename}' not found."
    with open(path, "r") as f:
        return f.read()


def write_file(filename, content):
    path = _safe_path(filename)
    with open(path, "w") as f:
        f.write(content)
    return f"File '{filename}' written successfully."


def delete_file(filename):
    path = _safe_path(filename)
    if not os.path.exists(path):
        return f"Error: '{filename}' not found."
    os.remove(path)
    return f"File '{filename}' deleted successfully."


def run_file(filename):
    path = _safe_path(filename)
    if not os.path.exists(path):
        return f"Error: '{filename}' not found."

    ext = os.path.splitext(filename)[1]
    runner = RUNNERS.get(ext)
    if not runner:
        return f"Error: Cannot run '{ext}' files. Supported: {', '.join(RUNNERS.keys())}"

    try:
        result = subprocess.run(
            [runner, path],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=WORKSPACE_DIR,
        )
        output = result.stdout + result.stderr
        return output.strip() if output.strip() else "Script ran with no output."
    except subprocess.TimeoutExpired:
        return "Error: Script timed out after 15 seconds."
    except Exception as e:
        return f"Error running file: {str(e)}"


def run_code(code):
    tmp_path = None
    try:
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, dir=WORKSPACE_DIR
        ) as f:
            f.write(code)
            tmp_path = f.name
        result = subprocess.run(
            ["python3", tmp_path],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=WORKSPACE_DIR,
        )
        output = result.stdout + result.stderr
        return output.strip() if output.strip() else "Code ran with no output."
    except subprocess.TimeoutExpired:
        return "Error: Code timed out after 15 seconds."
    except Exception as e:
        return f"Error running code: {str(e)}"
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


def list_files():
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    items = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        rel_root = os.path.relpath(root, WORKSPACE_DIR)
        for f in files:
            if rel_root == ".":
                items.append(f)
            else:
                items.append(os.path.join(rel_root, f))
    return items if items else ["No files in workspace."]


def create_folder(folder_name):
    path = os.path.join(WORKSPACE_DIR, folder_name)
    os.makedirs(path, exist_ok=True)
    return f"Folder '{folder_name}' created successfully."


def install_package(package_name):
    try:
        result = subprocess.run(
            ["pip", "install", package_name],
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = result.stdout + result.stderr
        last_lines = "\n".join(output.strip().splitlines()[-5:])
        return last_lines if last_lines else f"Installed {package_name}."
    except subprocess.TimeoutExpired:
        return "Error: Installation timed out."
    except Exception as e:
        return f"Error installing package: {str(e)}"


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file from the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name or relative path of the file to read."}
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file in the workspace. Creates the file if it doesn't exist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name or relative path of the file to write."},
                    "content": {"type": "string", "description": "Content to write to the file."},
                },
                "required": ["filename", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a file from the workspace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name of the file to delete."}
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_file",
            "description": "Execute a Python (.py) or Bash (.sh) file and return its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name of the file to run."}
                },
                "required": ["filename"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_code",
            "description": "Execute a Python code snippet directly without saving it as a file. Useful for quick calculations, tests, or experiments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Python code to execute."}
                },
                "required": ["code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files currently in the workspace including subfolders.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_folder",
            "description": "Create a new folder inside the workspace to organize files.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_name": {"type": "string", "description": "Name of the folder to create."}
                },
                "required": ["folder_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "install_package",
            "description": "Install a Python package using pip.",
            "parameters": {
                "type": "object",
                "properties": {
                    "package_name": {"type": "string", "description": "Name of the pip package to install."}
                },
                "required": ["package_name"],
            },
        },
    },
]

TOOL_MAP = {
    "read_file": read_file,
    "write_file": write_file,
    "delete_file": delete_file,
    "run_file": run_file,
    "run_code": run_code,
    "list_files": list_files,
    "create_folder": create_folder,
    "install_package": install_package,
}

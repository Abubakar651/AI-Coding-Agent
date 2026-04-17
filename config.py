import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"
MEMORY_FILE = "chat_history.json"
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", os.path.expanduser("~/workspace"))

client = Groq(api_key=GROQ_API_KEY)

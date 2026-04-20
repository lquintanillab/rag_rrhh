import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_PROJECT_ROOT = Path(__file__).resolve().parent.parent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4.1-mini")

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
PERSIST_DIR = str(_PROJECT_ROOT / "data" / "chroma_db")
FAQ_DOCUMENT_PATH = str(_PROJECT_ROOT / "data" / "faq_document.txt")
TOP_K = 3

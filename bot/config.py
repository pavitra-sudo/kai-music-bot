import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

BOT_TOKEN = os.getenv("BOT_TOKEN")
DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "/mnt/music/music")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found (check .env loading)")

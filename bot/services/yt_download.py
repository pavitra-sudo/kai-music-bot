import os
import logging
from yt_dlp import YoutubeDL

from config import DOWNLOAD_PATH


os.makedirs(DOWNLOAD_PATH, exist_ok=True)


def download_audio(url: str) -> dict:
    logging.info(f"Downloading: {url}")

    ydl_opts = {
        "format": "bestaudio/best",

        # -----------------------------
        # OPUS ONLY OUTPUT
        # -----------------------------
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "opus",
                "preferredquality": "0",
            }
        ],

        "outtmpl": os.path.join(
            DOWNLOAD_PATH,
            "%(title).80s.%(ext)s"
        ),
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl: # type: ignore
        info = ydl.extract_info(url, download=True)

        # -----------------------------
        # DO NOT GUESS FILE NAME
        # -----------------------------
        base_path = ydl.prepare_filename(info)
        audio_path = os.path.splitext(base_path)[0] + ".opus"

    # -----------------------------
    # SAFETY CHECK (CRITICAL)
    # -----------------------------
    if not os.path.exists(audio_path):
        logging.error(f"Primary path missing: {audio_path}")

        # fallback scan (safe recovery)
        for file in os.listdir(DOWNLOAD_PATH):
            if file.endswith(".opus"):
                audio_path = os.path.join(DOWNLOAD_PATH, file)
                break

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio not found: {audio_path}")

    logging.info(f"Downloaded: {audio_path}")

    return {
        "audio_path": audio_path,
        "thumbnail_path": None,
        "title": info.get("title", "Unknown"),
        "artist": info.get("uploader", "Unknown"),
        "album": "YouTube",
        "duration": info.get("duration", 0),
    }
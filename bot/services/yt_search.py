from yt_dlp import YoutubeDL
import logging


def find_best_match(query: str) -> str:
    logging.info(f"Searching for: {query}")

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl: # type: ignore
        result = ydl.extract_info( 
            f"ytsearch1:{query}",
            download=False
        )

    entries = result.get("entries", [])

    if not entries:
        raise ValueError("No results found")

    video = entries[0]

    url = f"https://www.youtube.com/watch?v={video['id']}"

    logging.info(f"Found URL: {url}")

    return url
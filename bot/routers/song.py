import asyncio
import logging

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, FSInputFile

from services.yt_search import find_best_match
from services.yt_download import download_audio
from services.metadata_change import write_metadata

router = Router()


async def safe_delete(msg: Message, delay: int = 0):
    """Delete message safely after optional delay"""
    if delay:
        await asyncio.sleep(delay)
    try:
        await msg.delete()
    except Exception:
        pass


@router.message(Command("song"))
async def song_handler(message: Message, command: CommandObject):
    query = command.args or ""

    if not query:
        await message.answer(
            "🎵 Usage:\n\n"
            "/song <song name>\n"
            "/song <youtube url>"
        )
        return

    status_msg = await message.answer("🔎 Searching song...")

    try:
        # -----------------------------
        # SEARCH / URL RESOLVE
        # -----------------------------
        if query.startswith(("http://", "https://")):
            url = query
        else:
            await status_msg.edit_text("🎯 Finding best match...")
            url = await asyncio.to_thread(find_best_match, query)

        logging.info(f"Selected URL: {url}")

        # -----------------------------
        # DOWNLOADING
        # -----------------------------
        await status_msg.edit_text("⬇️ Downloading audio...")

        song_data = await asyncio.to_thread(download_audio, url)

        # -----------------------------
        # METADATA WRITE
        # -----------------------------
        await status_msg.edit_text("📝 Adding metadata...")

        await asyncio.to_thread(
            write_metadata,
            audio_path=song_data["audio_path"],
            title=song_data["title"],
            artist=song_data["artist"],
            album=song_data["album"],
            thumbnail_path=song_data["thumbnail_path"]
        )

        # -----------------------------
        # UPLOADING
        # -----------------------------
        await status_msg.edit_text("📤 Uploading file...")

        audio_file = FSInputFile(song_data["audio_path"])

        caption = (
            f"🎧 <b>{song_data['title']}</b>\n"
            f"👤 Artist: {song_data['artist']}\n"
            f"💿 Album: {song_data.get('album', 'Unknown')}\n"
            f"⏱ Duration: {song_data['duration'] // 60}:{song_data['duration'] % 60:02d}"
        )

        await message.answer_audio(
            audio=audio_file,
            title=song_data["title"],
            performer=song_data["artist"],
            caption=caption,
            parse_mode="HTML"
        )

        # -----------------------------
        # CLEAN UP STATUS MESSAGE
        # -----------------------------
        await safe_delete(status_msg)

    except Exception as e:
        logging.exception("Song processing failed")

        await status_msg.edit_text("❌ Failed processing request")
        await message.answer(f"❌ Error occurred\n\n{str(e)}")

        await safe_delete(status_msg, delay=5)
import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from routers.start import router as start_router
from routers.help import router as help_router
from routers.song import router as song_router
from log import logging

async def main():
    if BOT_TOKEN is None:
        raise ValueError("BOT_TOKEN not found")

    bot = Bot(BOT_TOKEN)

    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(help_router)
    

    logging.info("🚀 Bot started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Bot stopped")
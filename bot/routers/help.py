from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        """
Help information for the music bot.

/start - Begin using the bot
/song - Search for a song

"""
    )
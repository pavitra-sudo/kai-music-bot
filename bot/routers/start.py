from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello! I'm a music bot. Send me a YouTube link or name, and I'll download the audio for you.")
    
    

    
    
    
from aiogram import Bot, Router
from aiogram.filters import Command
from aiogram.types import Message
from texts.start import START_TEXT

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(START_TEXT, parse_mode="HTML")
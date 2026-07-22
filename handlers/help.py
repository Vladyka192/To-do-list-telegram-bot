from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from texts.help import HELP_TEXT

router = Router()

@router.message(Command("help"))
async def help(message: Message):
    await message.answer(HELP_TEXT, parse_mode="HTML")
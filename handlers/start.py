from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from texts.start import START_TEXT

from keyboards.menu import main_menu_kb

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    
    await message.answer(START_TEXT, parse_mode="HTML", reply_markup=main_menu_kb())
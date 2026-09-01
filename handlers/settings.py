from aiogram import Router, F
# from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from keyboards.settings_menu import settings_menu_kb

router = Router()

@router.message(F.text == "Настройки")
async def settings(message: Message):
    await message.answer("нуы", reply_markup=settings_menu_kb())
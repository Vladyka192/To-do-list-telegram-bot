from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import text
from repositories.user import UserRepo
from texts.start import START_TEXT

from keyboards.menu import main_menu_kb

router = Router()

@router.message(Command("start"))
async def start(message: Message, user_repo: UserRepo):
    await user_repo.create_or_update_user(message.from_user.id, message.from_user.full_name, message.from_user.username, "Asia/Almaty")
    await message.answer(START_TEXT, parse_mode="HTML", reply_markup=main_menu_kb())
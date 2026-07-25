from aiogram import Router, types, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "Задачи")
async def task(message: Message):
    await message.answer("У вас на сегодня нет задач", reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Создать задачу", callback_data="addtask")]
        ]
    ))

@router.callback_query(F.data == "addtask")
async def create_task(callback: types.CallbackQuery):
    await callback.message.answer("Напишите название задачи")
from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

class AddTask(StatesGroup):
    choosing_task_name = State()
    choosing_task_date = State()
    choosing_task_time = State()

router = Router()


@router.message(F.text == "Задачи")
async def task(message: Message):
    await message.answer("У вас на сегодня нет задач", reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Создать задачу", callback_data="addtask")]
        ]
    ))

@router.callback_query(StateFilter(None), F.data == "addtask")
async def create_task(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите название задачи")
    await state.set_state(AddTask.choosing_task_name)


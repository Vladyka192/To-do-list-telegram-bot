from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.user import UserRepo
from repositories.task import TaskRepo

from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

class AddTask(StatesGroup):
    choosing_task_name = State()
    choosing_task_description = State()
    choosing_task_priority = State()
    choosing_task_date = State()
    choosing_task_time = State()
    task_submit = State()

router = Router()

@router.message(Command("create_task"))
async def create_by_command(message: Message, state: FSMContext):
    await create_task(message, state)

@router.message(F.text == "Создать задачу")
async def create_by_button(message: Message, state: FSMContext):
    await create_task(message, state)

async def create_task(message: Message, state: FSMContext):
    await message.answer("Напишите название задачи")
    await state.set_state(AddTask.choosing_task_name)

@router.callback_query(StateFilter(None), F.data == "addtask")
async def create_task_by_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Напишите название задачи")
    await state.set_state(AddTask.choosing_task_name)

@router.message(StateFilter(AddTask.choosing_task_name))
async def take_task_name(message: Message, state: FSMContext):
    await state.update_data(task_name=message.text)
    await message.answer("Введите описание")
    await state.set_state(AddTask.choosing_task_description)

@router.message(StateFilter(AddTask.choosing_task_description))
async def take_description_name(message: Message, state: FSMContext):
    await state.update_data(task_description=message.text)
    await message.answer("Выберите приоритет:\n 1- низкий\n 2 - средний\n 3 - высокий\n")
    await state.set_state(AddTask.choosing_task_priority)

@router.message(StateFilter(AddTask.choosing_task_priority))
async def take_priority(message: Message, state: FSMContext):
    try:
        priority = int(message.text)
        if(priority < 4 and priority > 0):
            await state.update_data(task_priority=priority)
        else:
            await message.answer("Введите число 1,2,3")
            return
    except ValueError:
        await message.answer("Введите число 1,2,3")
        return
    await message.answer("Напишите дату, когда нужно будет начать")
    await state.set_state(AddTask.choosing_task_date)

@router.message(StateFilter(AddTask.choosing_task_date))
async def take_date(message: Message, state: FSMContext):
    try:
        date = datetime.strptime(message.text, "%d.%m.%Y").date()
        await state.update_data(task_date=date)
    except ValueError:
        await message.answer("Введите дату в формате ДД.ММ.ГГГГ\nНапример: 15.08.2026")
        return
    await message.answer("Напишите время, когда нужно выполнить")
    await state.set_state(AddTask.choosing_task_time)

@router.message(StateFilter(AddTask.choosing_task_time))
async def take_time(message: Message, state: FSMContext, user_repo: UserRepo, task_repo: TaskRepo):
    try:
        time = datetime.strptime(message.text, "%H:%M").time()
        await state.update_data(task_time=time)
    except ValueError:
        await message.answer("Введите время в формате ЧЧ:ММ\nНапример: 16:50")
        return
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните /start")
        return
    data = await state.get_data()
    await task_repo.create_task(user.id, data["task_name"], data["task_description"], "active", data["task_priority"], data["task_date"], data["task_time"])
    await message.answer("Задача создана!")
    await state.clear()
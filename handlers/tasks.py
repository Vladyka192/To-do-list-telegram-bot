from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message

from repositories.user import UserRepo
from repositories.task import TaskRepo

import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

router = Router()

@router.message(Command("tasks"))
async def checktasks_by_command(message: Message, user_repo: UserRepo, task_repo: TaskRepo):
    await get_tasks(message, user_repo, task_repo)

@router.message(F.text == "Просмотреть задачи")
async def checktasks_by_button(message: Message, user_repo: UserRepo, task_repo: TaskRepo):
    await get_tasks(message, user_repo, task_repo)

async def get_tasks(message: Message, user_repo: UserRepo, task_repo: TaskRepo):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните /start")
        return
    tasks = await task_repo.get_user_tasks(user.id)
    if not tasks:
        await message.answer("У вас пока нет задач", reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Создать задачу", callback_data="addtask")]
        ]
    ))
        return
    else:
        status_names = {
            "active": "Активная",
            "completed": "Выполненная",
            "cancelled": "Отмененная"
        }
        result = ""
        for count, task in enumerate(tasks, start=1):
            task_status = status_names[task.status]
            result += f"{count}) {task.title} - {task_status}\n"
        await message.answer(result)
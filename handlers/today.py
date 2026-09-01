from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from repositories.user import UserRepo
from repositories.task import TaskRepo

from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

router = Router()

@router.message(Command("today"))
async def get_tasks(message: Message, user_repo: UserRepo, task_repo: TaskRepo):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните /start")
        return
    tasks = await task_repo.get_tasks_for_date(user.id, datetime.today().date())
    if not tasks:
        await message.answer("У вас пока нет задач")
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
            result += f"{count}) {task.title} - {task_status}"
        await message.answer(result)
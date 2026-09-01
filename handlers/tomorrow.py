from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from repositories.user import UserRepo
from repositories.task import TaskRepo

from datetime import date, timedelta

router = Router()

@router.message(Command("tomorrow"))
async def get_tasks(message: Message, user_repo: UserRepo, task_repo: TaskRepo):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните /start")
        return
    tomorrow = date.today() + timedelta(days=1)
    tasks = await task_repo.get_tasks_for_date(user.id, tomorrow)
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
            result += f"{count}) {task.title} - {task_status}\n"
        await message.answer(result)
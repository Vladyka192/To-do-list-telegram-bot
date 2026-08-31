from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from repositories.user import UserRepo
from repositories.task import TaskRepo

from datetime import datetime
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

router = Router()

@router.message(Command("tasks"))
async def get_tasks(message: Message, user_repo: UserRepo, task_repo: TaskRepo):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните /start")
        return
    tasks = await task_repo.get_user_tasks(user.id)
    if not tasks:
        await message.answer("У вас пока нет задач")
        return
    else:
        priority_names = {
            1: "Низкий",
            2: "Важный",
            3: "Срочный"
        }
        status_names = {
            "active": "Активная",
            "completed": "Выполненная",
            "cancelled": "Отмененная"
        }
        result = ""
        for count, task in enumerate(tasks, start=1):
            task_priority = priority_names[task.priority]
            task_status = status_names[task.status]

            result += f"{count}) {task.title}\nСтатус: {task_status}\nОписание: {task.description}\nПриоритет: {task_priority}\nДедлайн задачи: {task.due_date:%d %B} {task.due_time}\n "
        await message.answer(result)
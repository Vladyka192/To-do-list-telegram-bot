from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from datetime import datetime

from repositories.user import UserRepo
from repositories.task import TaskRepo
from repositories.reminder import RemindRepo

router = Router()

@router.message(Command("search"))
async def remind_task(message: Message, command: CommandObject, task_repo: TaskRepo, user_repo: UserRepo):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)

    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return
    tasks = await task_repo.get_user_tasks(user.id)
    
    if not tasks:
        await message.answer("У вас пока нет задач")
        return


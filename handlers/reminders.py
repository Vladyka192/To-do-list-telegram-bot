from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from repositories.user import UserRepo
from repositories.task import TaskRepo
from repositories.reminder import RemindRepo

router = Router()

@router.message(Command("reminders"))
async def get_reminders(message: Message, user_repo: UserRepo, task_repo: TaskRepo, remind_repo: RemindRepo):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните /start")
        return
    reminds = await remind_repo.get_users_reminders(user.id)
    result = ""
    for reminder, task in reminds:
        result += f"Задача: {task.title} напомнить в {reminder.remind_at}\n"

    if not result:
        await message.answer("У вас нет напоминаний")
        return

    await message.answer(result)

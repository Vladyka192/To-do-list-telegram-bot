from aiogram import Router
from aiogram.types import Message

from nlp.parser import parse_message

from repositories.task import TaskRepo
from repositories.user import UserRepo

router = Router()

@router.message()
async def take_message(message: Message, task_repo: TaskRepo, user_repo: UserRepo):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните /start")
        return
    parsed_task = parse_message(message.text)
    await task_repo.create_task(user.id, parsed_task.title, None, "active", parsed_task.priority, parsed_task.date, parsed_task.time)
    await message.answer("Задача создана!")
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from repositories.user import UserRepo
from repositories.task import TaskRepo

router = Router()

@router.message(Command("search"))
async def search_task(message: Message, command: CommandObject, task_repo: TaskRepo, user_repo: UserRepo):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните команду /start")

    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return

    results = await task_repo.search_task(user.id, command.args)
    for result in results:
        await message.answer(f"{result.id}) {result.title}\n")
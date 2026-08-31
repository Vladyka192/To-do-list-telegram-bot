from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from repositories.user import UserRepo
from repositories.task import TaskRepo

router = Router()

@router.message(Command("task"))
async def get_task(message: Message, user_repo: UserRepo, task_repo: TaskRepo, command: CommandObject):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните /start")
        return
    task = await task_repo.get_user_tasks(user.id)

    if not task:
        await message.answer("У вас пока нет задач")
        return
    try:
        task_number = int(command.args)
    except ValueError:
        await message.answer("Ошибка: неправильный формат команды. Пример:\n"
                             "/add <number_of_task>"
                             )
        return
    try:
        if task_number < 1:
            await message.answer("Номер задачи быть больше 0")
            return
        else:
            task = task[task_number - 1]
    except IndexError:
        await message.answer("Ошибка: задач меньше, чем в аргументе. Введите правильный id задачи")
        return
    await 
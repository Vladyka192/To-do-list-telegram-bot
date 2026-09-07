from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from repositories.user import UserRepo
from repositories.task import TaskRepo

router = Router()

@router.meesage(Command("complete"))
async def complete_task(message: Message, task_repo: TaskRepo, user_repo: UserRepo, command: CommandObject):
    user = user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните команду /start")
        return

    tasks = task_repo.get_user_tasks(user.id)
    if not tasks:
        await message.answer("У вас пока нет задач")
        return
    try:
        task_number = int(command.args)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/complete <number_of_task>"
        )
        return
    try:
        if task_number < 1:
            await message.answer("Номер задачи должен быть больше 0")
            return
        else:
            task = tasks[task_number - 1]
    except IndexError:
        await message.answer("Ошибка: задач меньше, чем в аргументе. Введите правильный id задачи")
        return
    await task_repo.complete_task(task.id, user.id)
    await message.answer(f"Задача {task.title} выполнена!")



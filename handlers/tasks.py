from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from repositories.task import TaskRepo

router = Router()

@router.message(Command("tasks"))
async def get_tasks(message: Message, task_repo: TaskRepo):
    tasks = await task_repo.get_user_tasks(message.from_user.id)
    if not tasks:
        await message.answer("У вас пока нет задач")
    else:
        result = ""
        for count, task in enumerate(tasks, start=1):
            result += f"{count}) {task.title}\n"
        await message.answer(result)
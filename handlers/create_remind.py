from aiogram import Router
from aiogram.filters import StateFilter, Command, CommandObject
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from datetime import datetime

from repositories.user import UserRepo
from repositories.task import TaskRepo
from repositories.reminder import RemindRepo

class CreateReminder(StatesGroup):
    remind_time = State()

router = Router()

@router.message(Command("remind"))
async def remind_task(message: Message, command: CommandObject, task_repo: TaskRepo, user_repo: UserRepo, state: FSMContext):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)

    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return
    tasks = await task_repo.get_user_tasks(user.id)
    
    if not tasks:
        await message.answer("У вас пока нет задач")
        return
    try:
        task_number = int(command.args)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/remind <number_of_task>"
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
    
    await state.update_data(task_id=task.id)
    await message.answer("Во сколько вы хотите добавить напоминание?")
    await state.set_state(CreateReminder.remind_time)

@router.message(StateFilter(CreateReminder.remind_time))
async def take_remind_time(message: Message, state: FSMContext, remind_repo: RemindRepo):
    try:
        remind_time = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer("Введите дату и время в формате: ДД.ММ.ГГГГ ЧЧ:ММ.\nНапример: 15.08.2026 16:50")
        return

    if remind_time <= datetime.now():
        await message.answer("Нельзя создать напоминание в прошлом\n\n"
                             "Введите будущую дату и время")
        return

    data = await state.get_data()
    await remind_repo.create_reminder(data["task_id"], remind_time)
    await message.answer("Напоминание создано!")
    await state.clear()
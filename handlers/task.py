from aiogram import Router, F
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from repositories.user import UserRepo
from repositories.task import TaskRepo

from keyboards.choice import choice_menu_kb
from keyboards.choice import edit_task_kb

from handlers.edit import EditTask
router = Router()

@router.message(Command("task"))
async def get_task(message: Message, user_repo: UserRepo, task_repo: TaskRepo, command: CommandObject, state: FSMContext):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните /start")
        return
    tasks = await task_repo.get_user_tasks(user.id)

    if not tasks:
        await message.answer("У вас пока нет задач")
        return
    try:
        task_number = int(command.args)
    except TypeError:
        await message.answer("Ошибка: неправильный формат команды. Пример:\n"
                             "/task <number_of_task>"
                             )
        return
    try:
        if task_number < 1:
            await message.answer("Номер задачи быть больше 0")
            return
        else:
            task = tasks[task_number - 1]
    except IndexError:
        await message.answer("Ошибка: задач меньше, чем в аргументе. Введите правильный id задачи")
        return
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
    
    task_priority = priority_names[task.priority]
    task_status = status_names[task.status]
    await message.answer(f"{task_number}) {task.title}\nСтатус: {task_status}\n"
                         f"Описание: {task.description}\nПриоритет: {task_priority}\n"
                         f"Дедлайн задачи: {task.due_date:%d %B} {task.due_time}\n", reply_markup=edit_task_kb(task.id))

@router.callback_query(F.data.startswith("delete_task:"))
async def delete_task(callback: CallbackQuery, user_repo: UserRepo, task_repo: TaskRepo):
    task_id = int(callback.data.split(":")[1])
    user = await user_repo.get_user_by_tg_id(callback.from_user.id)
    await task_repo.delete_task(task_id, user.id)
    await callback.answer()
    await callback.message.answer("Задача успешно удалена")


@router.callback_query(F.data.startswith("edit_task:"))
async def edit_task(callback: CallbackQuery, user_repo: UserRepo, state: FSMContext):
    task_id = int(callback.data.split(":")[1])
    user = await user_repo.get_user_by_tg_id(callback.from_user.id)
    await state.update_data(task_id = task_id, user_id=user.id)
    await callback.message.answer("Что вы хотите изменить?", reply_markup=choice_menu_kb())
    await state.set_state(EditTask.edit_message)
    await callback.answer()
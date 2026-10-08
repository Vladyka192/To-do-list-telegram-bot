from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.user import UserRepo
from repositories.task import TaskRepo

from datetime import datetime

from keyboards.choice import choice_menu_kb
from keyboards.menu import main_menu_kb

class EditTask(StatesGroup):
    edit_message = State()
    change_value = State()

router = Router()

@router.message(Command("edit"))
async def edit_task(message: Message, command: CommandObject, user_repo: UserRepo, task_repo: TaskRepo, state: FSMContext):
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
            "/edit <number_of_task>"
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

    await state.update_data(task_id = task.id)
    await state.update_data(user_id = user.id)

    await message.answer(f"Вы выбрали:\nНазвание: {task.title}\nСтатус: {task.status}\n"
                         f"Описание: {task.description}\nПриоритет: {task.priority}\n"
                         f"Дедлайн задачи: {task.due_date:%d %B} {task.due_time}\n")
    await message.answer(f"Что вы хотите в ней изменить?", reply_markup=choice_menu_kb())
    await state.set_state(EditTask.edit_message)

@router.message(StateFilter(EditTask.edit_message))
async def get_task_message(message: Message, state: FSMContext):
    if(message.text == "Название"):
        await message.answer("Какое новое название вы хотите поставить?")
        await state.update_data(edit_field="title")
    elif(message.text == "Статус"):
        await message.answer("Какой новое состояние вы хотите поставить?")
        await state.update_data(edit_field="status")
    elif(message.text == "Описание"):
        await message.answer("Какое новое описание вы хотите поставить?")
        await state.update_data(edit_field="description")
    elif(message.text == "Приоритет"):
        await message.answer("Какой новый приоритет вы хотите поставить?")
        await state.update_data(edit_field="priority")
    elif(message.text == "Дата"):
        await message.answer("Какую новую дату вы хотите поставить?")
        await state.update_data(edit_field="due_date")
    elif(message.text == "Время"):
        await message.answer("Какое новое время вы хотите поставить?")
        await state.update_data(edit_field="due_time")
    elif(message.text == "Назад"):
        await state.clear()
        await message.answer("Редактирование отменено", reply_markup=main_menu_kb())
        return
    else:
        await message.answer("Неизвестный аргумент. Напишите, что именно: Название, Описание, Приоритет, Дату, Время, Статус")
        return

    await state.set_state(EditTask.change_value)

@router.message(StateFilter(EditTask.change_value))
async def edit_task_value(message: Message, state: FSMContext, task_repo: TaskRepo):
    data = await state.get_data()
    field = data["edit_field"]
    if(field == "title" or field == "description"):
        value = message.text
    elif(field == "status"):
        if message.text != "active" and message.text != "completed" and message.text != "cancelled":
            await message.answer("Введите статус active, completed, cancelled")
            return
        value = message.text
    elif(field == "priority"):
        try:
            value = int(message.text)
            if value not in (1, 2, 3):
                await message.answer("Введите число 1, 2, 3")
                return
        except ValueError:
            await message.answer("Введите число 1, 2, 3")
            return
    elif(field == "due_date"):
        try:
            value = datetime.strptime(message.text, "%d.%m.%Y").date()
        except ValueError:
            await message.answer("Введите дату в формате ДД.ММ.ГГГГ\nНапример: 15.08.2026")
            return
    elif(field == "due_time"):
        try:
            value = datetime.strptime(message.text, "%H:%M").time()
        except ValueError:
            await message.answer("Введите время в формате ЧЧ:ММ\nНапример: 16:50")
            return
    else:
        return

    await task_repo.update_task(data["task_id"], data["user_id"], data["edit_field"], value)
    await message.answer("Данные успешно обновлены!", reply_markup=main_menu_kb())
    await state.clear()

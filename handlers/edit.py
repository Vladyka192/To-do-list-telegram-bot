from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from repositories.user import UserRepo
from repositories.task import TaskRepo

from datetime import datetime

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

    await message.answer(f"Вы выбрали:\nНазвание: {task.title}")
    await message.answer(f"Что вы хотите в ней изменить?")
    await state.set_state(EditTask.edit_message)

@router.message(StateFilter(EditTask.edit_message))
async def get_task_message(message: Message, state: FSMContext):
    if(message.text == "Название"):
        await message.answer("Какое новое название вы хотите поставить?")
        await state.update_data(edit_field="title")
    elif(message.text == "Описание"):
        await message.answer("Какое новое описание вы хотите поставить?")
        await state.update_data(edit_field="description")
    elif(message.text == "Приоритет"):
        await message.answer("Какой новый приоритет вы хотите поставить?")
        await state.update_data(edit_field="priority")
    elif(message.text == "Дату"):
        await message.answer("Какую новую дату вы хотите поставить?")
        await state.update_data(edit_field="due_date")
    elif(message.text == "Время"):
        await message.answer("Какое новое время вы хотите поставить?")
        await state.update_data(edit_field="due_time")
    elif(message.text == "Состояние"):
        await message.answer("Какой новое состояние вы хотите поставить?")
        await state.update_data(edit_field="status")
    else:
        await message.answer("Неизвестный аргумент. Напишите, что именно: Название, Описание, Приоритет, Дату, Время, Состояние.")
        return

    await state.set_state(EditTask.change_value)

@router.message(StateFilter(EditTask.change_value))
async def edit_task_value(message: Message, state: FSMContext, task_repo: TaskRepo):
    data = await state.get_data()
    field = data["edit_field"]
    if(field == "title" and field == "description"):
        text_information = message.text
    elif(field == "priority"):
        try:
            text_information = int(message.text)
            if(text_information < 4 and text_information > 0):
                pass
            else:
                await message.answer("Введите число 1, 2, 3")
                return
        except ValueError:
            await message.answer("Введите число 1, 2, 3")
            return
    elif(field == "due_data"):
        try:
            text_information = datetime.strptime(message.text, "%H:%M").date()
        except ValueError:
            await message.answer("Введите время в формате ЧЧ:ММ\nНапример: 16:50")
            return
    elif(field == "due_time"):
        try:
            text_information = datetime.strptime(message.text, "%H:%M").time()
        except ValueError:
            await message.answer("Введите время в формате ЧЧ:ММ\nНапример: 16:50")
            return

    await task_repo.update_task(data["task_id"], data["user_id"], data["edit_field"], text_information)
    await message.answer("Данные успешно обновлены!")

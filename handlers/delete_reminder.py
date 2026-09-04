from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from repositories.reminder import RemindRepo
from repositories.user import UserRepo

router = Router()

@router.message(Command("delreminder"))
async def delete_reminder(message: Message, command: CommandObject, user_repo: UserRepo, remind_repo: RemindRepo):
    user = await user_repo.get_user_by_tg_id(message.from_user.id)
    if not user:
        await message.answer("Сначала выполните /start")
        return

    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return
    
    reminders = await remind_repo.get_user_reminders(user.id)
    
    if not reminders:
        await message.answer("У вас пока нет напоминаний")
        return
    try:
        reminder_number = int(command.args)
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/delreminders <number_of_task>"
        )
        return
    try:
        if reminder_number < 1:
            await message.answer("Номер задачи должен быть больше 0")
            return
        else:
            reminder, task = reminders[reminder_number - 1]
    except IndexError:
        await message.answer("Ошибка: задач меньше, чем в аргументе. Введите правильный id задачи")
        return
    await remind_repo.delete_reminder(reminder.id, user.id)
    await message.answer(f"Напоминание {task.title} в {reminder.remind_at} удалено!")
from aiogram import Bot
from repositories.reminder import RemindRepo
from repositories.task import TaskRepo

async def check_reminders(bot: Bot, session_factory):
    async with session_factory() as session:
        reminder_repo = RemindRepo(session)
        reminders = await reminder_repo.get_due_reminders()

        for reminder, task, user in reminders:
            try:
                await bot.send_message(chat_id=user.tg_id, text=f"Напоминие\n\n{task.title}")
                await reminder_repo.mark_as_completed(reminder.id)
            except Exception as error:
                print(f"Ошибка отправки напоминания {reminder.id}\n Ошибка: {error}")
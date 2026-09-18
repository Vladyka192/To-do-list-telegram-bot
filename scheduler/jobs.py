from aiogram import Bot
from repositories.reminder import RemindRepo
from repositories.recurrence_rule import RecurrenceRule
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

async def check_recurrence_rules(bot: Bot, session_factory, task_repo: TaskRepo, remind_repo: RemindRepo):
    async with session_factory() as session:
        recurrence_rule_repo = RecurrenceRule(session)
        recurrence_rules = await recurrence_rule_repo.get_next_run()

        for recurrence_rule, task, user in recurrence_rules:
            try:
                await task_repo.create_task(user.id, task.title, task.descriptin, task.status, task.priority, task.due_date, task.due_time)
                await remind_repo.create_reminder(task.id, recurrence_rule.start_at)
            except Exception as error:
                print(f"Ошибка отправки напоминани")
from datetime import date, time, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.reminder import Reminder
from database.models.user import User
from database.models.task import Task

class RemindRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def create_reminder(self, task_id: int, remind_time: datetime):
        reminder = Reminder(task_id=task_id, remind_at=remind_time)
        self.__session.add(reminder)
        await self.__session.commit()
        await self.__session.refresh(reminder)

    async def get_due_reminders(self):
        query = (select(Reminder, Task, User)
                 .join(Task, Reminder.task_id == Task.id)
                 .join(User, Task.user_id == User.id)
                 .where(Reminder.remind_at <= datetime.now(),
                        Reminder.is_sent == False
                        )
                        )

        result = await self.__session.execute(query)

        return result.all()

    async def mark_as_completed(self, remind_id: int):
        statement = select(Reminder).where(Reminder.id==remind_id)
        remind = await self.__session.scalar(statement)

        setattr(remind, "is_sent", True)
        await self.__session.commit()

    async def get_users_reminders(self, user_id: int):
        statement = (select(Reminder, Task)
                     .join(Task, Reminder.task_id == Task.id)
                     .where(Task.user_id == user_id, Reminder.is_sent == False)
                     .order_by(Reminder.remind_at))
        result = await self.__session.execute(statement)
        return result.all()

    async def delete_reminder(self, user_id: int):
        statement = (select(Reminder, Task)
                .join(Task, Reminder.task_id == Task.id)
                .where(Task.user_id == user_id, Reminder.is_sent == False)
                .order_by(Reminder.remind_at))

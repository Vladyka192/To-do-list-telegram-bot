from datetime import date, time, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.recurrence_rule import RecurrenceRule
from database.models.reminder import Reminder
from database.models.user import User
from database.models.task import Task

class RecurrenceRule:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_next_run(self):
        query = (select(Recurrence_rule, Task, User)
            .join(Task, Recurrence_rule.task_id == Task.id)
            .join(User, Recurrence_rule.user_id == User.id)
            .where(Recurrence_rule.next_run_at <= datetime.now(), is_active=True)
            )

        result = await self.__session.execute(query)

        return result.all()
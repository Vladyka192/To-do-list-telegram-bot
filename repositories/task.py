from datetime import date, time, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.task import Task

class TaskRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_user_tasks(self, user_id: int):
        statement = select(Task).where(Task.user_id == user_id)
        tasks = await self.__session.scalars(statement)
        return tasks.all()

    async def get_tasks_for_date(self, user_id: int, task_date: date):
        statement = select(Task).where(Task.user_id == user_id, Task.due_date == task_date)
        tasks = await self.__session.scalars(statement)
        return tasks.all()
    
    async def create_task(self, user_id: int, title: str, description: str | None , status: str, priority: int, due_date: date, due_time: time):
        task = Task(user_id=user_id, title=title, description=description, status=status, priority=priority, due_date=due_date, due_time=due_time)
        self.__session.add(task)
        await self.__session.commit()

    async def delete_task(self, task_id: int, user_id: int):
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = await self.__session.scalar(statement)

        if not task:
            return

        await self.__session.delete(task)
        await self.__session.commit()

    async def update_task(self, task_id: int, user_id: int, field: str, value):
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = await self.__session.scalar(statement)

        if not task:
            return

        setattr(task, field, value)
        await self.__session.commit()


        
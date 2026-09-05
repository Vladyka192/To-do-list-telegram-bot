from typing import Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from repositories.user import UserRepo
from repositories.task import TaskRepo
from repositories.reminder import RemindRepo
from repositories.recurrence_rule import RecurrenceRule

class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker) -> None:
        self.session_maker = session_maker

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: dict[str, Any]
    ) -> Any:
        async with self.session_maker() as session:
            data["user_repo"] = UserRepo(session=session)
            data["task_repo"] = TaskRepo(session=session)
            data["remind_repo"] = RemindRepo(session=session)
            data["recurrence_rule"] = RecurrenceRule(session=session)
            return await handler(event, data)
from aiogram import BaseMiddleware
from typing import Any, Callable, Dict
from collections.abc import Awaitable
from aiogram.types import Message

from repositories.user import UserRepo
from repositories.task import TaskRepo
from repositories.reminder import RemindRepo

class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, session_maker) -> None:
        self.session_maker = session_maker

    async def __call__(
        self, 
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], 
        event: Message, 
        data: Dict[str, any]
    ) -> Any:
        async with self.session_maker() as session:
            data["user_repo"] = UserRepo(session=session)
            data["task_repo"] = TaskRepo(session=session)
            data["remind_repo"] = RemindRepo(session=session)
            return await handler(event, data)
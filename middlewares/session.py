from aiogram import BaseMiddleware
from typing import Any, Callable, Dict
from collections.abc import Awaitable
from aiogram.types import Message

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
            data["session"] = session
            return await handler(event, data)
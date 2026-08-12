from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import User

class UserRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_user_by_tg_id(self, tg_id: int):
        statement = select(User).where(User.tg_id == tg_id)
        return await self.__session.scalar(statement)

    async def create_or_update_user(self, tg_id: int, fullname: str, username: str, timezone: str):
        user = await self.get_user_by_tg_id(tg_id)

        if not user:
            await self.create_user(tg_id, fullname, username, timezone)
        else:
            user.fullname = fullname
            user.username = username
            user.timezone = timezone

        await self.__session.commit()

    async def create_user(self, tg_id: int, fullname: str, username: str, timezone: str):
        user = User(tg_id=tg_id, username=username, fullname=fullname, timezone=timezone)
        self.__session.add(user)

    
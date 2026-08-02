import asyncio
from aiogram import Bot, Dispatcher

from middlewares import register_middlewares
from handlers import register_routes
from database.models import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
TOKEN = "8968451956:AAFdo-SP_mE9ajS1UX5lqypWk5UmhFSrkF8"


async def init_model(engine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all) # alembic

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    engine = create_async_engine(
        url="sqlite+aiosqlite:///notes.db"
    )
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    register_middlewares(dp, session_maker)

    register_routes(dp)

    await init_model(engine)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
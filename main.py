import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from middlewares import register_middlewares
from handlers import register_routes

from database.models import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from scheduler.scheduler import setup_scheduler

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def init_model(engine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all) # alembic

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    engine = create_async_engine(
        url=os.getenv("PG_LINK")
    )
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    await init_model(engine)

    register_middlewares(dp, session_maker)
    register_routes(dp)

    scheduler = setup_scheduler(bot=bot, session_factory=session_maker)
    scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await bot.seesion.close()
        await engine.dispose()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
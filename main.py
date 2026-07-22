import asyncio
from aiogram import Bot, Dispatcher

from handlers import register_routes

TOKEN = "8968451956:AAFdo-SP_mE9ajS1UX5lqypWk5UmhFSrkF8"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    register_routes(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
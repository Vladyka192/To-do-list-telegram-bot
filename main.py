import asyncio
from aiogram import Bot, Dispatcher, Router

TOKEN = "8968451956:AAFdo-SP_mE9ajS1UX5lqypWk5UmhFSrkF8"
router = Router()

@router.message()
async def start(message):
    await message.answer("Привет")

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
from aiogram import Dispatcher

from handlers.start import router as start_message
from handlers.help import router as help_message
from handlers.tasks import router as task_info

def register_routes(dp: Dispatcher):
    dp.include_router(start_message)
    dp.include_router(help_message)
    dp.include_router(task_info)
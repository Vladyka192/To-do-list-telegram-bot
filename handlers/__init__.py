from aiogram import Dispatcher

from handlers.start import router as start_message
from handlers.settings import router as settings
from handlers.help import router as help_message
from handlers.tasks import router as tasks_info
from handlers.task import router as task
from handlers.today import router as today_tasks
from handlers.add_task import router as create_task
from handlers.delete import router as delete_task
from handlers.edit import router as edit_task
from handlers.check_tasks import router as check_task

def register_routes(dp: Dispatcher):
    dp.include_router(start_message)
    dp.include_router(settings)
    dp.include_router(help_message)
    dp.include_router(tasks_info)
    dp.include_router(task)
    dp.include_router(today_tasks)
    dp.include_router(create_task)
    dp.include_router(delete_task)
    dp.include_router(edit_task)
    dp.include_router(check_task)
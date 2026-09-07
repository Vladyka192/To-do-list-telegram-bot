from aiogram import Dispatcher

from handlers.start import router as start_message
from handlers.settings import router as settings
from handlers.help import router as help_message
from handlers.tasks import router as tasks
from handlers.task import router as task
from handlers.today import router as today_tasks
from handlers.tomorrow import router as tomorrow_tasks
from handlers.complete import router as complete_task
from handlers.add_task import router as create_task
from handlers.delete import router as delete_task
from handlers.edit import router as edit_task
from handlers.task_history import router as task_history
from handlers.search import router as search_task
from handlers.create_remind import router as create_reminder
from handlers.reminders import router as reminders
from handlers.delete_reminder import router as delete_reminder
from handlers.check_tasks import router as check_task

def register_routes(dp: Dispatcher):
    dp.include_router(start_message)
    dp.include_router(settings)
    dp.include_router(help_message)
    dp.include_router(tasks)
    dp.include_router(task)
    dp.include_router(today_tasks)
    dp.include_router(tomorrow_tasks)
    dp.include_router(complete_task)
    dp.include_router(create_task)
    dp.include_router(delete_task)
    dp.include_router(edit_task)
    dp.include_router(task_history)
    dp.include_router(search_task)
    dp.include_router(create_reminder)
    dp.include_router(reminders)
    dp.include_router(delete_reminder)
    dp.include_router(check_task)
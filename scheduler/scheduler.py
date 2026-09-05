from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scheduler import jobs

def setup_scheduler(bot, session_factory):
    scheduler = AsyncIOScheduler(timezone="Asia/Almaty")
    scheduler.add_job(jobs.check_reminders, trigger='interval', seconds=60, args=[bot, session_factory], id="check_reminders", replace_existing=True)
    scheduler.add_job(jobs.check_recurrence_rules, trigger='interval', seconds=60, args=[bot, session_factory], id="check_recurrence_rules", replace_existiong=True)

    return scheduler
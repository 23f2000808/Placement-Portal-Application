import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "placement_portal",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=[
        "tasks.reminder_tasks",
        "tasks.report_tasks",
        "tasks.export_tasks"
    ]
)


celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
    beat_schedule={
        "close-expired-drives": {
            "task": "tasks.reminder_tasks.close_expired_drives",
            "schedule": crontab(hour=0, minute=0),
        },
        "daily-reminders": {
            "task": "tasks.reminder_tasks.send_deadline_reminders",
            "schedule": crontab(hour=8, minute=0),
        },
        "monthly-report": {
            "task": "tasks.report_tasks.generate_monthly_report",
            "schedule": crontab(day_of_month=1, hour=0, minute=5),
        },
    }
)


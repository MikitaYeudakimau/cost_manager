import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

app = Celery("src")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_email_every_morning_9_am': {
        'task': 'manager.tasks.send_email_report',
        'schedule': crontab(hour=9),
    },
}

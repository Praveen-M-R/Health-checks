## start --> celery beat scheduler 
 celery -A healthcheck beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

## start worker
celery -A healthcheck worker --loglevel=info

## 👉 Restart Celery Worker:
celery -A healthcheck worker --loglevel=info

## 👉 Restart Celery Beat:
celery -A healthcheck beat --loglevel=info

## scheduler

python manage.py shell

from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

# Create a schedule to run every 1 minute
schedule, created = IntervalSchedule.objects.get_or_create(
    every=1, period=IntervalSchedule.MINUTES
)

# Create the periodic task
PeriodicTask.objects.create(
    interval=schedule,
    name="Check for Missing Pings",
    task="checks.tasks.check_missing_pings",
    args=json.dumps([]),
)

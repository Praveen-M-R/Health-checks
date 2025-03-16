from django.contrib import admin
from .models import Check, CheckLog
from django.contrib import admin
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from .models import Check, FailedCheck

admin.site.register(Check)
admin.site.register(CheckLog)
admin.site.register(FailedCheck)

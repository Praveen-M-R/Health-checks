from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
import uuid

class Check(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    duration_days = models.PositiveIntegerField(default=0)
    duration_hours = models.PositiveIntegerField(default=0)
    duration_minutes = models.PositiveIntegerField(default=0)  # Default 5 minutes
    
    grace_days = models.PositiveIntegerField(default=0)
    grace_hours = models.PositiveIntegerField(default=0)
    grace_minutes = models.PositiveIntegerField(default=0)  # Default 5 minutes
    
    ping_url = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    channel = models.CharField(max_length=100, blank=True, null=True)  # Notification method
    recipient = models.EmailField(blank=True, null=True)  # Email for notifications
    
    last_ping = models.DateTimeField(null=True, blank=True)
    is_up = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CheckLog(models.Model):
    check_name = models.ForeignKey(Check, on_delete=models.CASCADE, related_name="logs")
    status = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

class FailedCheck(models.Model):
    check_name = models.ForeignKey(Check, on_delete=models.CASCADE, related_name="failed_attempts")
    failed_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)  # To track if notification was sent

    def __str__(self):
        return f"Failed: {self.check.name} at {self.failed_at}"
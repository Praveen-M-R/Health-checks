from celery import shared_task
from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from .models import Check, FailedCheck, CheckLog

@shared_task
def check_missing_pings():
    """Check for overdue pings and send email notifications."""
    current_time = now()
    checks = Check.objects.filter(is_up=True)  # Only check active ones

    for check in checks:
        # Calculate when the last ping was expected
        expected_ping_time = check.last_ping + timedelta(
            days=check.duration_days,
            hours=check.duration_hours,
            minutes=check.duration_minutes,
        ) if check.last_ping else check.created_at

        # Add grace period
        grace_period = timedelta(
            days=check.grace_days,
            minutes=check.grace_minutes,
        )

        # If expected time + grace period has passed, mark as failed
        if current_time > (expected_ping_time + grace_period):
            # If not already marked as failed, save and send email
            if not FailedCheck.objects.filter(check_name=check, email_sent=False).exists():
                failed_check = FailedCheck.objects.create(check_name=check)

                # Send email
                send_alert_email(check)
                
                # Mark check as DOWN
                check.is_up = False
                check.save()
                CheckLog.objects.create(check_name=check, status=False)
                # Update failure record
                failed_check.email_sent = True
                failed_check.save()

def send_alert_email(check):
    """Send email notification for failed checks."""
    if check.recipient:
        subject = f"🚨 ALERT: {check.name} is DOWN!"
        message = f"""
        The check '{check.name}' has missed its expected ping.

        Expected every: {check.duration_days} days, {check.duration_hours} hours, {check.duration_minutes} mins
        Grace period: {check.grace_days} days, {check.grace_minutes} mins
        Last Ping: {check.last_ping or 'Never'}

        Please check your service.
        """
        send_mail(subject, message, "p4413020@gmail.com", [check.recipient])

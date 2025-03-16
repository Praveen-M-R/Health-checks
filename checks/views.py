from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.timezone import now
from django.db.models import Count

from datetime import timedelta
from .models import Check, CheckLog, FailedCheck
from .forms import CheckForm


def welcome(request):
    return render(request, 'checks/welcome.html')


def register(request):
    """Handles user registration"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "checks/register.html", {"form": form})


def logout_view(request):
    """Logs out the user"""
    logout(request)
    return redirect('welcome')


def get_user_statistics(user):
    """Compute statistics for a user's checks."""
    total_checks = Check.objects.filter(created_by=user).count()
    active_checks = Check.objects.filter(created_by=user, is_up=True).count()
    failed_checks = Check.objects.filter(created_by=user, is_up=False).count()
    
    last_failed_check = (
        FailedCheck.objects.filter(check_name__created_by=user)
        .order_by("-failed_at")
        .first()
    )

    return {
        "total_checks": total_checks,
        "active_checks": active_checks,
        "failed_checks": failed_checks,
        "last_failed_check": last_failed_check.failed_at if last_failed_check else None,
    }


@login_required
def dashboard(request):
    """User dashboard displaying checks and statistics"""
    checks = Check.objects.filter(created_by=request.user)
    stats = get_user_statistics(request.user)
    
    return render(request, "checks/dashboard.html", {
        "checks": checks,
        "stats": stats
    })


@login_required
def create_check(request):
    """Handles check creation"""
    form = CheckForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        check = form.save(commit=False)
        check.created_by = request.user
        check.created_at = now()
        check.save()
        return redirect("dashboard")
    
    return render(request, "checks/create_check.html", {"form": form})


@login_required
def check_logs(request, check_id):
    """View logs of a specific check"""
    check = get_object_or_404(Check, id=check_id, created_by=request.user)
    logs = check.logs.all()
    return render(request, "checks/logs.html", {"check": check, "logs": logs})


@login_required
def check_detail(request, check_id):
    """Detailed view of a check including logs and stats"""
    check = get_object_or_404(Check, id=check_id, created_by=request.user)
    logs = check.logs.all()

    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    def get_status_counts(start_date):
        return (
            CheckLog.objects.filter(check_name=check, timestamp__date__gte=start_date)
            .values('status')
            .annotate(count=Count('status'))
        )

    stats = {
        "today": get_status_counts(today),
        "this_week": get_status_counts(start_of_week),
        "this_month": get_status_counts(start_of_month),
        "this_year": get_status_counts(start_of_year),
    }

    return render(request, "checks/check_detail.html", {
        "check": check,
        "logs": logs,
        "stats": stats
    })


def ping_check(request, ping_uuid):
    """Handles receiving a ping for a check"""
    check = get_object_or_404(Check, ping_url=ping_uuid)
    check.last_ping = now()
    check.is_up = True
    check.save()

    CheckLog.objects.create(check_name=check, status=True)

    return HttpResponse("Ping received!", status=200)


@login_required
def failed_checks_view(request):
    """Displays failed checks for the user"""
    failed_checks = FailedCheck.objects.filter(
        check_name__created_by=request.user
    ).order_by("-failed_at")
    
    return render(request, "checks/failed_checks.html", {"failed_checks": failed_checks})

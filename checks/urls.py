from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="checks/login.html"), name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create_check/", views.create_check, name="create_check"),
     path("check_logs/<int:check_id>/", views.check_logs, name="check_logs"),
     path("check/<int:check_id>/", views.check_detail, name="check_detail"),
     path("ping/<uuid:ping_uuid>/", views.ping_check, name="ping_check"),
     path('', views.welcome, name='welcome'),
     path('logout/', views.logout_view, name='logout'),
     path("failed_checks/", views.failed_checks_view, name="failed_checks"),
]

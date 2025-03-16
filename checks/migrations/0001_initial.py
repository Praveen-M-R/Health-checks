# Generated by Django 5.1 on 2025-02-02 06:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('duration_days', models.PositiveIntegerField(default=0)),
                ('duration_hours', models.PositiveIntegerField(default=0)),
                ('duration_minutes', models.PositiveIntegerField(default=5)),
                ('grace_days', models.PositiveIntegerField(default=0)),
                ('grace_minutes', models.PositiveIntegerField(default=5)),
                ('ping_url', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('channel', models.CharField(blank=True, max_length=100, null=True)),
                ('recipient', models.EmailField(blank=True, max_length=254, null=True)),
                ('last_ping', models.DateTimeField(blank=True, null=True)),
                ('is_up', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CheckLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('check_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='checks.check')),
            ],
        ),
    ]

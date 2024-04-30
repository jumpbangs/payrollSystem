# Generated by Django 4.2.7 on 2024-04-30 04:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('client_name', models.CharField(default=None, max_length=225, null=True)),
                ('client_email', models.EmailField(default=None, max_length=225, null=True)),
                ('client_contact', models.IntegerField(default=None, null=True)),
                ('last_invoiced', models.DateField(default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_address', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.address')),
            ],
        ),
        migrations.CreateModel(
            name='Worklogs',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('worklog_date', models.DateField(default=None, null=True)),
                ('start_time', models.TimeField(default=None, null=True)),
                ('end_time', models.TimeField(default=None, null=True)),
                ('break_time', models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True)),
                ('description', models.CharField(default=None, max_length=225, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorklogDetails',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('job_type', models.CharField(default=None, max_length=225, null=True)),
                ('job_detail', models.CharField(default=None, max_length=225, null=True)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='worklogs.clients')),
                ('worklog_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='worklogs.worklogs')),
            ],
        ),
    ]

# Generated by Django 4.2.7 on 2025-03-13 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('user_id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(default=None, max_length=100, null=True)),
                ('last_name', models.CharField(default=None, max_length=100, null=True)),
                ('date_of_birth', models.DateField(default=None, null=True)),
                ('employment_type', models.CharField(choices=[('1', 'Full Time'), ('2', 'Part Time'), ('3', 'Contractual'), ('4', 'Internship'), ('5', 'Casual')], default='2', max_length=1)),
                ('email', models.EmailField(default=None, max_length=225, unique=True)),
                ('employment_start', models.DateTimeField(auto_now_add=True)),
                ('contact_number', models.IntegerField(default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('password', models.CharField(default=None, max_length=100, null=True)),
                ('user_role', models.CharField(choices=[('E', 'Employee'), ('M', 'Manager'), ('A', 'Admin')], default='E', max_length=1)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('employee_address', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('gross_salary', models.FloatField(default=0, null=True)),
                ('net_salary', models.FloatField(default=0, null=True)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('last_payment', models.DateField(default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmploymentTerms',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('leave_days', models.IntegerField(default=0, null=True)),
                ('sick_days', models.IntegerField(default=14, null=True)),
                ('agreed_salary', models.FloatField(default=None, null=True)),
                ('start_date', models.DateField(default=None, null=True)),
                ('end_date', models.DateField(default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee_id', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

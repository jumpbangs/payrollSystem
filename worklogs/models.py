import uuid

from django.db import models

from employee.models import Employee
from locations.models import Address


class WorklogTypes(models.TextChoices):
    Worklog = "Worklog"
    LeaveLog = "LeaveLog"


class WorklogStatus(models.TextChoices):
    PENDING = "Pending"
    APPROVED = "Approved"
    BILLED = "Billed"


# Create your models here.
class Clients(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    client_name = models.CharField(max_length=225, null=True, default=None)
    client_email = models.EmailField(max_length=225, null=True, default=None)
    client_contact = models.IntegerField(null=True, default=None)
    client_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, default=None)
    client_details = models.JSONField(null=True, default=None)
    last_invoiced = models.DateField(null=True, default=None)
    is_client_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} --> {self.client_name} --> {self.client_email}"


class WorklogDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    client_id = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True, default=None)
    billed_hours = models.DecimalField(null=True, default=0, decimal_places=1, max_digits=10)
    approved_hours = models.DecimalField(null=True, default=0, decimal_places=1, max_digits=10)
    job_detail = models.CharField(max_length=255, null=True, default=None)
    additional_details = models.JSONField(null=True)
    rate = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Worklogs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, default=None)
    worklog_detail_id = models.ForeignKey(WorklogDetails, on_delete=models.CASCADE, null=True, default=None)
    worklog_date = models.DateField(null=True, default=None)
    start_time = models.TimeField(null=True, default=None)
    end_time = models.TimeField(null=True, default=None)
    break_time = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=5)
    description = models.CharField(max_length=255, null=True, default=None)
    worklog_billed = models.BooleanField(default=False)
    worklog_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    worklog_type = models.CharField(
        max_length=20,
        null=False,
        choices=WorklogTypes.choices,
        default=WorklogTypes.Worklog,
    )
    worklog_status = models.CharField(
        max_length=20,
        null=False,
        choices=WorklogStatus.choices,
        default=WorklogStatus.PENDING,
    )

    def __str__(self):
        return str(self.id)

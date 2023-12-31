import uuid

from django.contrib.auth.hashers import check_password, make_password
from django.db import models

from locations.models import Address


# Create your models here.
class WorkerStatus(models.TextChoices):
    ACTIVE = 1, "Active"
    INACTIVE = 2, "Inactive"


class EmploymentType(models.TextChoices):
    FULL_TIME = 1, "Full Time"
    PART_TIME = 2, "Part Time"
    CONTRACTUAL = 3, "Contractual"
    INTERNSHIP = 4, "Internship"
    CASUAL = 5, "Casual"


class JobTitle(models.TextChoices):
    ENGINEER = 1, "Engineer"
    MANAGER = 2, "Manager"
    ACCOUNTANT = 3, "Accountant"
    HR = 4, "HR"
    SALES = 5, "Sales"
    IT = 6, "IT"


class EmploymentStatus(models.Model):
    id = models.IntegerField(primary_key=True, default=0)
    employment_term = models.CharField(max_length=1, null=False, default=3)
    position = models.CharField(max_length=1, null=False, default=JobTitle.ENGINEER, choices=JobTitle.choices)
    status = models.CharField(max_length=1, null=False, default=WorkerStatus.ACTIVE, choices=WorkerStatus.choices)
    employment_type = models.CharField(
        max_length=1, null=False, default=EmploymentType.PART_TIME, choices=EmploymentType.choices
    )

    def __str__(self) -> str:
        return "{value} : {display}".format(
            value=self.get_position_display(),
            display=self.get_employment_type_display() + " - " + self.get_status_display(),
        )

    def save(self, *args, **kwargs):
        self.id = self.id + 1
        super().save(*args, **kwargs)


class Employee(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, null=True, default=None)
    last_name = models.CharField(max_length=100, null=True, default=None)
    date_of_birth = models.DateField(null=True, default=None)
    gender = models.CharField(max_length=10, null=True, default=None)
    employee_status = models.ForeignKey(EmploymentStatus, on_delete=models.CASCADE, null=True, default=None)
    employee_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, default=None)
    email = models.EmailField(max_length=225, unique=True, default=None)
    employment_start = models.DateTimeField(auto_now_add=True)
    contact_number = models.IntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=100, null=True, default=None)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password):
        self.password = make_password(password)
        return self.password

    def check_password(self, password):
        return check_password(password, self.password)


class EmploymentTerms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, default=None)
    leave_days = models.IntegerField(null=True, default=0)
    sick_days = models.IntegerField(null=True, default=14)
    agreed_salary = models.FloatField(null=True, default=None)
    start_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.employment_term


class Payments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, default=None)
    gross_salary = models.FloatField(null=True, default=0)
    net_salary = models.FloatField(null=True, default=0)
    tax = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=10)
    last_payment = models.DateField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.employment_term

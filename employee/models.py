import uuid

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from backend.utils.dateUtils import get_current_year
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


class UserRole(models.TextChoices):
    SUPERVISOR = "S", "Supervisor"
    EMPLOYEE = "E", "Employee"
    MANAGER = "M", "Manager"
    ADMIN = "A", "Admin"


class EmployeeManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be be provided")
        if not password:
            raise ValueError("Password must be provided")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)


class Employee(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    first_name = models.CharField(max_length=100, null=True, default=None)
    last_name = models.CharField(max_length=100, null=True, default=None)
    date_of_birth = models.DateField(null=True, default=None)

    employment_type = models.CharField(
        max_length=1,
        null=False,
        default=EmploymentType.PART_TIME,
        choices=EmploymentType.choices,
    )
    employee_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, default=None)
    email = models.EmailField(max_length=225, unique=True, default=None)
    employment_start = models.DateTimeField(auto_now_add=True)
    contact_number = models.IntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=100, null=True, default=None)

    user_role = models.CharField(max_length=1, null=False, choices=UserRole.choices, default=UserRole.EMPLOYEE)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.password is None:
                username = self.email.split("@")[0]
                self.set_password(str(get_current_year) + str(username))

            super().save(*args, **kwargs)
            EmploymentTerms.objects.create(
                employee_id=self,
                leave_days=0,
                sick_days=14,
            )
        else:
            super().save(*args, **kwargs)

    def set_password(self, password):
        self.password = make_password(password)
        return self.password

    def check_password(self, password):
        return check_password(password, self.password)


class EmploymentTerms(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, default=None)
    leave_days = models.IntegerField(null=True, default=0)
    sick_days = models.IntegerField(null=True, default=14)
    agreed_salary = models.FloatField(null=True, default=None)
    start_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Employment Term"
        verbose_name_plural = "Employment Terms"


class EmployeeBankDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    employee_id = models.OneToOneField(Employee, on_delete=models.CASCADE)
    tax_number = models.CharField(null=True, default=None, max_length=20)
    bank_name = models.CharField(null=True, default=None, max_length=40)
    swift_code = models.CharField(null=True, default=None, max_length=11)
    bank_account_number = models.CharField(null=True, default=None, max_length=10)
    provident_fund_number = models.CharField(null=True, default=None, max_length=20)


class Payments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, default=None)
    gross_salary = models.FloatField(null=True, default=0)
    net_salary = models.FloatField(null=True, default=0)
    tax = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=10)
    last_payment = models.DateField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self) -> str:
        return f"{self.employee_id}"

from django.core.management.base import BaseCommand

from backend.utils.dateUtils import get_current_date, get_current_year
from employee.models import Employee, EmploymentTerms


class Command(BaseCommand):
    help = "Populate initial data into the database"

    def handle(self, *args, **options):
        if Employee.objects.exists():
            return self.stdout.write(self.style.SUCCESS("Initial data already exists"))

        # Create Admin User
        admin = Employee.objects.create(
            first_name="Admin",
            employment_type=1,
            email="admin@mail.com",
            user_role="A",
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )
        admin.set_password("itseasy")
        admin.save()
        self.stdout.write(self.style.SUCCESS("Created admin successfully"))

        # Create initial Employee instances
        emp = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-01-01",
            gender="Male",
            employment_type=1,  # Assuming this corresponds to the EmploymentStatus instance ID
            email="john@example.com",
            employment_start="2022-01-01T00:00:00Z",
            contact_number="1234567890",
            user_role="E",
            is_staff=True,
            is_active=True,
            is_superuser=False,
        )
        emp.set_password(str(get_current_year()) + emp.last_name)
        emp.save()

        EmploymentTerms.objects.create(
            employee_id=emp,
            leave_days=14,
            sick_days=14,
            start_date=get_current_date(),
        )

        self.stdout.write(self.style.SUCCESS("Initial data populated successfully"))

from django.core.management.base import BaseCommand

from employee.models import Teams


class Command(BaseCommand):
    help = "Populate initial team data into the database"

    def handle(self, *args, **options):
        if Teams.objects.exists():
            return self.stdout.write(self.style.SUCCESS("Initial team data already exists"))

        # Create initial Team instances
        Teams.objects.create(team_name="Engineering", description="Handles all engineering tasks")

        Teams.objects.create(team_name="HR", description="Manages human resources")

        Teams.objects.create(team_name="Marketing", description="Responsible for marketing strategies")

        self.stdout.write(self.style.SUCCESS("Created initial teams successfully"))

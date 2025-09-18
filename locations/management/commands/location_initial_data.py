from django.core.management.base import BaseCommand

from locations.models import Address, City, Country


class Command(BaseCommand):
    help = "Initial Location data"

    def handle(self, *args, **kwargs):

        if Country.objects.count() > 0:
            return self.stdout.write(self.style.SUCCESS("Initial data already exists"))

        country = Country.objects.create(
            country_name="Australia",
            country_code="AU",
            phone_code="61",
            currency="AUD",
        )

        self.stdout.write(self.style.SUCCESS("Initial country populated successfully"))

        sydney_branch_1 = City.objects.create(
            city_name="Sydney",
            state="NSW",
            state_code="NSW",
            has_branch=True,
            postal_code="2000",
        )

        Address.objects.create(
            address="401 Sussex St", city_id=sydney_branch_1, country_id=country, lat=-33.8688, lng=151.2093
        )
        Address.objects.create(
            address="26/60 Margaret St", city_id=sydney_branch_1, country_id=country, lat=-33.864832, lng=151.206713
        )

        self.stdout.write(self.style.SUCCESS("Initial NSW branch populated successfully"))

        perth_branch = City.objects.create(
            city_name="Perth",
            state="WA",
            state_code="WA",
            has_branch=True,
            postal_code="6005",
        )

        Address.objects.create(
            address="1/22 Delhi St",
            city_id=perth_branch,
            country_id=country,
            lat=-31.952712,
            lng=115.857048,
        )

        self.stdout.write(self.style.SUCCESS("Initial WA branch populated successfully"))

        queensland_branch = City.objects.create(
            city_name="Gold Coast City",
            state="QLD",
            state_code="QLD",
            has_branch=True,
            postal_code="4218",
        )

        Address.objects.create(
            address="21 Peerless Ave", city_id=queensland_branch, country_id=country, lat=-28.037797, lng=153.435138
        )

        queensland_branch_2 = City.objects.create(
            city_name="Brisbane City",
            state="QLD",
            state_code="QLD",
            has_branch=True,
            postal_code="4017",
        )

        Address.objects.create(
            address="14 Queens Parade", city_id=queensland_branch_2, country_id=country, lat=-27.303746, lng=153.061626
        )

        self.stdout.write(self.style.SUCCESS("Initial QLD populated successfully"))

        vic_branch = City.objects.create(
            city_name="Melbourne",
            state="VIC",
            state_code="VIC",
            has_branch=True,
            postal_code="3195",
        )

        Address.objects.create(
            address="576 Main St",
            city_id=vic_branch,
            country_id=country,
            lat=-38.007044,
            lng=145.086325,
        )

        self.stdout.write(self.style.SUCCESS("Initial VIC populated successfully"))

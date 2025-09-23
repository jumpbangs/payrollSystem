import uuid

from django.db import models


# Create your models here.
class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    country_name = models.CharField(max_length=225, null=True, default=None)
    country_code = models.CharField(max_length=3, null=True, default=None)
    phone_code = models.CharField(max_length=4, null=True, default=None)
    currency = models.CharField(max_length=4, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self) -> str:
        return f"{self.country_name}"


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    city_name = models.CharField(max_length=225, null=True, default=None)
    state = models.CharField(max_length=100, null=True, default=None)
    state_code = models.CharField(max_length=4, null=True, default=None)
    has_branch = models.BooleanField(null=True, default=False)
    postal_code = models.CharField(max_length=10, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self) -> str:
        return f"{self.city_name}"


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    address = models.CharField(max_length=225, null=True, default=None)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE, null=True, default=None, related_name="address_city_id")
    country_id = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, default=None, related_name="address_country_id"
    )
    lat = models.FloatField(null=True, default=0.0)
    lng = models.FloatField(null=True, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self) -> str:
        return f"{self.address}"

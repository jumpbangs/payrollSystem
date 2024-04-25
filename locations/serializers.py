from rest_framework import serializers

from .models import Address, City, Country


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "address",
            "city_id",
            "country_id",
            "lat",
            "lng",
        ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "id",
            "country_name",
            "country_code",
            "phone_code",
            "currency",
        ]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            "id",
            "city_name",
            "state",
            "state_code",
            "has_branch",
            "postal_code",
        ]

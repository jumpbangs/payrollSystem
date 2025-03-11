from rest_framework import serializers

from .models import Address, City, Country


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = [
            "id",
            "address",
            "city_id",
            "country_id",
            "lat",
            "lng",
            "city",
            "country",
        ]

    def get_city(self, obj):
        if obj.city_id:
            return CitySerializer(obj.city_id).data
        return None

    def get_country(self, obj):
        if obj.country_id:
            return CountrySerializer(obj.country_id).data
        return None


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

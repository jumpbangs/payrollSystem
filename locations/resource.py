from import_export import resources

from .models import Address, City, Country


class AddressResource(resources.ModelResource):
    class Meta:
        model = Address
        fields = ("address", "city_id", "country_id", "lat", "lng")


class CountryResource(resources.ModelResource):
    class Meta:
        model = Country
        fields = ("country_name", "country_code", "phone_code", "currency")


class CityResource(resources.ModelResource):
    class Meta:
        model = City
        fields = ("city_name", "state", "state_code", "has_branch", "postal_code")

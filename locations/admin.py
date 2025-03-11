from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import Address, City, Country
from .resource import AddressResource, CityResource, CountryResource


class CountryAdmin(ImportExportModelAdmin):
    resource_class = CountryResource
    list_display = ("id", "country_name", "country_code", "phone_code", "currency")
    search_fields = ("id", "country_name", "country_code", "currency")


class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource
    list_display = ("id", "city_name", "state", "state_code", "has_branch", "postal_code")
    search_fields = ("id", "city_name", "state", "state_code", "has_branch", "postal_code")


class AddressAdmin(ImportExportModelAdmin):
    resource_class = AddressResource
    list_display = ("id", "address", "get_postal_code", "city_id_link", "country_id_link")
    search_fields = ("id", "address", "city_id__city_name", "city_id__state", "city_id__postal_code")

    def get_postal_code(self, obj):
        return obj.city_id.postal_code

    get_postal_code.short_description = "Postal Code"

    def city_id_link(self, obj):
        if obj.city_id:  # Ensure ForeignKey exists
            url = reverse("admin:locations_city_change", args=[obj.city_id.id])
            return format_html('<a href="{}">{}</a>', url, obj.city_id)
        return "-"

    city_id_link.short_description = "City"

    def country_id_link(self, obj):
        if obj.city_id:  # Ensure ForeignKey exists
            url = reverse("admin:locations_country_change", args=[obj.country_id.id])
            return format_html('<a href="{}">{}</a>', url, obj.country_id)
        return "-"

    country_id_link.short_description = "Country"


# Register your models here.
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Address, AddressAdmin)

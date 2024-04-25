from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Address, City, Country
from .resource import AddressResource, CityResource, CountryResource


class CountryAdmin(ImportExportModelAdmin):
    resource_class = CountryResource


class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource


class AddressAdmin(ImportExportModelAdmin):
    resource_class = AddressResource


# Register your models here.
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Address, AddressAdmin)

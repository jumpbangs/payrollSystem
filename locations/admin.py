from django.contrib import admin

from .models import Address, City, Country

# Register your models here.
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Address)
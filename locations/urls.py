from django.urls import path

from locations.views.AddressView import AddressModelView
from locations.views.CityView import CityModelView
from locations.views.CountryView import CountryModelView

urlpatterns = [
    path("city/", CityModelView.as_view()),
    path("address/", AddressModelView.as_view()),
    path("country/", CountryModelView.as_view()),
]

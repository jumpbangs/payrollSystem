from rest_framework.views import APIView

from backend.helpers import is_none_or_empty
from backend.networkHelpers import (
    get_error_response_400,
    get_error_response_404,
    get_server_response_500,
    get_success_response_200,
)
from backend.paginationHelpers import CustomPagination
from locations.models import Country
from locations.serializers import CountrySerializer


# Create your views here.
class CountryModelView(APIView):
    pagination_class = CustomPagination

    """
    GET: Fetch all countries
    """

    def get(self, request):
        try:
            country = Country.objects.all()
            serialized_data = CountrySerializer(country, many=True)
            return get_success_response_200(serialized_data.data)
        except Exception as exception:
            return get_server_response_500(str(exception))

    def post(self, request):
        country_data = request.data
        country_name = country_data.get("country_name")

        if is_none_or_empty(country_data):
            return get_error_response_400("Country data cannot be empty")

        if is_none_or_empty(country_name):
            return get_error_response_400("Country name cannot be empty")

        if is_none_or_empty(country_data.get("country_code")):
            return get_error_response_400("Country code cannot be empty")

        if Country.objects.filter(country_name=country_name).exists():
            return get_error_response_400("Country with this name already exists")

        try:
            serialized_data = CountrySerializer(data=country_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Country data is invalid")
        except Exception as exception:
            return get_server_response_500(str(exception))

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.networkHelpers import (
    get_error_response_400,
    get_error_response_401,
    get_error_response_404,
    get_server_response_500,
    get_success_response_200,
)
from backend.paginationHelpers import CustomPagination
from backend.utils.helpers import is_none_or_empty, is_user_manager_or_admin
from locations.docs.coutry_schema import (
    get_country_schema,
    post_country_schema,
    put_country_schema,
)
from locations.models import Country
from locations.serializers import CountrySerializer


# Create your views here.
class CountryModelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    """
    GET: Fetch all countries
    """

    @get_country_schema
    def get(self, request):
        try:
            country = Country.objects.all()
            serialized_data = CountrySerializer(country, many=True)
            return get_success_response_200(serialized_data.data)

        except Exception as exception:
            return get_server_response_500(f"Exception when fetching country :{str(exception)}")

    """
    POST: Add new country
    """

    @post_country_schema
    def post(self, request):
        country_data = request.data
        country_name = country_data.get("country_name")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can add new countries")

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
            return get_server_response_500(f"Exception when adding a new country :{str(exception)}")

    """
    PUT: Update country
    """

    @put_country_schema
    def put(self, request):
        country_data = request.data
        country_id = country_data.get("country_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can update countries")

        if is_none_or_empty(country_data):
            return get_error_response_400("Country data cannot be empty")

        if is_none_or_empty(country_id):
            return get_error_response_400("Country id cannot be empty")

        try:
            country_data_to_update = Country.objects.get(pk=country_id)
            serialized_data = CountrySerializer(country_data_to_update, data=country_data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Country data is invalid")

        except Country.DoesNotExist:
            return get_error_response_404("Country not found or doesn't exist")
        except Exception as exception:
            return get_server_response_500(f"Exception when updating a country :{str(exception)}")

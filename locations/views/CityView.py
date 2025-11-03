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
from locations.docs.city_schema import (
    delete_city_schema,
    get_city_schema,
    post_city_schema,
    update_city_schema,
)
from locations.models import City
from locations.serializers import CitySerializer


# Create your views here.
class CityModelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    """
    GET: Fetch a city by city_id, state or name
    """

    @get_city_schema
    def get(self, request):
        city_id = request.query_params.get("city_id", None)

        try:
            if city_id is not None:
                city = City.objects.get(pk=city_id)
                serialized_data = CitySerializer(city)
                return get_success_response_200(serialized_data.data)
            else:
                city = City.objects.all()
                serialized_data = CitySerializer(city, many=True)
                return get_success_response_200(serialized_data.data)

        except Exception as exception:
            return get_server_response_500(f"Exception when fetching city :{str(exception)}")

    """
    POST: Add a city
    """

    @post_city_schema
    def post(self, request):
        city_data = request.data
        city_name = city_data.get("city_name")
        city_state = city_data.get("state")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can add new cities")

        if is_none_or_empty(city_data):
            return get_error_response_400("City data cannot be empty")

        if is_none_or_empty(city_name):
            return get_error_response_400("City name cannot be empty")

        if is_none_or_empty(city_state):
            return get_error_response_400("State cannot be empty")

        if City.objects.filter(city_name=city_name).exists():
            return get_error_response_400("City with this name already exists")

        try:
            serialized_data = CitySerializer(data=city_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("City data is invalid")

        except Exception as exception:
            return get_server_response_500(f"Exception when adding a new city :{str(exception)}")

    """
    PUT: Update a city
    """

    @update_city_schema
    def put(self, request):
        city_data = request.data
        city_id = city_data.get("city_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can update cities")

        if is_none_or_empty(city_data):
            return get_error_response_400("City data cannot be empty")

        if is_none_or_empty(city_id):
            return get_error_response_400("City id cannot be empty")

        try:
            city_data_to_update = City.objects.get(pk=city_id)
            serialized_data = CitySerializer(city_data_to_update, data=city_data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("City data is invalid")

        except City.DoesNotExist:
            return get_error_response_404("City not found or doesn't exist")
        except Exception as exception:
            return get_server_response_500(f"Exception when updating a city detail :{str(exception)}")

    """
    DELETE: Delete a city
    """

    @delete_city_schema
    def delete(self, request):
        city_id = request.query_params.get("city_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can delete cities")

        if is_none_or_empty(city_id):
            return get_error_response_400("City id cannot be empty")

        try:
            city_data_to_delete = City.objects.get(pk=city_id)
            city_data_to_delete.delete()
            return get_success_response_200("City deleted successfully")

        except City.DoesNotExist:
            return get_error_response_404("City not found")
        except Exception as exception:
            return get_server_response_500(f"Exception when deleting a city :{str(exception)}")

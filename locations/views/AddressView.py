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
from locations.docs.address_schema import (
    delete_address_schema,
    get_address_schema,
    post_address_schema,
    put_address_schema,
)
from locations.models import Address
from locations.serializers import AddressSerializer


# Create your views here.
class AddressModelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    """
    GET: Fetch Address data by id else fetch all
    """

    @get_address_schema
    def get(self, request):
        address_data = request.query_params.get("address_id")

        if is_none_or_empty(address_data):
            try:
                address_data = Address.objects.all()
                serialized_data = AddressSerializer(address_data, many=True)
                return get_success_response_200(serialized_data.data)

            except Exception as exception:
                return get_server_response_500(f"Exception when fetching addresses :{str(exception)}")
        else:
            try:
                address_data = Address.objects.get(pk=address_data)
                serialized_data = AddressSerializer(address_data)
                return get_success_response_200(serialized_data.data)

            except Address.DoesNotExist:
                return get_error_response_404("Address not found or doesn't exist")
            except Exception as exception:
                return get_server_response_500(f"Exception when fetching address :{str(exception)}")

    """
    POST: Add Address data
    """

    @post_address_schema
    def post(self, request):
        address_data = request.data
        address = address_data.get("address")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can add new addresses")

        if is_none_or_empty(address_data):
            return get_error_response_400("Address data cannot be empty")

        if is_none_or_empty(address):
            return get_error_response_400("Address cannot be empty")

        if is_none_or_empty(address_data.get("city_id")):
            return get_error_response_400("City id cannot be empty")

        if is_none_or_empty(address_data.get("country_id")):
            return get_error_response_400("Country id cannot be empty")

        try:
            serialized_data = AddressSerializer(data=address_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Address data is invalid")
        except Exception as exception:
            return get_server_response_500(f"Exception when adding new address  :{str(exception)}")

    """
    PUT: Update Address data
    """

    @put_address_schema
    def put(self, request):
        address_data = request.data
        address_id = address_data.get("address_id")
        updated_address = address_data.get("address")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can update addresses")

        if is_none_or_empty(updated_address):
            return get_error_response_400("Address cannot be empty")

        if is_none_or_empty(address_id):
            return get_error_response_400("Address id cannot be empty")

        try:
            address_data_to_update = Address.objects.get(pk=address_id)
            serialized_data = AddressSerializer(address_data_to_update, data=address_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Address data is invalid")

        except Exception as exception:
            return get_server_response_500(f"Exception when updating address detail: {str(exception)}")

    """
    DELETE: Delete Address data
    """

    @delete_address_schema
    def delete(self, request):
        address_id = request.query_params.get("address_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can delete addresses")

        if is_none_or_empty(address_id):
            return get_error_response_400("Address cannot be empty")

        try:
            address_to_delete = Address.objects.get(pk=address_id)
            address_to_delete.delete()
            return get_success_response_200("Address deleted successfully")

        except Address.DoesNotExist:
            return get_error_response_400("Address not found")
        except Exception as exception:
            return get_server_response_500(f"Exception when deleting address :{str(exception)}")

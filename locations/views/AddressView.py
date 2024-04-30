from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.networkHelpers import (
    get_error_response_400,
    get_server_response_500,
    get_success_response_200,
)
from backend.paginationHelpers import CustomPagination
from backend.utils.helpers import is_none_or_empty, is_user_manager_or_admin
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

    def get(self, request):
        address_data = request.data.get("address_id")

        if is_none_or_empty(address_data):
            try:
                address_data = Address.objects.all()
                serialized_data = AddressSerializer(address_data, many=True)
                return get_success_response_200(serialized_data.data)

            except Exception as exception:
                return get_server_response_500(str(exception))
        else:
            try:
                address_data = Address.objects.get(pk=address_data)
                serialized_data = AddressSerializer(address_data)
                return get_success_response_200(serialized_data.data)

            except Address.DoesNotExist:
                return get_error_response_400("Address not found or doesn't exist")
            except Exception as exception:
                return get_server_response_500(str(exception))

    """
    POST: Add Address data
    """

    def post(self, request):
        address_data = request.data
        address = address_data.get("address")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_400("Only admin and manager can add new addresses")

        if is_none_or_empty(address_data):
            return get_error_response_400("Address data cannot be empty")

        if is_none_or_empty(address):
            return get_error_response_400("Address cannot be empty")

        if is_none_or_empty(address_data.get("city_id")):
            return get_error_response_400("City id cannot be empty")

        if is_none_or_empty(address_data.get("country_id")):
            return get_error_response_400("Country id cannot be empty")

        try:
            print(address_data)
            serialized_data = AddressSerializer(data=address_data)
            print(serialized_data.is_valid())
            if serialized_data.is_valid():
                # print(serialized_data.data)
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Address data is invalid")
        except Exception as exception:
            return get_server_response_500(str(exception))

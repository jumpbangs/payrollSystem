from rest_framework.views import APIView

from backend.networkHelpers import (
 get_server_response_500, get_success_response_200,
)
from backend.paginationHelpers import CustomPagination
from locations.models import Address
from locations.serializers import AddressSerializer


# Create your views here.    
class AddressModelView(APIView):
    pagination_class = CustomPagination
    def get(self, request):
        try :
            address = Address.objects.all()
            serialized_data = AddressSerializer(address, many=True)
            return get_success_response_200(serialized_data.data)
        except Exception as exception:
            return get_server_response_500(str(exception))
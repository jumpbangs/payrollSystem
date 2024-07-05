from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.networkHelpers import (
    get_error_response_400,
    get_server_response_500,
    get_success_response_200,
)
from backend.paginationHelpers import CustomPagination
from backend.utils.helpers import is_none_or_empty
from worklogs.models import Clients
from worklogs.seralizers import ClientMinSerializer, ClientSerializer


# Create your views here.
class ClientModelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    """
    GET: Fetch client by id or fetch all
    """

    def get(self, request):
        req_client_data = request.data.get("client_id")

        if is_none_or_empty(req_client_data):
            try:
                all_client_data = Clients.objects.all()
                serialized_data = ClientMinSerializer(all_client_data, many=True)
                return get_success_response_200(serialized_data.data)

            except Exception as exception:
                return get_server_response_500(str(exception))

        else:
            try:
                client_data = Clients.objects.get(pk=req_client_data)
                serialized_client_data = ClientSerializer(client_data)
                return get_success_response_200(serialized_client_data.data)

            except Clients.DoesNotExist:
                return get_error_response_400("Client does not exist")
            except Exception as exception:
                return get_server_response_500(str(exception))

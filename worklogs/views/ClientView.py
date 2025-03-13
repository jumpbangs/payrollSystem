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
from worklogs.models import Clients, WorklogDetails
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
        req_client_id = request.data.get("client_id")

        if is_none_or_empty(req_client_id):
            try:
                all_client_data = Clients.objects.all()
                serialized_data = ClientMinSerializer(all_client_data, many=True)
                return get_success_response_200(serialized_data.data)

            except Exception as exception:
                return get_server_response_500(str(exception))

        else:
            try:
                client_data = Clients.objects.get(pk=req_client_id)
                serialized_client_data = ClientSerializer(client_data)
                return get_success_response_200(serialized_client_data.data)

            except Clients.DoesNotExist:
                return get_error_response_400("Client does not exist")
            except Exception as exception:
                return get_server_response_500(str(exception))

    """
    POST: Add client detail
    """

    def post(self, request):
        req_client_data = request.data
        required_fields = ["client_name", "client_email", "client_contact"]

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only managers and admins can add client data")

        missing_fields = [field for field in required_fields if field not in req_client_data]
        if missing_fields:
            return get_error_response_400(f"Missing fields: {', '.join(missing_fields)}")

        try:
            filter_kwargs = {field: req_client_data[field] for field in required_fields if req_client_data[field]}
            check_client_data = Clients.objects.filter(**filter_kwargs)

            if check_client_data.exists():
                return get_error_response_400("Client already exists")

            serialized_data = ClientSerializer(data=req_client_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Invalid client data")

        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    PATCH: Update Client details
    """

    def patch(self, request):
        client_data = request.data
        client_id = client_data.get("client_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only managers and admins can update client data")

        if is_none_or_empty(client_id):
            return get_error_response_400("Client id cannot be empty")

        try:
            client_to_update: Clients = Clients.objects.get(pk=client_id)
            serialized_data = ClientSerializer(client_to_update, data=client_data, partial=True)

            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)

        except Clients.DoesNotExist:
            return get_error_response_404("Client not found")
        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    DELETE: Delete Client details
    """

    def delete(self, request):
        client_id = request.data.get("client_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only managers and admins can delete client data")

        if is_none_or_empty(client_id):
            return get_error_response_400("Client id cannot be empty")

        try:
            worklog_details_available = WorklogDetails.objects.filter(client_id=client_id)

            # [TODO] Need to handle what if client is deleted
            if worklog_details_available.exists():
                return get_success_response_200("Worklog details exists")

            else:
                client_data_to_delete: Clients = Clients.objects.get(pk=client_id)
                client_data_to_delete.delete()
                return get_success_response_200("Client deleted successfully")

        except Clients.DoesNotExist:
            return get_error_response_404("Employee not found")

        except Exception as exception:
            return get_server_response_500(str(exception))

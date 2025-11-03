from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.networkHelpers import (
    get_error_response_400,
    get_error_response_401,
    get_server_response_500,
    get_success_response_200,
)
from backend.paginationHelpers import CustomPagination, PaginationHandlerMixin
from backend.utils.helpers import is_none_or_empty, is_user_manager_or_admin
from worklogs.docs.client_schema import (
    get_client_schema,
    patch_client_schema,
    post_client_schema,
)
from worklogs.models import Clients
from worklogs.serializers import ClientMinSerializer, ClientSerializer


# Create your views here.
class ClientModelView(APIView, PaginationHandlerMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    """
    GET: Fetch client by id or fetch all
    """

    @get_client_schema
    def get(self, request):
        req_client_id = request.query_params.get("client_id")

        if is_none_or_empty(req_client_id):
            try:
                client_queryset = Clients.objects.all()
                client_pages = self.paginate_queryset(client_queryset)
                serialized_data = ClientMinSerializer(client_pages, many=True)
                return self.get_paginated_response(serialized_data.data)

            except Exception as exception:
                return get_server_response_500(f"Exception when fetching clients' details : {str(exception)}")

        else:
            try:
                client_data = Clients.objects.get(pk=req_client_id)
                serialized_client_data = ClientSerializer(client_data)
                return get_success_response_200(serialized_client_data.data)

            except Clients.DoesNotExist:
                return get_error_response_400("Client does not exist")
            except Exception as exception:
                return get_server_response_500(f"Exception when fetching client's detail :{str(exception)}")

    """
    POST: Add client detail
    """

    @post_client_schema
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
            return get_server_response_500(f"Exception when adding new client : {str(exception)}")

    """
    PATCH: Update Client with given client id
    """

    @patch_client_schema
    def patch(self, request):
        update_client_data = request.data
        details_to_update = update_client_data.get("client_details")
        client_id = update_client_data.get("client_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can update client")

        try:
            update_client_detail = Clients.objects.get(id=client_id)
            serialized_data = ClientSerializer(update_client_detail, data=details_to_update, partial=True)

            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Client data is invalid")

        except Clients.DoesNotExist:
            return get_error_response_400("Given client_id does not exist")

        except Exception as exception:
            return get_server_response_500(f"Exception when updating client detail: {str(exception)}")

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
from worklogs.models import Clients, Jobs
from worklogs.seralizers import JobsSerializer


# Create your views here.
class WorklogModelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        return get_success_response_200("Worklog data fetched successfully")


class JobsModelView(APIView, PaginationHandlerMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    """
    GET: Fetch Worklog by id
    """

    def get(self, request):
        worklog_detail_id = request.data.get("detail_id")

        if is_none_or_empty(worklog_detail_id):
            try:
                all_worklog_detail_queryset = Jobs.objects.all()
                page = self.paginate_queryset(all_worklog_detail_queryset)
                serialized_data = JobsSerializer(page, many=True)
                return self.get_paginated_response(serialized_data.data)
            except Exception as exception:
                return get_server_response_500(str(exception))
        else:
            try:
                worklog_detail = Jobs.objects.get(pk=worklog_detail_id)
                serialized_worklog_detail_data = JobsSerializer(worklog_detail)
                return get_success_response_200(serialized_worklog_detail_data.data)

            except Jobs.DoesNotExist:
                return get_error_response_400("Job id does not exist")
            except Exception as exception:
                return get_server_response_500(str(exception))

    """
    POST: Add a new worklog detail
    """

    def post(self, request):
        worklog_data = request.data
        required_fields = ["client_id", "job_detail", "rate"]

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only managers and admins can add worklog detail")

        missing_fields = [field for field in required_fields if field not in worklog_data]
        if missing_fields:
            return get_error_response_400(f"Missing fields : {', '.join(missing_fields)}")

        try:
            check_client_details = Clients.objects.filter(id=worklog_data["client_id"])

            if not check_client_details.exists():
                return get_error_response_400("Client does not exist")

            serialized_data = JobsSerializer(data=worklog_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Failed to add new worklog detail")

        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    PATCH: Update the worklog detail by ID
    """

    def patch(self, request):
        worklog_detail = request.data
        required_fields = ["client_id", "job_detail", "rate"]
        worklog_detail_id = worklog_detail.get("worklog_detail_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can update worklog detail")

        if is_none_or_empty(worklog_detail_id):
            return get_error_response_400("worklog_detail_id is required!")

        missing_fields = [field for field in required_fields if field not in worklog_detail]
        if missing_fields:
            return get_error_response_400(f"Missing fields : {', '.join(missing_fields)}")

        try:
            update_worklog_detail = Jobs.objects.get(id=worklog_detail_id)
            serialized_data = JobsSerializer(update_worklog_detail, data=worklog_detail, partial=True)

            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Job data is invalid")

        except Jobs.DoesNotExist:
            return get_error_response_400("Given detail_id for worklog does not exist")

        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    DELETE: Delete the worklog detail by ID
    """

    def delete(self, request):
        request_worklog_detail_id = request.data.get("detail_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admins and managers can delete worklog detail")

        if request_worklog_detail_id is None:
            return get_error_response_400("detail_id is required")

        try:
            worklog_detail_to_delete = Jobs.objects.filter(id=request_worklog_detail_id)

            if worklog_detail_to_delete.exists():
                worklog_detail_to_delete.first().delete()
                return get_success_response_200("Deleted selected worklog detail")
            else:
                return get_error_response_400("Following worklog detail_id does not exists!")

        except Exception as exception:
            return get_server_response_500(str(exception))

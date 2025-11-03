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
from backend.paginationHelpers import CustomPagination, PaginationHandlerMixin
from backend.utils.dateUtils import get_current_date
from backend.utils.helpers import is_none_or_empty, is_user_manager_or_admin
from worklogs.docs.worklog_schema import (
    delete_worklog_schema,
    get_worklog_schema,
    patch_worklog_schema,
    post_worklog_schema,
)
from worklogs.models import Clients, Jobs, Worklogs
from worklogs.serializers import JobsSerializer, WorklogMinSerializer, WorklogSerializer


# Create your views here.
class WorklogModelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    """
    GET: Fetch Worklogs or a single worklog
    """

    @get_worklog_schema
    def get(self, request):
        req_worklog_id = request.query_params.get("worklog_id")
        user_id = request.user.user_id

        if is_none_or_empty(req_worklog_id):
            try:
                worklog_obj = Worklogs.objects.filter(employee_id=user_id)
                serialized_data = WorklogMinSerializer(worklog_obj, many=True)
                return get_success_response_200(serialized_data.data)
            except Exception as exception:
                return get_server_response_500(f"Exception fetching worklogs :{str(exception)}")

        else:
            try:
                worklog_obj = Worklogs.objects.filter(id=req_worklog_id, employee_id=user_id).first()
                if worklog_obj is None:
                    return get_success_response_200("No worklogs found")
                else:
                    serialized_data = WorklogSerializer(worklog_obj)
                    return get_success_response_200(serialized_data.data)

            except Worklogs.DoesNotExist:
                return get_error_response_404("Worklog not found")
            except Exception as exception:
                return get_server_response_500(f"Exception fetching worklog :{str(exception)}")

    """
    POST: Create new worklog
    """

    @post_worklog_schema
    def post(self, request):
        worklog_data = request.data
        user_id = request.user.user_id
        required_fields = ["job_id", "start_time", "end_time", "description", "worklog_type"]

        if is_none_or_empty(worklog_data):
            return get_error_response_400("Worklog data is empty")

        missing_fields = [field for field in required_fields if field not in worklog_data]
        if missing_fields:
            return get_error_response_400(f"Missing fields: {', '.join(missing_fields)}")

        if "worklog_date" not in worklog_data:
            worklog_data["worklog_date"] = get_current_date()

        try:
            worklog_data["employee_id"] = user_id
            serialized_worklog_entry = WorklogSerializer(data=worklog_data)

            if serialized_worklog_entry.is_valid():
                serialized_worklog_entry.save()
                return get_success_response_200(serialized_worklog_entry.data)
            else:
                return get_error_response_400("Invalid worklog data")
        except Exception as exception:
            return get_server_response_500(f"Exception when adding new worklog :{str(exception)}")

    """
    PATCH: Update given worklog by worklog_id
    """

    @patch_worklog_schema
    def patch(self, request):
        worklog_data = request.data
        user_id = request.user.user_id
        worklog_id = worklog_data.get("worklog_id")

        if is_none_or_empty(worklog_data):
            return get_error_response_400("Worklog data is empty")

        if worklog_data.get("worklog_id") is None:
            return get_error_response_400("Worklog id is required")

        try:
            worklog_to_update = Worklogs.objects.filter(id=worklog_id, employee_id=user_id).first()

            if worklog_to_update is None:
                return get_error_response_400("Worklog does not belong to the user")

            serialized_worklog = WorklogSerializer(worklog_to_update, data=worklog_data, partial=True)
            if serialized_worklog.is_valid():
                return get_success_response_200(serialized_worklog.data)
            else:
                return get_error_response_400(
                    f"Exception when saving updated worklog : {str(serialized_worklog.errors)}"
                )

        except Worklogs.DoesNotExist:
            return get_error_response_404("Invalid worklog id")
        except Exception as exception:
            return get_server_response_500(f"Exception when updating worklog :{str(exception)}")

    """
    DELETE: Delete the given worklog by worklog_id
    """

    @delete_worklog_schema
    def delete(self, request):
        user_role = request.user.user_role
        user_id = request.user.user_id
        worklog_id = request.data.get("worklog_id")

        if is_none_or_empty(worklog_id):
            return get_error_response_400("Worklog_id is required")

        try:
            worklog_to_delete_obj = Worklogs.objects.filter(pk=worklog_id).first()
            if is_user_manager_or_admin(user_role) or worklog_to_delete_obj.employee_id.user_id == user_id:
                worklog_to_delete_obj.delete()
                return get_success_response_200("Worklog deleted")
            else:
                return get_error_response_400("only managers, admin or the owner can delete the following worklog")

        except Worklogs.DoesNotExist:
            return get_error_response_400("Worklog_id is invalid")
        except Exception as exception:
            return get_server_response_500(f"Exception when deleting a worklog :{str(exception)}")


class JobsModelView(APIView, PaginationHandlerMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    """
    GET: Fetch Job by id
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
                return get_server_response_500(f"Exception when fetching jobs :{str(exception)}")
        else:
            try:
                worklog_detail = Jobs.objects.get(pk=worklog_detail_id)
                serialized_worklog_detail_data = JobsSerializer(worklog_detail)
                return get_success_response_200(serialized_worklog_detail_data.data)

            except Jobs.DoesNotExist:
                return get_error_response_400("Job id does not exist")
            except Exception as exception:
                return get_server_response_500(f"Exception when fetching job :{str(exception)}")

    """
    POST: Add a new Job detail
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
            return get_server_response_500(f"Exception when adding a new job :{str(exception)}")

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
            return get_server_response_500(f"Exception when updating job detail :{str(exception)}")

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
            return get_server_response_500(f"Exception when deleting job :{str(exception)}")

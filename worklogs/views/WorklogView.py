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
from backend.utils.dateUtils import get_current_date
from backend.utils.helpers import is_none_or_empty, is_user_manager_or_admin
from worklogs.models import WorklogDetails, Worklogs
from worklogs.seralizers import (
    WorklogDetailSerializer,
    WorklogMinSerializer,
    WorklogSerializer,
)


# Create your views here.
class WorklogModelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    """
    GET: Fetch Worklogs or a single worklog
    """

    def get(self, request):
        req_worklog_id = request.data.get("worklog_id")
        user_id = request.user.user_id

        if is_none_or_empty(req_worklog_id):
            try:
                worklog_obj = Worklogs.objects.filter(employee_id=user_id)
                serialized_data = WorklogMinSerializer(worklog_obj, many=True)
                return get_success_response_200(serialized_data.data)
            except Exception as exception:
                return get_server_response_500(str(exception))

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
                return get_server_response_500(str(exception))

    """
    POST: Create new worklog
    """

    def post(self, request):
        worklog_data = request.data
        user_id = request.user.user_id
        required_fields = ["worklog_detail_id", "start_time", "end_time", "description", "worklog_type"]

        if is_none_or_empty(worklog_data):
            return get_error_response_400("Worklog data empty")

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
            return get_server_response_500(str(exception))

    """
    PATCH: Update given worklog by worklog_id
    """

    def patch(self, request):
        worklog_data = request.data
        user_id = request.user.user_id
        worklog_id = worklog_data.get("worklog_id")

        if is_none_or_empty(worklog_data):
            return get_error_response_400("Worklog data empty")

        if worklog_data.get("worklog_id") is None:
            return get_error_response_400("Worklog id required")

        try:
            worklog_to_update = Worklogs.objects.filter(id=worklog_id, employee_id=user_id).first()

            if worklog_to_update is None:
                return get_error_response_400("Worklog does not belong to the user")

            serialized_worklog = WorklogSerializer(worklog_to_update, data=worklog_data, partial=True)
            if serialized_worklog.is_valid():
                return get_success_response_200(serialized_worklog.data)
            else:
                return get_error_response_400(str(serialized_worklog.errors))

        except Worklogs.DoesNotExist:
            return get_error_response_404("Invalid worklog id")
        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    DELETE: Delete the given worklog by worklog_id
    """

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
            return get_server_response_500(str(exception))


class WorklogDetailModelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    GET: Fetch detail for worklog
    """

    def get(self, request):
        worklog_detail_id = request.data.get("worklog_detail_id")
        client_id = request.data.get("client_id")

        if is_none_or_empty(worklog_detail_id) and is_none_or_empty(client_id):
            return get_error_response_400("Required worklog_detail_id or client_id")

        try:
            queryset = WorklogDetails.objects
            # Determine the filter criteria
            filter_kwargs = {}
            if worklog_detail_id:
                filter_kwargs["id"] = worklog_detail_id
            if client_id:
                filter_kwargs["client_id"] = client_id

            # Apply filters
            worklog_detail_obj = queryset.filter(**filter_kwargs)

            # Serialize based on result type
            many = client_id and not worklog_detail_id  # If filtering only by client_id, expect multiple results
            worklog_detail_obj = worklog_detail_obj.first() if not many else worklog_detail_obj
            serialized_data = WorklogDetailSerializer(worklog_detail_obj, many=many)

            return get_success_response_200(serialized_data.data)

        except WorklogDetails.DoesNotExist:
            return get_error_response_404("Worklog details not found")

        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    POST: Added detail for worklog
    """

    def post(self, request):
        req_worklog_detail_data = request.data
        required_fields = ["client_id", "job_detail"]

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only managers and admins can add worklog detail")

        missing_fields = [field for field in required_fields if field not in req_worklog_detail_data]
        if missing_fields:
            return get_error_response_400(f"Missing fields: {', '.join(missing_fields)}")

        try:
            serialized_data = WorklogDetailSerializer(data=req_worklog_detail_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Invalid worklog detail data")

        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    PATCH: Update Worklog detail by worklog_detail_id
    """

    def patch(self, request):
        update_worklog_data = request.data
        worklog_detail_id = request.data.get("worklog_detail_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only managers and admins can update worklog detail")

        if is_none_or_empty(worklog_detail_id):
            return get_error_response_400("worklog_detail_id required")

        try:
            worklog_detail_to_update_obj = WorklogDetails.objects.get(pk=worklog_detail_id)
            serialized_data = WorklogDetailSerializer(
                worklog_detail_to_update_obj, data=update_worklog_data, partial=True
            )

            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)

        except WorklogDetails.DoesNotExist:
            return get_error_response_400("Invalid worklog detail id")

        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    DELETE: Delete Worklog detail by worklog_detail_id
    """

    def delete(self, request):
        worklog_detail_id = request.data.get("worklog_detail_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only managers and admins can delete worklog detail")

        if is_none_or_empty(worklog_detail_id):
            return get_error_response_400("worklog_detail_id required")

        try:
            delete_worklog_detail = WorklogDetails.objects.filter(pk=worklog_detail_id).first()
            delete_worklog_detail.delete()
            return get_success_response_200("Worklog detail deleted")

        except WorklogDetails.DoesNotExist:
            return get_error_response_404("Invalid Worklog detail id")

        except Exception as exception:
            return get_server_response_500(str(exception))

from rest_framework.views import APIView

from backend.networkHelpers import (
    get_error_response_400,
    get_error_response_401,
    get_error_response_404,
    get_server_response_500,
    get_success_response_200,
)
from backend.utils.helpers import is_none_or_empty, is_user_manager_or_admin
from worklogs.models import WorklogDetails
from worklogs.seralizers import WorklogDetailSerializer


# Create your views here.
class WorklogModelView(APIView):
    def get(self, request):
        return get_success_response_200("Worklog data fetched successfully")


class WorklogDetailModelView(APIView):
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

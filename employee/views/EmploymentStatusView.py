
from rest_framework.views import APIView

from backend.networkHelpers import (
    get_server_response_500, get_success_response_200,
)
from employee.models import EmploymentStatus, EmploymentType, JobTitle
from employee.serializers import EmploymentStatusSerializer


class EmploymentStatusModelView(APIView):
    """
    GET: Get all employment status
    """
    def get(self, request):
        try:
            employment_status = EmploymentStatus.objects.all()
            serialisered_data = EmploymentStatusSerializer(employment_status, many=True)
            return get_success_response_200(serialisered_data.data)
        except Exception as exception:
            return get_server_response_500(str(exception))

class EmploymentTypeModelView(APIView):

    """
    GET: Get employment types
    """
    def get(self, request):
        try:
            employment_type = { option[0] : option[1] for option in EmploymentType.choices}
            return get_success_response_200(employment_type)
        except Exception as exception:
            return get_server_response_500(str(exception))
        
class JobTitlesModelView(APIView):

    """
    GET: Get job titles
    """
    def get(self, request):
        try:
            job_titles = { option[0] : option[1] for option in JobTitle.choices}
            return get_success_response_200(job_titles)
        except Exception as exception:
            return get_server_response_500(str(exception))
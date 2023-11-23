from rest_framework.views import APIView

from backend.networkHelpers import get_success_response_200


# Create your views here.
class WorklogModelView(APIView):
    def get(self, request):
        return get_success_response_200('Worklog data fetched successfully')
    
class WorklogDetailModelView(APIView):
    def get(self, request):
        return get_success_response_200('Worklog data fetched successfully')
from rest_framework.views import APIView

from backend.networkHelpers import get_server_response_500, get_success_response_200
from backend.paginationHelpers import CustomPagination
from locations.models import Country
from locations.serializers import CountrySerializer


# Create your views here.
class CountryModelView(APIView):
    
    pagination_class = CustomPagination\
    
    """
    GET: Fetch all countries
    """
    def get(self, request):
        try:
            country = Country.objects.all()
            serialized_data = CountrySerializer(country, many=True)
            return get_success_response_200(serialized_data.data)
        except Exception as exception:
            return get_server_response_500(str(exception))
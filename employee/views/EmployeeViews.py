from rest_framework.views import APIView

from backend.helpers import is_none_or_empty
from backend.networkHelpers import (
    get_error_response_400, get_error_response_404, get_server_response_500,
    get_success_response_200,
)
from employee.models import Employee
from employee.serializers import EmployeeSerializer


# Create your views here.
class EmployeeModelView(APIView):
    """
    GET: Fetch Employee data by id else fetch all
    """

    def get(self, request):
        employee_data = request.GET.get('user_id')
        if is_none_or_empty(employee_data):
            try:
                employee_data = Employee.objects.all()
                serialised_data = EmployeeSerializer(employee_data, many=True)
                return get_success_response_200(serialised_data.data)

            except Exception as exception:
                return get_server_response_500(str(exception))
        else:
            try:
                employee_data = Employee.objects.get(pk=employee_data)
                serialised_data = EmployeeSerializer(employee_data)
                return get_success_response_200(serialised_data.data)

            except Employee.DoesNotExist:
                return get_error_response_404('Employee not found')
            except Exception as exception:
                return get_server_response_500(str(exception))

    """
    POST: Add new Employee
    """

    def post(self, request):
        employee_data = request.data

        if is_none_or_empty(employee_data):
            return get_error_response_400('Employee data cannot be empty')
        
        if is_none_or_empty(employee_data.get('email')):
            return get_error_response_400('Employee email cannot be empty')
        else :
            if Employee.objects.filter(email=employee_data.get('email')).exists():
                return get_error_response_400('Employee with this email already exists')
            
        if is_none_or_empty(employee_data.get('password')):
            return get_error_response_400('Employee password cannot be empty')

        try:
            serialised_data = EmployeeSerializer(data=employee_data)
            if serialised_data.is_valid():
                serialised_data.save()
                return get_success_response_200('Employee added successfully')
            else:
                return get_error_response_400('Employee data is invalid')
        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    PUT: Update Employee
    """

    def patch(self, request):
        employee_data = request.data
        user_id = employee_data.get('user_id')

        if is_none_or_empty(employee_data):
            return get_error_response_400('Employee data cannot be empty')

        if is_none_or_empty(user_id):
            return get_error_response_400('Employee id cannot be empty')

        try:
            employee_data_to_update: Employee = Employee.objects.get(pk=user_id)
            serialised_data = EmployeeSerializer(employee_data_to_update, data=employee_data, partial=True)
            if serialised_data.is_valid():
                serialised_data.save()
                return get_success_response_200(serialised_data.data)
            else:
                return get_error_response_400('Employee data is invalid')

        except Employee.DoesNotExist:
            return get_error_response_404('Employee not found or doesn\'t exist')
        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    DELETE: Delete Employee
    """

    def delete(self, request):
        employee_data = request.data
        user_id = employee_data.get('user_id')

        if is_none_or_empty(user_id):
            return get_error_response_400('Employee id cannot be empty')

        try:
            employee_data_to_delete: Employee = Employee.objects.get(pk=user_id)
            employee_data_to_delete.delete()
            return get_success_response_200('Employee deleted successfully')
        except Employee.DoesNotExist:
            return get_error_response_404('Employee not found')
        except Exception as exception:
            return get_server_response_500(str(exception))

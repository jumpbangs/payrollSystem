from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.networkHelpers import (
    get_error_response_400,
    get_error_response_404,
    get_server_response_500,
    get_success_response_200,
)
from backend.utils.helpers import (
    is_none_or_empty,
    is_user_admin,
    is_user_manager_or_admin,
)
from employee.models import Employee
from employee.serializers import EmployeeSerializer


# Create your views here.
class EmployeeModelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    GET: Fetch Employee data by id else fetch all
    """

    def get(self, request):
        employee_id = request.data.get("user_id")
        if is_none_or_empty(employee_id):
            if not is_user_manager_or_admin(request.user.user_role):
                return get_error_response_404("Only admin and manager can fetch all employees")

            try:
                employee_data = Employee.objects.all().exclude(user_id=request.user.user_id)
                serialized_data = EmployeeSerializer(employee_data, many=True)
                return get_success_response_200(serialized_data.data)

            except Exception as exception:
                return get_server_response_500(str(exception))
        else:
            try:
                employee_data = Employee.objects.filter(user_id__in=employee_id)
                serialized_data = EmployeeSerializer(employee_data, many=True)
                return get_success_response_200(serialized_data.data)

            except Employee.DoesNotExist:
                return get_error_response_404("Employee not found")
            except Exception as exception:
                return get_server_response_500(str(exception))

    """
    POST: Add new Employee
    """

    def post(self, request):
        employee_data = request.data

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_400("Only admin and manager can add new employees")

        if is_none_or_empty(employee_data):
            return get_error_response_400("Employee data cannot be empty")

        if is_none_or_empty(employee_data.get("email")):
            return get_error_response_400("Employee email cannot be empty")
        else:
            if Employee.objects.filter(email=employee_data.get("email")).exists():
                return get_error_response_400("Employee with this email already exists")

        if is_none_or_empty(employee_data.get("password")):
            return get_error_response_400("Employee password cannot be empty")

        try:
            new_employee = Employee.objects.create(**employee_data)
            new_employee.set_password(employee_data.get("password"))
            new_employee.save()
            return get_success_response_200("Employee added successfully")

        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    PUT: Update Employee
    """

    def patch(self, request):
        employee_data = request.data
        user_id = employee_data.get("user_id")
        is_allowed_to_update = False
        if is_none_or_empty(employee_data):
            return get_error_response_400("Employee data cannot be empty")

        if is_none_or_empty(user_id):
            return get_error_response_400("Employee id cannot be empty")

        if is_user_manager_or_admin(request.user.user_role):
            is_allowed_to_update = True

        if not is_user_admin(request.user.user_role) and employee_data.get("user_role") is not None:
            return get_error_response_400("Only admin can update employee role")

        try:
            employee_data_to_update: Employee = Employee.objects.get(pk=user_id)
            if employee_data_to_update.user_id != request.user.user_id and not is_allowed_to_update:
                return get_error_response_400("You are can only update your own profile")

            serialized_data = EmployeeSerializer(employee_data_to_update, data=employee_data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Employee data is invalid")

        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    DELETE: Delete Employee
    """

    def delete(self, request):
        employee_data = request.data
        user_id = employee_data.get("user_id")

        if not is_user_admin(request.user.user_role):
            return get_error_response_400("Only admin can delete employees")

        if is_none_or_empty(user_id):
            return get_error_response_400("Employee id cannot be empty")

        try:
            employee_data_to_delete: Employee = Employee.objects.get(pk=user_id)
            employee_data_to_delete.delete()
            return get_success_response_200("Employee deleted successfully")
        except Employee.DoesNotExist:
            return get_error_response_404("Employee not found")
        except Exception as exception:
            return get_server_response_500(str(exception))

from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from backend.networkHelpers import (
    get_error_response_400,
    get_error_response_401,
    get_server_response_500,
    get_success_response_200,
)
from backend.utils.helpers import is_none_or_empty
from employee.docs.auth_schema import (
    change_password_schema,
    login_schema,
    logout_schema,
)
from employee.models import Employee
from employee.serializers import EmployeeSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    """
    POST: Login API for Users
    """

    @login_schema
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if is_none_or_empty(email) or is_none_or_empty(password):
            return get_error_response_400("Email and password cannot be empty")

        try:
            employee = Employee.objects.get(email=email)
            if employee is None:
                return get_error_response_400("The email is not registered")

            else:
                if not check_password(password, employee.password):
                    return get_error_response_400("The password is incorrect")

                login(request, employee)

                token, _ = Token.objects.get_or_create(user=employee)
                user_serialized_data = EmployeeSerializer(employee).data
                data = {"access_token": token.key, "user": user_serialized_data}
                return get_success_response_200(data)

        except Exception as exception:
            return get_server_response_500(str(exception))


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    DELETE: Logout API for Logging out users
    """

    @logout_schema
    def delete(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return get_success_response_200("Logout successful")
        else:
            return get_error_response_401("User is not authenticated")


class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    POST: Change password for users API
    """

    @change_password_schema
    def post(self, request):
        if request.user.is_authenticated:
            old_password = request.data.get("old_password")
            new_password = request.data.get("new_password")

            if is_none_or_empty(old_password) or is_none_or_empty(new_password):
                return get_error_response_400("Old password and new password cannot be empty")

            if not check_password(old_password, request.user.password):
                return get_error_response_401("The old password is incorrect")

            request.user.set_password(new_password)
            request.user.save()
            return get_success_response_200("Password updated successfully")

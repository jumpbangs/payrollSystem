from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from backend.helpers import is_none_or_empty
from backend.networkHelpers import (
    get_error_response_400,
    get_error_response_401,
    get_success_response_200,
)
from employee.models import Employee
from employee.serializers import EmployeeSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if is_none_or_empty(email) or is_none_or_empty(password):
            return get_error_response_400("Email and password cannot be empty")

        try:
            employee = Employee.objects.get(email=email)
            print(f" LOL ===> {employee.password} ")
            if employee is None:
                return get_error_response_401("The email is not registered")

            else:
                if not check_password(password, employee.password):
                    return get_error_response_401("The password is incorrect")

                login(request, employee)

                token, _ = Token.objects.get_or_create(user=employee)
                user_serialized_data = EmployeeSerializer(employee).data
                data = {"access_token": token.key, "user": user_serialized_data}
                return get_success_response_200(data)

        except Exception as exception:
            return get_error_response_401(str(exception))


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            logout(request)
            return get_success_response_200("Logout successful")
        else:
            return get_error_response_400("User is not authenticated")

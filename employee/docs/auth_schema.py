from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers

from employee.serializers import EmployeeSerializer


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


login_schema = extend_schema(
    request=LoginRequestSerializer,
    responses={
        200: EmployeeSerializer,
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Email and password cannot be empty\n"
                "- The email is not registered\n"
                "- The password is incorrect"
            )
        ),
    },
    description="Login endpoint",
    tags=["Auth"],
)

logout_schema = extend_schema(
    responses={
        200: OpenApiResponse(description="Logout successful"),
        401: OpenApiResponse(description="User is not authenticated"),
    },
    description="Logouts out user",
    tags=["Auth"],
)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)


change_password_schema = extend_schema(
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(description="Password updated successfully"),
        400: OpenApiResponse(description="Old password and new password cannot be empty"),
        401: OpenApiResponse(description="The old password is incorrect"),
    },
    description="Change password",
    tags=["Auth"],
)

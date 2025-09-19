from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers

from employee.serializers import EmployeeSerializer


class EmployeeRequestSerializer(serializers.Serializer):
    user_id = serializers.ListField(child=serializers.UUIDField(), allow_empty=False, help_text="List of user IDs")


get_employee_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="user_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            many=False,
            required=False,
            description="Fetch employee by ID else fetch all if there is none.",
        )
    ],
    responses={
        200: EmployeeSerializer(many=True),
        400: OpenApiResponse(description="Employee not found"),
        403: OpenApiResponse(description="Only admin and manager can fetch all employees"),
        404: OpenApiResponse(description="Employee not found"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Fetching employee data by id or fetch all",
    tags=["Employee"],
)

post_employee_schema = extend_schema(
    request=EmployeeSerializer(many=False),
    responses={
        200: OpenApiResponse(description="Employee added successfully"),
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Employee data cannot be empty\n"
                "- Employee email cannot be empty\n"
                "- Employee with this email already exists"
            )
        ),
        403: OpenApiResponse(description="Only admin and manager can fetch all employees"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Add new employee data",
    tags=["Employee"],
)


class UpdateEmployeeSchema(serializers.Serializer):
    employee_data = EmployeeSerializer(many=False)
    user_id = serializers.UUIDField(required=True)


patch_employee_schema = extend_schema(
    request=UpdateEmployeeSchema,
    responses={
        200: EmployeeSerializer,
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Employee data cannot be empty\n"
                "- Employee id cannot be empty\n"
                "- Employee data is invalid"
            )
        ),
        401: OpenApiResponse(
            description=(
                "Possible errors:\n- Only admin can update employee role\n- You are can only update your own profile\n"
            )
        ),
        500: OpenApiResponse(description="Server error"),
    },
    description="Update employee data by user_id",
    tags=["Employee"],
)


class DeleteEmployeeSchema(serializers.Serializer):
    user_id = serializers.UUIDField()


delete_employee_schema = extend_schema(
    request=DeleteEmployeeSchema,
    responses={
        200: OpenApiResponse(description="Employee deleted successfully"),
        400: OpenApiResponse(description="Employee id cannot be empty"),
        401: OpenApiResponse(description="Only admin can delete employee"),
        404: OpenApiResponse(description="Employee not found"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Delete employee by their user_id",
    tags=["Employee"],
)

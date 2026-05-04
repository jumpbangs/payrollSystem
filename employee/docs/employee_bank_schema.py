from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers

from employee.serializers import EmployeeBankDetailSerializer

EMPLOYEE_BANK_TAGS = "Employee Bank Details"

get_employee_bank_details_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="user_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            many=False,
            required=True,
            description="Employee to fetch bank details by user_id",
        ),
    ],
    responses={
        200: EmployeeBankDetailSerializer(many=False),
        400: OpenApiResponse(description="Employee id cannot be empty"),
        403: OpenApiResponse(description="Only admin and manager can fetch employee bank details"),
        404: OpenApiResponse(description="Employee not found"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Fetch employee bank details by their user_id",
    tags=[EMPLOYEE_BANK_TAGS],
)


class EmployeeBankDetailsRequestSchema(serializers.Serializer):
    employee_id = serializers.UUIDField(help_text="Employee to fetch bank details by user_id")
    tax_number = serializers.CharField(max_length=20, help_text="Tax number of the employee")
    bank_name = serializers.CharField(max_length=40, help_text="Bank name of the employee")
    bank_account_number = serializers.CharField(max_length=10, help_text="Account number of the employee")
    swift_code = serializers.CharField(max_length=11, help_text="SWIFT code of the employee's bank")
    provident_fund_number = serializers.CharField(max_length=20, help_text="Provident fund number of the employee")


post_employee_bank_details_schema = extend_schema(
    request=EmployeeBankDetailsRequestSchema,
    responses={
        200: OpenApiResponse(description="Employee bank details added successfully"),
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Employee bank details data cannot be empty\n"
                "- Employee with this id does not exist\n"
                "- Employee bank details for this employee already exist"
            ),
        ),
    },
    tags=[EMPLOYEE_BANK_TAGS],
)

patch_employee_bank_details_schema = extend_schema(
    request=EmployeeBankDetailsRequestSchema,
    responses={
        200: EmployeeBankDetailSerializer(many=False),
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Update bank details cannot not be empty"
                "- Employee ud cannot be empty"
                "- Only managers and admins are allowed to update employee bank details"
            ),
        ),
        500: OpenApiResponse("Exception updating employee's bank detail"),
    },
    tags=[EMPLOYEE_BANK_TAGS],
)

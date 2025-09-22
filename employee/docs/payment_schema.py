from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers

from employee.serializers import PaymentsSerializer

PAYMENT_TAG = "Employee Payment"

get_payment_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="employee_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            many=False,
            required=True,
            description="Fetch employee payment by employee_id",
        )
    ],
    responses={
        200: PaymentsSerializer,
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Employee payment doesn't exist for the given employee\n"
                "- Employee id is empty.\n"
                "- Only admins and users can fetch other/their user payment details"
            )
        ),
        500: OpenApiResponse(description="Server error"),
    },
    description="Fetch employee payment terms",
    tags=[PAYMENT_TAG],
)


class PostPaymentSchema(serializers.Serializer):
    employee_id = serializers.UUIDField()
    gross_salary = serializers.FloatField()
    net_salary = serializers.FloatField()
    tax = serializers.DecimalField(decimal_places=2, max_digits=10)


post_payment_schema = extend_schema(
    request=PostPaymentSchema,
    responses={
        200: PaymentsSerializer,
        400: OpenApiResponse(
            description="Possible errors:\n- Missing fields\n- Employee payment details exists\n- Serializer error"
        ),
        401: OpenApiResponse(description="Only admin and managers can add user payment detail"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Add payment details to user detail",
    tags=[PAYMENT_TAG],
)


class PatchPaymentSchema(PostPaymentSchema):
    last_payment = serializers.DateField()


patch_payment_schema = extend_schema(
    request=PatchPaymentSchema,
    responses={
        200: PaymentsSerializer,
        400: OpenApiResponse(description="Employee id is required"),
        401: OpenApiResponse(description="Only admin and managers can add user payment detail"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Update the user payment detail by the employee_id",
    tags=[PAYMENT_TAG],
)


class DeletePaymentSchema(serializers.Serializer):
    employee_id = serializers.UUIDField()


delete_payment_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="employee_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            many=False,
            required=False,
            description="Employee to delete by given employee_id.",
        )
    ],
    responses={
        200: OpenApiResponse(description="Employee's payment detail has been deleted"),
        400: OpenApiResponse(description="employee_id is required"),
        401: OpenApiResponse(description="Only admin and managers can delete user payment details"),
        404: OpenApiResponse(description="Given employee's payment detail does not exist"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Delete the user payment detail by employee_id",
    tags=[PAYMENT_TAG],
)

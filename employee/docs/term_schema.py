from drf_spectacular.utils import OpenApiResponse, extend_schema

from employee.serializers import EmploymentTermsSerializer

get_employee_term_schema = extend_schema(
    responses={
        200: EmploymentTermsSerializer(many=True),
        401: OpenApiResponse(description="Only admin and manager can fetch all employment terms"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Fetches employee terms",
    tags=["Employee"],
)

patch_employee_term_schema = extend_schema(
    request=EmploymentTermsSerializer(many=False),
    responses={
        200: EmploymentTermsSerializer(many=False),
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Employment term data cannot be empty\n"
                "- Employee id cannot be empty\n"
                "- Employment term data is invalid"
            )
        ),
        401: OpenApiResponse(description="Only admin and manager can update employment terms"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Update employee terms",
    tags=["Employee"],
)

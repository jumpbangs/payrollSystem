from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers

from worklogs.models import WorklogStatus, WorklogTypes
from worklogs.serializers import WorklogSerializer

WORKLOG_TAG = "Worklog"

get_worklog_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="worklog_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            many=True,
            required=False,
            description="Fetch worklog by id or fetch all",
        )
    ],
    responses={
        200: WorklogSerializer,
        404: OpenApiResponse(description="Worklog not found"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Fetch worklog by id or fetch all",
    tags=[WORKLOG_TAG],
)


class PostWorklogSchema(serializers.Serializer):
    job_id = serializers.UUIDField(required=True)
    employee_id = serializers.UUIDField(required=True)
    start_time = serializers.DateField(required=True)
    end_time = serializers.DateField(required=True)
    description = serializers.CharField(required=True)
    worklog_type = serializers.ChoiceField(choices=WorklogTypes.choices)
    break_time = serializers.DecimalField(required=False, decimal_places=2, max_digits=5)
    worklog_billed = serializers.BooleanField(required=False, default=False)
    worklog_approved = serializers.BooleanField(required=False, default=False)
    worklog_status = serializers.ChoiceField(choices=WorklogStatus.choices)


post_worklog_schema = extend_schema(
    request=PostWorklogSchema,
    responses={
        200: WorklogSerializer,
        400: OpenApiResponse(
            description="Possible errors:\n- Worklog data empty\n- Invalid worklog data\n- MIssing fields"
        ),
        500: OpenApiResponse(description="Server error"),
    },
    description="Creating new worklog",
    tags=[WORKLOG_TAG],
)


class PatchWorklogSchema(PostWorklogSchema):
    worklog_id = serializers.UUIDField(required=True)


patch_worklog_schema = extend_schema(
    request=PatchWorklogSchema,
    responses={
        200: WorklogSerializer,
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Worklog data is empty\n"
                "- Worklog id is required\n"
                "- Worklog does not belong to the user"
            )
        ),
        404: OpenApiResponse(description="Invalid worklog id"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Update worklog given by worklog_id",
    tags=[WORKLOG_TAG],
)


class DeleteWorklogSchema(serializers.Serializer):
    worklog_id = serializers.UUIDField()


delete_worklog_schema = extend_schema(
    request=DeleteWorklogSchema,
    responses={
        200: OpenApiResponse(description="Worklog deleted"),
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Worklog_id is required\n"
                "- Only managers, admin or the owner can delete the following worklog\n"
                "- Worklog_id is invalid"
            )
        ),
        500: OpenApiResponse(description="Server error"),
    },
    description="Delete the given worklog by the worklog_id",
    tags=[WORKLOG_TAG],
)

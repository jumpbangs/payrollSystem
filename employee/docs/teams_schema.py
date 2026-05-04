from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers

from employee.serializers import TeamDetailSerializer

TEAMS_TAGS = "Team"

get_teams_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="team_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            many=False,
            required=False,
            description="Fetch teams by ID else fetch all if there is no ID",
        ),
    ],
    responses={
        200: TeamDetailSerializer(),
        400: OpenApiResponse(
            description=(
                "Possible errors:\n- Only upper management are allow to fetch teams- Following team does not exist"
            ),
        ),
        500: OpenApiResponse(description="Exception when fetching team detail"),
    },
    tags=[TEAMS_TAGS],
)


class TeamRequestSerializer(serializers.Serializer):
    team_name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(required=True)
    members = serializers.ListField(child=serializers.UUIDField(), allow_empty=True, help_text="List of Users ID")


post_teams_schema = extend_schema(
    request=TeamRequestSerializer(),
    responses={
        201: TeamDetailSerializer(many=False),
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Only upper management are allow to create teams"
                "- Team with the same name already exists"
                "- Failed to create team"
            ),
        ),
        500: OpenApiResponse(description="Exception when creating team"),
    },
    tags=[TEAMS_TAGS],
)


class PatchTeamRequestSerializer(TeamRequestSerializer):
    # Override fields to make them optional for PATCH operations
    team_id = serializers.UUIDField(required=True)
    team_name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(required=False)
    members = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=True,
        required=False,
        help_text="List of Users ID",
    )


patch_teams_schema = extend_schema(
    request=PatchTeamRequestSerializer(),
    responses={
        200: TeamDetailSerializer(many=False),
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Only upper management are allowed to update teams\n"
                "- Team does not exist\n"
                "- Team with the same name already exists\n"
                "- Invalid member IDs provided"
            ),
        ),
        500: OpenApiResponse(description="Exception when updating team"),
    },
    tags=[TEAMS_TAGS],
)


delete_teams_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="team_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            required=True,
            description="ID of the team to delete team",
        ),
    ],
    responses={
        200: OpenApiResponse(description="Team has been deleted"),
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Only upper management are allowed to delete teams\n"
                "- Team id cannot be empty\n"
                "- Team has been deleted\n"
                "- Following team does not exist"
            ),
        ),
        500: OpenApiResponse(description="Exception when deleting team"),
    },
)

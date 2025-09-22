from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers

from locations.serializers import CountrySerializer

COUNTRY_TAGS = "Country"

get_country_schema = extend_schema(
    responses={200: CountrySerializer(many=True), 500: OpenApiResponse(description="Server error")},
    description="Fetch all countries",
    tags=[COUNTRY_TAGS],
)


post_country_schema = extend_schema(
    request=CountrySerializer,
    responses={
        200: CountrySerializer,
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Country data cannot be empty\n"
                "- Country name cannot be empty\n"
                "- Country code cannot be empty\n"
                "- Country with this name already exists\n"
                "- Country data is invalid"
            )
        ),
        401: OpenApiResponse(description="Only admin and manager can add new countries"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Add new country",
    tags=[COUNTRY_TAGS],
)


class PutCountrySchema(serializers.Serializer):
    country_id = serializers.UUIDField()
    country_name = serializers.CharField()
    country_code = serializers.CharField()
    phone_code = serializers.CharField()
    currency = serializers.CharField()


put_country_schema = extend_schema(
    request=PutCountrySchema,
    responses={
        200: CountrySerializer,
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Country data cannot be empty\n"
                "- Country id cannot be empty\n"
                "- Country data is invalid"
            )
        ),
        401: OpenApiResponse(description="Only admin and manager can update countries"),
        404: OpenApiResponse(description="Country not found or doesn't exist"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Update country by country_id",
    tags=[COUNTRY_TAGS],
)

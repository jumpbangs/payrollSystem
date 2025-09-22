from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)

from locations.serializers import CitySerializer

CITY_TAG = "City"

get_city_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="city_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            many=True,
            required=False,
            description="Fetch city by city_id or fetch all",
        )
    ],
    responses={200: CitySerializer, 500: OpenApiResponse(description="Server error")},
    description="Fetch city by city_id or fetch all",
    tags=[CITY_TAG],
)

post_city_schema = extend_schema(
    request=CitySerializer,
    responses={
        200: CitySerializer,
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- City data cannot be empty\n"
                "- City name cannot be empty\n"
                "- State cannot be empty\n"
                "- City with this name already exists\n"
                "- City data is invalid"
            )
        ),
        401: OpenApiResponse(description="Only admin and manager can add new cities"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Adding a new city location",
    tags=[CITY_TAG],
)

update_city_schema = extend_schema(
    request=CitySerializer,
    responses={
        200: CitySerializer,
        400: OpenApiResponse(
            description=(
                "Possible errors:\n- City data cannot be empty\n- City id cannot be empty\n- City data is invalid"
            )
        ),
        401: OpenApiResponse(description="Only admin and manager can update cities"),
        404: OpenApiResponse(description="City not found or doesn't exist"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Update city location by city_id",
    tags=[CITY_TAG],
)

delete_city_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="city_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            many=False,
            required=False,
            description="Delete city by the given city_id.",
        )
    ],
    responses={
        200: OpenApiResponse(description="City deleted successfully"),
        400: OpenApiResponse(description="City id cannot be empty"),
        401: OpenApiResponse(description="only admin and manager can delete cities"),
        404: OpenApiResponse(description="City not found"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Delete city location by city_id",
    tags=[CITY_TAG],
)

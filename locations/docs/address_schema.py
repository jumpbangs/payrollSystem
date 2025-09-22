from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers

from locations.serializers import AddressSerializer

ADDRESS_TAG = "Address"

get_address_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="address_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            many=False,
            required=False,
            description="Fetch address by address_id",
        )
    ],
    responses={
        200: AddressSerializer,
        404: OpenApiResponse(description="Address not found or doesn't exit"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Fetch address by id or fetch all",
    tags=[ADDRESS_TAG],
)

post_address_schema = extend_schema(
    request=AddressSerializer,
    responses={
        200: AddressSerializer,
        400: OpenApiResponse(
            description=(
                "Possible errors:\n"
                "- Address data cannot be empty\n"
                "- Employee cannot be empty\n"
                "- City id cannot be empty\n"
                "- country id cannot be empty\n"
                "- Address data is invalid"
            )
        ),
        401: OpenApiResponse(description="Only admin and manager can add new addresses"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Adding new address",
    tags=[ADDRESS_TAG],
)


class PutAddressSchema(serializers.Serializer):
    address_id = serializers.UUIDField()
    address = serializers.CharField()
    address_data = AddressSerializer


put_address_schema = extend_schema(
    request=PutAddressSchema,
    responses={
        200: AddressSerializer,
        400: OpenApiResponse(
            description=(
                "Possible errors:\n- Address cannot be empty\n- Address id cannot be empty\n- Address data is invalid"
            )
        ),
        401: OpenApiResponse(description="Only admin and manager can update addresses"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Update address",
    tags=[ADDRESS_TAG],
)


class DeleteAddressSchema(serializers.Serializer):
    address_id = serializers.UUIDField()


delete_address_schema = extend_schema(
    request=DeleteAddressSchema,
    responses={
        200: OpenApiResponse(description="Address deleted successfully"),
        400: OpenApiResponse(
            description=(
                "Possible errors:\n- Address not found\n- Address data cannot be empty\n- Address cannot be empty"
            )
        ),
        401: OpenApiResponse(description="Only admin and manager can delete addresses"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Delete address by given address_id",
    tags=[ADDRESS_TAG],
)

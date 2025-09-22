from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import serializers

from worklogs.serializers import ClientSerializer

CLIENT_TAG = "Client"

get_client_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="client_id",
            type=OpenApiTypes.UUID,
            location=OpenApiParameter.QUERY,
            many=True,
            required=False,
            description="Fetch client by id or fetch all",
        )
    ],
    responses={
        200: ClientSerializer,
        400: OpenApiResponse(description="Client does not exist"),
        500: OpenApiResponse(description="Server error"),
    },
    tags=[CLIENT_TAG],
)

post_client_schema = extend_schema(
    request=ClientSerializer,
    responses={
        200: ClientSerializer,
        400: OpenApiResponse(
            description="Possible errors:\n- Client already exists\n- Missing fields\n- Invalid client data"
        ),
        401: OpenApiResponse(description="Only managers and admins can add client data"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Add client details",
    tags=[CLIENT_TAG],
)


class PatchClientSchema(serializers.Serializer):
    client_id = serializers.UUIDField(required=True)
    client_details = ClientSerializer()


patch_client_schema = extend_schema(
    request=PatchClientSchema,
    responses={
        200: ClientSerializer,
        400: OpenApiResponse(
            description="Possible errors:\n- Client data is invalid \n- Given client_id does not exist"
        ),
        401: OpenApiResponse(description="Only admin and manager can update client"),
        500: OpenApiResponse(description="Server error"),
    },
    description="Update client with the given client_id",
    tags=[CLIENT_TAG],
)

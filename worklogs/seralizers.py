from rest_framework import serializers

from .models import Clients


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = [
            "id",
            "client_name",
            "client_email",
            "client_contact",
            "client_details",
            "client_address",
            "last_invoiced",
        ]


class ClientMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ["id", "client_name", "client_name"]

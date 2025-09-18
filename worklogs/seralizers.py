from rest_framework import serializers

from locations.serializers import AddressSerializer

from .models import Clients, Jobs


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = [
            "id",
            "client_name",
            "client_email",
            "client_contact",
            "client_address",
            "last_invoiced",
            "is_client_active",
        ]

    def to_representation(self, instance):
        client_data = super().to_representation(instance)
        address = instance.client_address
        client_data["client_address"] = AddressSerializer(address).data if address else None
        return client_data


class ClientMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ["id", "client_name", "client_name"]


class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = "__all__"


# class WorklogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Worklog

from rest_framework import serializers

from .models import Clients, WorklogDetails


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


class WorklogDetailSerializer(serializers.ModelSerializer):
    client_profile = serializers.SerializerMethodField()

    class Meta:
        model = WorklogDetails
        fields = [
            "id",
            "rate",
            "client_id",
            "job_detail",
            "billed_hours",
            "client_profile",
            "approved_hours",
            "additional_details",
        ]

    def get_client_profile(self, obj):
        if obj.client_id:
            return ClientMinSerializer(obj.client_id).data
        return None

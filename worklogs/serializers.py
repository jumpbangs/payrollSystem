from rest_framework import serializers

from employee.serializers import EmployeeMinSerializer
from locations.serializers import AddressSerializer

from .models import Clients, Jobs, Worklogs


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
class JobSerializer(serializers.ModelSerializer):
    client_profile = serializers.SerializerMethodField()

    class Meta:
        model = Jobs
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


class WorklogMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worklogs
        fields = [
            "id",
            "worklog_status",
            "worklog_type",
            "break_time",
            "start_time",
            "end_time",
            "worklog_type",
            "worklog_date",
        ]


class WorklogSerializer(serializers.ModelSerializer):
    employee_details = serializers.SerializerMethodField()
    job_details = serializers.SerializerMethodField()

    class Meta:
        model = Worklogs
        fields = [
            "id",
            "job_id",
            "employee_id",
            "worklog_date",
            "start_time",
            "end_time",
            "break_time",
            "description",
            "worklog_billed",
            "worklog_approved",
            "worklog_type",
            "worklog_status",
            "employee_details",
            "job_details",
        ]

    def get_employee_details(self, obj):
        if obj.employee_id:
            return EmployeeMinSerializer(obj.employee_id).data
        return None

    def get_job_details(self, obj):
        if obj.job_id:
            return JobSerializer(obj.job_id).data
        return None

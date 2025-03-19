from rest_framework import serializers

from employee.serializers import EmployeeMinSerializer

from .models import Clients, WorklogDetails, Worklogs


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
    worklog_details = serializers.SerializerMethodField()

    class Meta:
        model = Worklogs
        fields = [
            "id",
            "employee_id",
            "worklog_detail_id",
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
            "worklog_details",
        ]

    def get_employee_details(self, obj):
        if obj.employee_id:
            return EmployeeMinSerializer(obj.employee_id).data
        return None

    def get_worklog_details(self, obj):
        if obj.worklog_detail_id:
            return WorklogDetailSerializer(obj.worklog_detail_id).data
        return None

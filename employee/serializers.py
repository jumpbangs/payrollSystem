from rest_framework import serializers

from .models import Employee, EmploymentStatus


class EmployeeSerializer(serializers.ModelSerializer):
    employment_status = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "date_of_birth",
            "job_title_id",
            "department_id",
            "gender",
            "employee_status",
            "employment_status",
            "address",
            "city_id",
            "email",
            "employment_start",
            "contact_number",
        ]

    def get_employment_status(self, obj):
        return f"{obj.employee_status}"


class EmploymentStatusSerializer(serializers.ModelSerializer):
    employmentStatus = serializers.SerializerMethodField()
    employmentType = serializers.SerializerMethodField()

    class Meta:
        model = EmploymentStatus
        fields = [
            "id",
            "status",
            "employment_term",
            "employment_type",
            "employmentType",
            "employmentStatus",
        ]

    def get_employmentType(self, obj):
        return f"{obj.get_employment_type_display()}"

    def get_employmentStatus(self, obj):
        return f"{obj.get_status_display()}"

from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "employment_type",
            "email",
            "employment_start",
            "contact_number",
            "user_role",
            "is_staff",
            "is_active",
        ]

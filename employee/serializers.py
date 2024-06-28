from rest_framework import serializers

from .models import Employee, EmploymentTerms, Payments


class EmployeeSerializer(serializers.ModelSerializer):
    employment_term = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "date_of_birth",
            "employment_type",
            "email",
            "employment_start",
            "contact_number",
            "user_role",
            "is_staff",
            "is_active",
            "employment_term",
            "payment",
        ]

    def get_employment_term(self, obj):
        try:
            employment_term_obj = EmploymentTerms.objects.get(employee_id=obj.user_id)
            serialized_data = EmploymentTermsSerializer(employment_term_obj).data
            serialized_data.pop("employee_details")
            return serialized_data
        except Exception:
            return {}

    def get_payment(self, obj):
        try:
            payment_obj = Payments.objects.get(employee_id=obj.user_id)
            return PaymentsSerializer(payment_obj).data
        except Exception:
            return {}


class EmployeeMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "employment_type",
            "user_role",
            "is_staff",
            "is_active",
        ]


class EmploymentTermsSerializer(serializers.ModelSerializer):
    employee_details = serializers.SerializerMethodField()

    class Meta:
        model = EmploymentTerms
        fields = [
            "employee_details",
            "leave_days",
            "sick_days",
            "agreed_salary",
            "start_date",
            "end_date",
            "employee_id",
        ]

    def get_employee_details(self, obj):
        try:
            employee_obj = Employee.objects.get(user_id=obj.employee_id.user_id)
            serialized_data = EmployeeMinSerializer(employee_obj).data
            return serialized_data
        except Exception:
            return {}


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ["gross_salary", "tax", "net_salary", "last_payment", "employee_id"]

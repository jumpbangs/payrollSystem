from django.contrib import admin

from .models import Employee, EmploymentTerms, Payments


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user_id", "first_name", "last_name", "user_role", "employment_type")
    search_fields = ("user_id", "first_name", "last_name", "user_role", "employment_type")


class EmployeeTermsAdmin(admin.ModelAdmin):
    list_display = ("id", "get_employee_name", "leave_days", "sick_days")
    search_fields = ("id", "employee_id__first_name")

    def get_employee_name(self, obj):
        last_name = obj.employee_id.last_name if obj.employee_id.last_name != None else " "
        full_name = obj.employee_id.first_name + " " + last_name
        return full_name


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ("id", "get_employee_name", "employee_id")
    search_fields = ("id", "employee_id__first_name", "employee_id_last_name", "employee_id")

    def get_employee_name(self, obj):
        last_name = obj.employee_id.last_name if obj.employee_id.last_name != None else " "
        full_name = obj.employee_id.first_name + " " + last_name
        return full_name


# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmploymentTerms, EmployeeTermsAdmin)
admin.site.register(Payments, PaymentsAdmin)

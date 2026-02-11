from django.contrib import admin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .models import (
    Employee,
    EmployeeBankDetails,
    EmploymentTerms,
    Payments,
    TeamMembers,
    Teams,
)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user_id", "first_name", "last_name", "user_role", "employment_type")
    search_fields = ("user_id", "first_name", "last_name", "user_role", "employment_type")
    exclude = ("groups", "user_permissions")


class EmployeeTermsAdmin(admin.ModelAdmin):
    list_display = ("id", "get_employee_name", "leave_days", "sick_days")
    search_fields = ("id", "employee_id__first_name")

    def get_employee_name(self, obj):
        last_name = obj.employee_id.last_name if obj.employee_id.last_name != None else " "
        full_name = obj.employee_id.first_name + " " + last_name
        return full_name

    get_employee_name.short_description = "Employee Name"


class EmployeeBankDetailsAdmin(admin.ModelAdmin):
    list_display = ("id", "get_employee_name", "bank_name")
    search_fields = ("id", "employee_id__first_name")

    def get_employee_name(self, obj):
        last_name = obj.employee_id.last_name if obj.employee_id.last_name != None else " "
        full_name = obj.employee_id.first_name + " " + last_name
        return full_name

    get_employee_name.short_description = "Employee Name"


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ("id", "get_employee_name", "employee_id")
    search_fields = ("id", "employee_id__first_name", "employee_id__last_name", "employee_id")

    def get_employee_name(self, obj):
        last_name = obj.employee_id.last_name if obj.employee_id.last_name != None else " "
        full_name = obj.employee_id.first_name + " " + last_name
        return full_name

    get_employee_name.short_description = "Employee Name"


class TeamsAdmin(admin.ModelAdmin):
    list_display = ("team_id", "team_name", "description")
    search_fields = ("team_id", "team_name", "team_members__first_name", "team_members__last_name")


class TeamMembersAdmin(admin.ModelAdmin):
    list_display = ("get_member_name", "get_team_name")
    search_fields = ("member__first_name", "member__last_name", "team__team_name")

    def get_team_name(self, obj):
        return obj.team.team_name

    def get_member_name(self, obj):
        return f"{obj.member.first_name} {obj.member.last_name}"

    get_team_name.short_description = "Team"
    get_member_name.short_description = "Member Name"


# Hide Token and Groups from the Admin Panel
admin.site.unregister(TokenProxy)
admin.site.unregister(Group)

# Register your models here.
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(EmploymentTerms, EmployeeTermsAdmin)
admin.site.register(Payments, PaymentsAdmin)
admin.site.register(EmployeeBankDetails, EmployeeBankDetailsAdmin)
admin.site.register(Teams, TeamsAdmin)
admin.site.register(TeamMembers, TeamMembersAdmin)

from django.contrib import admin

from .models import Employee, EmploymentStatus, EmploymentTerms, Payments

# Register your models here.
admin.site.register(Employee)
admin.site.register(EmploymentStatus)
admin.site.register(EmploymentTerms)
admin.site.register(Payments)
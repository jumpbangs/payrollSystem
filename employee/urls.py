from django.urls import path

from employee.views.EmployeeViews import EmployeeModelView
from employee.views.EmploymentStatusView import (
    EmploymentStatusModelView,
    EmploymentTypeModelView,
    JobTitlesModelView,
)

urlpatterns = [
    path("employee", EmployeeModelView.as_view()),
    path("employment/status", EmploymentStatusModelView.as_view()),
    path("employment/types", EmploymentTypeModelView.as_view()),
    path("employment/titles", JobTitlesModelView.as_view()),
]

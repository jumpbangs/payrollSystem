from django.urls import path

from employee.views.EmployeeViews import EmployeeModelView

urlpatterns = [
    path("employee", EmployeeModelView.as_view()),
]

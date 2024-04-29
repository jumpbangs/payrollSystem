from django.urls import path

from employee.views.AuthView import LoginView, LogoutView
from employee.views.EmployeeViews import EmployeeModelView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("employee", EmployeeModelView.as_view()),
]

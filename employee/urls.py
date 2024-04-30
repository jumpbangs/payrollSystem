from django.urls import path

from employee.views.AuthView import ChangePasswordView, LoginView, LogoutView
from employee.views.EmployeeViews import EmployeeModelView, EmploymentTermsView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("employee/", EmployeeModelView.as_view()),
    path("employee/terms/", EmploymentTermsView.as_view()),
]

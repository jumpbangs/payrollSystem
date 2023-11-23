from django.urls import path

from worklogs.views.ClientView import ClientModelView
from worklogs.views.WorklogView import WorklogDetailModelView, WorklogModelView

urlpatterns = [
    path('clients', ClientModelView.as_view()),
    path('worklogs', WorklogModelView.as_view()),
    path('worklog/detail', WorklogDetailModelView.as_view()),
]
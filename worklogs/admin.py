from django.contrib import admin

from .models import Clients, WorklogDetails, Worklogs

# Register your models here.
admin.site.register(Worklogs)
admin.site.register(WorklogDetails)
admin.site.register(Clients)

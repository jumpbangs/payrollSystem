from django.contrib import admin

from .models import Clients, Jobs, Worklogs

# Register your models here.
admin.site.register(Worklogs)
admin.site.register(Jobs)
admin.site.register(Clients)

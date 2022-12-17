from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
# Register your models here.
admin.site.register(Status)
admin.site.register(Cities)
admin.site.register(Fount)
admin.site.register(AccountReport)
admin.site.register(Companies)
admin.site.unregister(Group)

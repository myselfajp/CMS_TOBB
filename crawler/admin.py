from django.contrib.auth.models import Group
from django.contrib import admin
from .models import *


class CompaniesAdmin(admin.ModelAdmin):
    list_filter = ('user','city','last_status','sector')
    search_fields = ['name','address']

class MyModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

admin.site.register(AccountReport, MyModelAdmin)

# Register your models here.
admin.site.register(Status)
admin.site.register(Cities)
admin.site.register(Fount)
# admin.site.register(AccountReport)
admin.site.register(Companies,CompaniesAdmin)
admin.site.unregister(Group)

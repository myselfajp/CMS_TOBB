from django.contrib.auth.models import Group
from django.contrib import admin
from .models import *


class PhoneStartsWithFiveFilter(admin.SimpleListFilter):
    title = "cep"
    parameter_name = 'phone_startswith'

    def lookups(self, request, model_admin):
        return [
            ('5', 'شماره موبایل'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '5':
            return queryset.filter(phone__startswith='5')
        return queryset

class PersonelCountFilter(admin.SimpleListFilter):
    title = 'Personel Sayısı'
    parameter_name = 'personels_caount'

    def lookups(self, request, model_admin):
        return [
            ('0_20', '0 - 20'),
            ('21_100', '21 - 100'),
            ('101_500', '101 - 500'),
            ('500_plus', '500+'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == '0_20':
            return queryset.filter(personels_caount__gte=0, personels_caount__lte=20)
        elif value == '21_100':
            return queryset.filter(personels_caount__gte=21, personels_caount__lte=100)
        elif value == '101_500':
            return queryset.filter(personels_caount__gte=101, personels_caount__lte=500)
        elif value == '500_plus':
            return queryset.filter(personels_caount__gte=501)
        return queryset



class CompaniesAdmin(admin.ModelAdmin):
    list_filter = ('user','city','last_status',PersonelCountFilter,PhoneStartsWithFiveFilter)
    search_fields = ['name','address']



class AzexportAdmin(admin.ModelAdmin):
    list_filter = ('is_verified','fount')
    search_fields = ['name','address','tel','phone']

# class MyModelAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         """
#         Return empty perms dict thus hiding the model from admin index.
#         """
#         return {}

# admin.site.register(AccountReport, MyModelAdmin)

# Register your models here.
admin.site.register(Status)
admin.site.register(Cities)
admin.site.register(Fount)
admin.site.register(Agreement)
admin.site.register(AgreementStatus)
admin.site.register(AccountReport)
admin.site.register(GoogleSearchReport)
admin.site.register(Companies,CompaniesAdmin)
admin.site.register(Permision)
admin.site.register(Azexport,AzexportAdmin)
admin.site.unregister(Group)

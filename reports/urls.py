from django.urls import path
from .views import http_companies,http_company

app_name="reports"

urlpatterns = [
    path("companies",http_companies,name='companies'),
    path("company-<int:company_id>",http_company,name='company'),

]

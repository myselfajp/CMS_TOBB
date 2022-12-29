from django.urls import path
from .views import http_companies,http_company,http_test_send_mail

app_name="reports"

urlpatterns = [
    path("companies",http_companies,name='companies'),
    path("company-<int:company_id>",http_company,name='company'),
    path("Sendmail",http_test_send_mail,name='Sendmail'),
]

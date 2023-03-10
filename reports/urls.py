from django.urls import path
from .views import *

app_name="reports"

urlpatterns = [
    path("azerbaycan_ihracat-<int:company_id>",http_company_azexport,name='company_azexport'),
    path("azerbaycan_ihracat",http_azexport,name='companies_azexport'),
    path("company-<int:company_id>",http_company,name='company'),
    path("companies",http_companies,name='companies'),
    path("sendmail",http_send_mail,name='sendmail'),
    path("reminder<int:company_id>",http_reminder,name='reminder'),
    path("reminder_report",http_reminder_report,name='reminder_report'),
    path("agreement-<int:company_id>",http_send_agreement,name='agreement'),
    path("agreement_report",http_report_agreement,name='report_agreement'),
    path("agreement_admin-<int:agreement_id>",http_report_agreement_admin,name='agreement_admin'),
    path("azerbaycan",http_azerbaycan,name='azerbaycan'),
]

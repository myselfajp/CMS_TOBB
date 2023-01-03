from django.urls import path
from .views import http_companies,http_company,http_send_mail,http_reminder,http_reminder_report

app_name="reports"

urlpatterns = [
    path("companies",http_companies,name='companies'),
    path("company-<int:company_id>",http_company,name='company'),
    path("sendmail",http_send_mail,name='sendmail'),
    path("reminder<int:company_id>",http_reminder,name='reminder'),
    path("reminder_report",http_reminder_report,name='reminder_report'),


]

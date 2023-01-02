from django.urls import path
from .views import http_companies,http_company,http_send_mail,http_reminder

app_name="reports"

urlpatterns = [
    path("companies",http_companies,name='companies'),
    path("company-<int:company_id>",http_company,name='company'),
    path("sendmail",http_send_mail,name='sendmail'),
    path("reminder<int:company_id>",http_reminder,name='reminder'),

]

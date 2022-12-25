from django.urls import path
from .views import http_login

app_name="users"

urlpatterns = [
    path("",http_login,name='login'),

]

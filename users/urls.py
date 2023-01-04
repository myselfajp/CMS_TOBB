from django.urls import path
from .views import http_login,http_share,http_logout

app_name="users"

urlpatterns = [
    path("accounts/login/",http_login,name='login'),
    path("",http_login,name='login'),
    path("logout",http_logout,name='logout'),
    path("share",http_share,name='share'),
]

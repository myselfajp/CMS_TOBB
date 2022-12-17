from django.urls import path
from .views import http_crawler_tobb,login

app_name="crawler"

urlpatterns = [
    path("crawler-<int:city_slug>",http_crawler_tobb,name='tobb'),
    path("login",login),

]

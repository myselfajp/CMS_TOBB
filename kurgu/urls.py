from django.urls import path
from .views import *

app_name="kurgu"

urlpatterns = [
    path("kj_kurgu",http_kj_kurgu,name='kj_kurgu'),
    path("kj_muhasebe",http_kj_muhasebe,name='kj_muhasebe'),
]

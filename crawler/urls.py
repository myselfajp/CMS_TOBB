from django.urls import path
from .views import http_crawler_tobb,http_crawler_google,http_excel,http_azexport,http_azerbaycan_yp,Http_firmaTurkiye
app_name="crawler"

urlpatterns = [
    path("crawler-<int:city_slug>",http_crawler_tobb,name='tobb'),
    path("crawler2-<str:city_slug>",Http_firmaTurkiye,name='firmaturkiye'),
    path("crawler_google",http_crawler_google,name='google_map_crawler'),
    path("excel-<int:city_slug>",http_excel,name='excel'),
    path("azexport-<int:city_slug>",http_azexport,name='azexport'),
    path("azerbaycanyp-<int:city_slug>",http_azerbaycan_yp,name='azerbaycanyp'),


]

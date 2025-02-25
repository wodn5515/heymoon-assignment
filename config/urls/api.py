from django.urls import path, include
from apps.accounts.urls import urlpatterns as accounts_urls
from apps.dashboards.urls import urlpatterns as dashboards_urls

urlpatterns = accounts_urls + dashboards_urls

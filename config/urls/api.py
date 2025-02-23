from django.urls import path, include
from apps.accounts.urls import urlpatterns as accounts_urls

urlpatterns = [accounts_urls]

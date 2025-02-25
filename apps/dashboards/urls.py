from django.urls import path
from apps.dashboards.views.dashboards import LiveSalesAPIView

urlpatterns = [
    path("live-sales", LiveSalesAPIView.as_view(), name="live-sales"),
]

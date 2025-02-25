from django.urls import path
from apps.dashboards.views.dashboards import (
    LiveSalesAPIView,
    SalesChartAPIView,
)

urlpatterns = [
    path("live-sales", LiveSalesAPIView.as_view(), name="live-sales"),
    path("sales-chart", SalesChartAPIView.as_view(), name="sales-chart"),
]

from django.urls import path
from apps.dashboards.views.dashboards import (
    LiveSalesAPIView,
    SalesChartAPIView,
)

urlpatterns = [
    path("dashboards/live-sales", LiveSalesAPIView.as_view(), name="live-sales"),
    path("dashboards/sales-chart", SalesChartAPIView.as_view(), name="sales-chart"),
]

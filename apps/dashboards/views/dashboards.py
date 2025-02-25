from datetime import datetime
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from apps.dashboards.validations.dashboards import DateRangeEntity
from apps.dashboards.validations import exceptions
from apps.dashboards.validations import exception_data
from apps.dashboards.services.dashboards import (
    LiveSalesService,
    SalesChartService,
)
from apps.utils import exception_data as common_exception_data
from apps.utils import exceptions as response_exceptions


class LiveSalesAPIView(APIView):
    permission_classes = [
        IsAdminUser,
    ]

    def get(self, request, *args, **kwargs):
        start_date = self.request.GET.get("start-date")
        end_date = self.request.GET.get("end-date", datetime.now())
        request_data = {"start_date": start_date, "end_date": end_date}

        # validate
        try:
            data = DateRangeEntity(**request_data)
        except ValidationError:
            raise response_exceptions.BadRequest(
                **common_exception_data.HTTP_400_INPUT_VALIDATION_ERROR
            )

        # service
        try:
            live_sales_service = LiveSalesService()
            response_data = live_sales_service.get_live_sales(data)
        except exceptions.DateRangeNotValid:
            raise response_exceptions.BadRequest(
                **exception_data.HTTP_400_INVALID_DATE_RANGE
            )

        return Response(status=status.HTTP_200_OK, data=response_data)


class SalesChartAPIView(APIView):
    permission_classes = [
        IsAdminUser,
    ]

    def get(self, request, *args, **kwargs):
        start_date = self.request.GET.get("start-date")
        end_date = self.request.GET.get("end-date", datetime.now())
        request_data = {"start_date": start_date, "end_date": end_date}

        # validate
        try:
            data = DateRangeEntity(**request_data)
        except ValidationError:
            raise response_exceptions.BadRequest(
                **common_exception_data.HTTP_400_INPUT_VALIDATION_ERROR
            )

        # service
        try:
            sales_chart_service = SalesChartService()
            response_data = sales_chart_service.get_sales_chart(data)
        except exceptions.DateRangeNotValid:
            raise response_exceptions.BadRequest(
                **exception_data.HTTP_400_INVALID_DATE_RANGE
            )

        return Response(status=status.HTTP_200_OK, data=response_data)

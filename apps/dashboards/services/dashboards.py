from apps.dashboards.validations.dashboards import DateRangeEntity
from django.db.models import Count, Sum, Case, When, Value, F
from django.db.models.functions import TruncHour
from apps.orders.models import Order


class LiveSalesService:
    def get_live_sales(self, data: DateRangeEntity):
        queryset = self._get_queryset(data)
        response_data = self._response_data_serializer(queryset)
        return response_data

    def _get_queryset(self, data: DateRangeEntity):
        # 1시간 단위로 데이터 집계
        sales_data = (
            Order.objects.filter(
                payment_date__gte=data.start_date,
                payment_date__lte=data.end_date,
                status__in=["PAID", "SHIPPING", "COMPLETED"],  # 결제 완료된 주문만
            )
            .annotate(hour=TruncHour("payment_date"))
            .values("hour")
            .annotate(
                total_amount=Sum("total_price"),  # 결제액
                customer_count=Count("user", distinct=True),  # 결제자 수
                first_purchase_count=Count(
                    Case(
                        When(is_first_purchase=True, then="user"),
                    ),
                    distinct=True,
                ),  # 첫 구매 수
                first_purchase_amount=Sum(
                    Case(
                        When(is_first_purchase=True, then="total_price"),
                        default=Value(0),
                    )
                ),  # 첫 구매액
                coupon_amount=Sum("discount_price"),  # 쿠폰 할인금액
            )
            .order_by("hour")
        )
        return sales_data

    def _response_data_serializer(self, queryset) -> dict:
        response_data = {
            "results": [self._object_serializer(object) for object in queryset]
        }
        return response_data

    def _object_serializer(self, object) -> dict:
        data = {
            "datetime": object["hour"].strftime("%Y-%m-%d %H:00"),
            "total_amount": object["total_amount"] or 0,
            "customer_count": object["customer_count"] or 0,
            "coupon_amount": object["coupon_amount"] or 0,
            "first_purchase_count": object["first_purchase_count"] or 0,
            "first_purchase_amount": object["first_purchase_amount"] or 0,
        }
        return data


class SalesChartService:
    def get_sales_chart(self, data: DateRangeEntity):
        queryset = self._get_queryset(data)
        response_data = self._response_data_serializer(queryset)
        return response_data

    def _get_queryset(self, data: DateRangeEntity):
        sales_data = (
            Order.objects.filter(
                payment_date__gte=data.start_date,
                payment_date__lte=data.end_date,
                status__in=["PAID", "SHIPPING", "COMPLETED"],  # 결제 완료된 주문만
            )
            .annotate(hour=TruncHour("payment_date"))
            .values("items__product__name")
            .annotate(
                product_name=F("items__product__name"),
                quantity=Sum("items__quantity"),  # 판매수량
                total_amount=Sum(
                    F("items__quantity")
                    * (
                        F("items__product__price")
                        + F("items__product_option__additional_price")
                    )
                ),  # 판매금액
            )
            .values("product_name", "quantity", "total_amount")
            .order_by("-quantity")
        )[:10]
        return sales_data

    def _response_data_serializer(self, queryset) -> dict:
        response_data = {
            "results": [self._object_serializer(object) for object in queryset]
        }
        return response_data

    def _object_serializer(self, object) -> dict:
        data = {
            "product_name": object["product_name"] or "",
            "total_amount": object["total_amount"] or 0,
            "quantity": object["quantity"] or 0,
        }
        return data

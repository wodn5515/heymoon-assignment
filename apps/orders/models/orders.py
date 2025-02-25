from django.db import models
from apps.common.models import TimeStampedModel


class OrderAddress(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="order_addresses",
        null=True,
    )
    address = models.CharField(max_length=255)
    detail_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5)
    is_default = models.BooleanField(default=False)
    memo = models.TextField(null=True)

    class Meta:
        verbose_name = "사용자 주소"
        verbose_name_plural = "사용자 주소 목록"
        app_label = "orders"
        db_table = "orders_order_addresses"

    def __str__(self):
        return f"{self.address} {self.detail_address}"


class OrderReceiver(TimeStampedModel):
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=11)

    class Meta:
        verbose_name = "주문 수령인"
        verbose_name_plural = "주문 수령인 목록"
        app_label = "orders"
        db_table = "orders_order_receivers"

    def __str__(self):
        return f"{self.name} - {self.phone_number}"


class Order(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    order_address = models.ForeignKey(
        "orders.OrderAddress",
        on_delete=models.PROTECT,
        related_name="orders",
        null=True,
    )
    receiver = models.OneToOneField(
        "orders.OrderReceiver",
        on_delete=models.PROTECT,
        related_name="order",
    )
    status = models.CharField(max_length=20)
    item_price = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=0)
    delivery_price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=20)
    payment_date = models.DateTimeField(null=True)
    is_first_purchase = models.BooleanField(default=False)

    class Meta:
        verbose_name = "주문"
        verbose_name_plural = "주문 목록"
        app_label = "orders"
        db_table = "orders_orders"

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.PROTECT,
        related_name="items",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    product_option = models.ForeignKey(
        "products.ProductOption",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = "주문 상품"
        verbose_name_plural = "주문 상품 목록"
        app_label = "orders"
        db_table = "orders_order_items"

    def __str__(self):
        return f"{self.order.user.email} - {self.product_option.product.name}"

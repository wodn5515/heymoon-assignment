from django.db import models
from apps.common.models import TimeStampedModel


class Coupon(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    discount_price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.PROTECT,
        related_name="coupons",
        null=True,
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="coupons",
        null=True,
    )

    class Meta:
        verbose_name = "쿠폰"
        verbose_name_plural = "쿠폰 목록"
        app_label = "coupons"
        db_table = "coupons_coupons"

    def __str__(self):
        return self.name


class UserCoupon(TimeStampedModel):
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.PROTECT,
        related_name="user_coupons",
    )
    coupon = models.ForeignKey(
        "coupons.Coupon",
        on_delete=models.PROTECT,
        related_name="user_coupons",
    )
    order = models.ForeignKey(
        "orders.Order", on_delete=models.PROTECT, related_name="user_coupons", null=True
    )
    is_used = models.BooleanField(default=False)
    used_date = models.DateTimeField(null=True)

    class Meta:
        verbose_name = "사용자 쿠폰"
        verbose_name_plural = "사용자 쿠폰 목록"
        app_label = "coupons"
        db_table = "coupons_user_coupons"

    def __str__(self):
        return f"{self.user_id} - {self.coupon.name}"

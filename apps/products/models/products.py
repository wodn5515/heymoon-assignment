from django.db import models
from apps.common.models import TimeStampedModel
import time


def product_thumbnail_image_path(instance, filename):
    timestamp = int(time.time())
    _, ext = filename.rsplit(".", 1)
    return f"products/thumbnails/{instance.id}/{timestamp}-{instance.order}.{ext}"


def product_original_image_path(instance, filename):
    timestamp = int(time.time())
    _, ext = filename.rsplit(".", 1)
    return f"products/originals/{instance.id}/{timestamp}-{instance.order}.{ext}"


def product_detail_image_path(instance, filename):
    timestamp = int(time.time())
    _, ext = filename.rsplit(".", 1)
    return f"products/details/{instance.id}/{timestamp}-{instance.order}.{ext}"


class ProductSeries(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

    class Meta:
        verbose_name = "상품 시리즈"
        verbose_name_plural = "상품 시리즈 목록"
        app_label = "products"
        db_table = "products_product_series"

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.PROTECT,
        related_name="products",
    )
    series = models.ForeignKey(
        "products.ProductSeries",
        on_delete=models.PROTECT,
        related_name="products",
        null=True,
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "상품"
        verbose_name_plural = "상품 목록"
        app_label = "products"
        db_table = "products_products"

    def __str__(self):
        return self.name


class ProductOption(TimeStampedModel):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="options",
    )
    name = models.CharField(max_length=100)
    additional_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

    class Meta:
        verbose_name = "상품 옵션"
        verbose_name_plural = "상품 옵션 목록"
        app_label = "products"
        db_table = "products_product_options"

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="images",
    )
    thumbnail = models.ImageField(
        upload_to=product_thumbnail_image_path,
        null=True,
    )
    original = models.ImageField(
        upload_to=product_original_image_path,
        null=True,
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "상품 이미지"
        verbose_name_plural = "상품 이미지 목록"
        app_label = "products"
        db_table = "products_product_images"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "order"],
                name="unique_product_order",
            ),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.id}"


class ProductDetail(TimeStampedModel):
    product = models.OneToOneField(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="detail",
    )
    description = models.TextField(null=True)

    class Meta:
        verbose_name = "상품 상세"
        verbose_name_plural = "상품 상세 목록"
        app_label = "products"
        db_table = "products_product_details"

    def __str__(self):
        return f"{self.product.name} - {self.id}"


class ProductDetailImage(TimeStampedModel):
    product_detail = models.ForeignKey(
        "products.ProductDetail",
        on_delete=models.CASCADE,
        related_name="images",
    )
    original = models.ImageField(
        upload_to=product_detail_image_path,
        null=True,
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "상품 상세 이미지"
        verbose_name_plural = "상품 상세 이미지 목록"
        app_label = "products"
        db_table = "products_product_detail_images"
        constraints = [
            models.UniqueConstraint(
                fields=["product_detail", "order"],
                name="unique_product_detail_order",
            ),
        ]

    def __str__(self):
        return f"{self.product_detail.product.name} - {self.id}"

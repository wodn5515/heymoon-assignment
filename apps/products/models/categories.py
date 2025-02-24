from django.db import models
from apps.common.models import TimeStampedModel


class Category(TimeStampedModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        related_name="children",
    )
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리 목록"
        app_label = "products"
        db_table = "products_categories"

    def __str__(self):
        return self.name

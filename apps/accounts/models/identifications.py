from apps.common.models import TimeStampedModel
from django.db import models


class PhoneIdentification(TimeStampedModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="phone_identification",
    )
    phone_number = models.CharField(max_length=11)

    class Meta:
        verbose_name = "전화번호 신분 증명"
        verbose_name_plural = "전화번호 신분 증명 목록"
        app_label = "accounts"
        db_table = "accounts_phone_identification"

    def __str__(self):
        return f"{self.user.email} - {self.phone_number}"


class EmailIdentification(TimeStampedModel):
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="email_identification",
    )
    email = models.EmailField(max_length=255)

    class Meta:
        verbose_name = "이메일 신분 증명"
        verbose_name_plural = "이메일 신분 증명 목록"
        app_label = "accounts"
        db_table = "accounts_email_identification"

    def __str__(self):
        return f"{self.user.email} - {self.email}"

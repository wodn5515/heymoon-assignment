from django.db import transaction
from django.utils import timezone
from faker import Faker
import random

from apps.accounts.models import User, PhoneIdentification

fake = Faker("ko_KR")


def create_users(num_users=10):
    """사용자 더미 데이터 생성"""
    print("=== 사용자 더미 데이터 생성 시작 ===")
    users = []
    identifications = []

    with transaction.atomic():
        for _ in range(num_users):
            email = fake.email()
            name = fake.name()
            phone_number = "010" + "".join(
                [str(random.randint(0, 9)) for _ in range(8)]
            )

            user = User.objects.create(
                email=email,
                name=name,
                is_active=True,
                is_identified=True,
            )
            # 비밀번호 설정 (실제 구현에 맞게 수정 필요)
            user.set_password("password123!")
            user.save()

            users.append(user)

            identification = PhoneIdentification(
                user=user,
                phone_number=phone_number,
            )
            identifications.append(identification)

        PhoneIdentification.objects.bulk_create(identifications)

    print("=== 사용자 더미 데이터 생성 완료 ===")

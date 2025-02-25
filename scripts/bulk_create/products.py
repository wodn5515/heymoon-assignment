import os
import django
import random
from faker import Faker

from apps.products.models import (
    ProductSeries,
    Product,
    ProductOption,
    ProductDetail,
    Category,
)
from django.core.files.uploadedfile import SimpleUploadedFile


fake = Faker("ko_KR")

NUM_PRODUCTS = 20  # 생성할 상품 수
NUM_SERIES = 5  # 생성할 시리즈 수


def create_products(num_products=NUM_PRODUCTS, num_series=NUM_SERIES):
    """상품 더미 데이터 생성"""
    print("=== 상품 더미 데이터 생성 시작 ===")
    # 시리즈 생성
    series_list = []
    for i in range(num_series):
        series = ProductSeries.objects.create(
            name=f"시리즈 {i+1}", description=fake.text()
        )
        series_list.append(series)
    print(f"{num_series}개의 시리즈 생성 완료")

    categories = Category.objects.filter(parent__isnull=False)

    # 상품 생성
    for i in range(num_products):
        try:
            # 상품 기본 정보 생성
            product = Product.objects.create(
                category=random.choice(categories),  # Category 모델 필요
                series=None,
                name=f"{fake.company()} {fake.word()} 상품",
                description=fake.text(),
                price=random.randint(10000, 100000),
                is_active=True,
            )

            # 상품 옵션 생성
            option_count = random.randint(1, 3)
            options = []
            for j in range(option_count):
                option = ProductOption(
                    product=product,
                    name=f"{fake.word()} 옵션",
                    additional_price=random.randint(1000, 5000),
                    quantity=random.randint(1, 100),
                )
                options.append(option)
            ProductOption.objects.bulk_create(options)

            # 상품 상세 정보 생성
            ProductDetail.objects.create(
                product=product, description=fake.text(max_nb_chars=1000)
            )

            print(f"상품 {i+1}/{num_products} 생성 완료")

        except Exception as e:
            print(f"상품 {i+1} 생성 중 오류 발생: {str(e)}")
    print("=== 상품 더미 데이터 생성 완료 ===")

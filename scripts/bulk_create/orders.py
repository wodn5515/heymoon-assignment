from faker import Faker
import random
import django
import os
import sys

from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from apps.accounts.models import User, PhoneIdentification
from apps.orders.models import OrderAddress, OrderReceiver, Order, OrderItem
from apps.products.models import Product, ProductOption
from apps.coupons.models import Coupon, UserCoupon
from django.db.models.functions import Coalesce

fake = Faker("ko_KR")


def create_orders(num_orders=50):
    """주문 더미 데이터 생성"""
    print("=== 주문 더미 데이터 생성 시작 ===")
    users = list(User.objects.all())
    if not users:
        print("사용자가 없습니다. 먼저 사용자를 생성해주세요.")
        return

    products = list(Product.objects.all())
    if not products:
        print("상품이 없습니다. 먼저 상품을 생성해주세요.")
        return

    with transaction.atomic():
        for i in range(num_orders):
            user = random.choice(users)
            # 주소 생성
            address = OrderAddress.objects.create(
                user=user,
                address=fake.address(),
                detail_address=fake.building_name(),
                postal_code=fake.postcode(),
                is_default=random.choice([True, False]),
                memo=fake.sentence(),
            )
            # 수령인 정보 생성
            receiver = OrderReceiver.objects.create(
                name=user.name,
                phone_number=user.phone_identification.phone_number,
            )
            # 주문 생성
            order = Order.objects.create(
                user=user,
                order_address=address,
                receiver=receiver,
                status=random.choice(["PENDING", "PAID", "SHIPPING", "COMPLETED"]),
                item_price=0,
                discount_price=0,
                delivery_price=0,
                total_price=0,
                payment_method=random.choice(["CARD", "BANK_TRANSFER", "MOBILE"]),
                payment_date=None,
                is_first_purchase=random.choice([True, False]),
            )
            if order.status != "PENDING":
                order.payment_date = fake.date_time_between(
                    start_date="-2d", end_date="now"
                )
            order.save()
            # 주문 상품 생성 (1~3개 랜덤)
            total_item_price = 0
            order_items = []
            order_items_product_ids = []
            for _ in range(random.randint(1, 3)):
                product = random.choice(products)
                product_option = random.choice(list(product.options.all()))
                quantity = random.randint(1, 5)
                order_item = OrderItem(
                    order=order,
                    product=product,
                    product_option=product_option,
                    quantity=quantity,
                )
                order_items.append(order_item)
                total_item_price += (
                    product_option.product.price + product_option.additional_price
                ) * quantity
                order_items_product_ids.append(product.id)
            OrderItem.objects.bulk_create(order_items)
            # 쿠폰 사용
            coupon = Coupon.objects.filter(
                is_active=True, product__in=order_items_product_ids
            )
            user_coupons = UserCoupon.objects.filter(
                user=user,
                coupon__in=coupon,
                is_used=False,
            )
            discount_price = user_coupons.aggregate(
                total_discount_price=Coalesce(Sum("coupon__discount_price"), 0)
            )["total_discount_price"]
            if user_coupons:
                for user_coupon in user_coupons:
                    user_coupon.is_used = True
                    user_coupon.used_date = timezone.now()
                    user_coupon.order = order
                    user_coupon.save()
            # price 필드 업데이트
            order.item_price = total_item_price
            order.discount_price = discount_price
            order.delivery_price = (
                3000 if random.random() < 0.5 else 0
            )  # 기본 배송비 3000원 or 무료배송
            order.total_price = (
                order.item_price - order.discount_price + order.delivery_price
            )
            order.save()

            print(f"주문 생성 완료: {i + 1}/{num_orders}")

    print("=== 주문 더미 데이터 생성 완료 ===")

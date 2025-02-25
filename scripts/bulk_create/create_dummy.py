from scripts.bulk_create.categories import create_categories
from scripts.bulk_create.products import create_products
from scripts.bulk_create.coupons import create_coupons
from scripts.bulk_create.orders import create_orders
from scripts.bulk_create.users import create_users
from django.db import transaction


COUPON_COUNT = 20  # 생성할 쿠폰 수
USER_COUPON_COUNT = 100  # 생성할 사용자 쿠폰 수
ORDER_COUNT = 100  # 생성할 주문 수
NUM_PRODUCTS = 20  # 생성할 상품 수
NUM_SERIES = 5  # 생성할 시리즈 수


def create_dummy():
    with transaction.atomic():
        create_users()
        create_categories()
        create_products(NUM_PRODUCTS, NUM_SERIES)
        create_coupons(COUPON_COUNT, USER_COUPON_COUNT)
        create_orders(ORDER_COUNT)

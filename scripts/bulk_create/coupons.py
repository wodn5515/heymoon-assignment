from datetime import datetime, timedelta
import random
from django.utils import timezone
from apps.coupons.models import Coupon, UserCoupon
from apps.accounts.models import User
from apps.products.models import Category, Product


def generate_dummy_coupons(count=10):
    """쿠폰 더미데이터 생성"""

    # 실제 데이터베이스에서 카테고리와 상품 목록 가져오기
    categories = list(Category.objects.all())
    products = list(Product.objects.all())

    coupons_data = []

    coupon_names = [
        "신규가입 특별 할인",
        "시즌 할인",
        "주말 특가",
        "첫 구매 할인",
        "회원 전용 할인",
        "특별 할인",
        "골드회원 전용",
        "프리미엄 할인",
        "한정특가",
        "기획전 할인",
    ]

    for i in range(count):
        # 시작일은 현재로부터 -5일 ~ +5일
        start_date = timezone.now() - timedelta(days=5)
        # 종료일은 시작일로부터 7일 ~ 30일
        end_date = start_date + timedelta(days=random.randint(7, 30))
        discount_price = random.choice([1000, 2000, 3000, 5000, 10000])
        is_category = random.random() < 0.5

        # 쿠폰 생성
        coupon = Coupon(
            name=f"{random.choice(coupon_names)} {i+1}",
            description=f"{discount_price}원 할인 쿠폰입니다.",
            discount_price=discount_price,
            is_active=True,  # 75% 확률로 활성화
            start_date=start_date,
            end_date=end_date,
            # 50% 확률로 카테고리 또는 상품 쿠폰으로 설정
            category=random.choice(categories) if is_category else None,
            product=random.choice(products) if not is_category else None,
        )
        coupons_data.append(coupon)

    # 벌크 생성으로 DB 저장
    created_coupons = Coupon.objects.bulk_create(coupons_data)
    return created_coupons


def generate_dummy_user_coupons(coupons, count=50):
    """사용자 쿠폰 더미데이터 생성"""

    users = list(User.objects.all())
    user_coupons_data = []

    for _ in range(count):
        user = random.choice(users)
        coupon = random.choice(coupons)
        is_used = False

        user_coupon = UserCoupon(
            user=user,
            coupon=coupon,
            is_used=is_used,
            used_date=timezone.now() if is_used else None,
        )
        user_coupons_data.append(user_coupon)

    # 벌크 생성으로 DB 저장
    created_user_coupons = UserCoupon.objects.bulk_create(user_coupons_data)
    return created_user_coupons


# 실행 예시
def create_coupons():
    print("=== 쿠폰 더미 데이터 생성 시작 ===")
    try:
        # 쿠폰 생성
        created_coupons = generate_dummy_coupons(10)
        print(f"생성된 쿠폰 수: {len(created_coupons)}")

        # 사용자 쿠폰 생성
        created_user_coupons = generate_dummy_user_coupons(created_coupons, 50)
        print(f"생성된 사용자 쿠폰 수: {len(created_user_coupons)}")
    except Exception as e:
        print(f"데이터 생성 중 오류 발생: {str(e)}")
    print("=== 쿠폰 더미 데이터 생성 완료 ===")

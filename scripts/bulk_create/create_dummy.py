from scripts.bulk_create.categories import create_categories
from scripts.bulk_create.products import create_products
from scripts.bulk_create.coupons import create_coupons
from scripts.bulk_create.orders import create_orders
from scripts.bulk_create.users import create_users
from django.db import transaction


def create_dummy():
    with transaction.atomic():
        create_users()
        create_categories()
        create_products()
        create_coupons()
        create_orders()

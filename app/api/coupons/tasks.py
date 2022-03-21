import random

from api.coupons.models import Coupon, UserCoupon
from api.users.models import User
from config.celery import app

from django.utils.timezone import now, timedelta


@app.task
def generate_coupons():
    coupon_types = Coupon.objects.all()
    if coupon_types:
        timezone_now = now().replace(microsecond=0)
        UserCoupon.objects.filter(
            created_at__lte=timezone_now - timedelta(minutes=1), valid=True, user__isnull=True
        ).update(valid=False)
        coupons_to_be_created = []
        users_without_coupons_total = User.objects.filter(
            is_superuser=False, coupons__isnull=True
        ).count()
        new_coupons_count = round(users_without_coupons_total / 2)

        for _ in range(new_coupons_count):
            coupon_type = random.choice(coupon_types)
            coupons_to_be_created.append(UserCoupon(created_at=timezone_now, coupon=coupon_type))

        UserCoupon.objects.bulk_create(coupons_to_be_created)


@app.task
def remove_expired_coupons():
    UserCoupon.objects.filter(valid=False, user__isnull=True).delete()

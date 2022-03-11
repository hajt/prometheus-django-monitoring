from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


COUPON_AMOUNTS = [500, 1000, 1500]


def validate_amount(amount):
    if amount not in COUPON_AMOUNTS:
        raise ValidationError(
            _(f"Amount should be one of {COUPON_AMOUNTS}"),
            params={"amount": amount},
        )

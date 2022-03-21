import uuid

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now

from .validators import validate_amount


class Coupon(models.Model):
    AMOUNTS = (
        (500, "500"),
        (1000, "1000"),
        (1500, "1500"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    amount = models.PositiveSmallIntegerField(
        help_text="Amount in cents", unique=True, validators=[validate_amount], choices=AMOUNTS
    )

    @property
    def amount_in_dolars(self) -> int:
        return self.amount // 100

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.amount_in_dolars}$"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.amount_in_dolars}$)>"


class UserCoupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    code = models.CharField(max_length=16, default=get_random_string)
    valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    coupon = models.ForeignKey(Coupon, on_delete=models.PROTECT, related_name="user_coupons")
    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="coupons", blank=True, null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["valid", "user", "coupon"],
                condition=models.Q(valid=True),
                name="unique_valid_user_coupon",
            )
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.code} | {self.user}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}({self.code})>"

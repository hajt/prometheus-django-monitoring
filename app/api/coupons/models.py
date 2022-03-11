import uuid

from django.db import models

from .validators import validate_amount


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4)
    amount = models.PositiveSmallIntegerField(
        null=False, help_text="Amount in cents", validators=[validate_amount]
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=["amount"], name="unique_amount")]

    @property
    def amount_in_dolars(self) -> int:
        return self.amount // 100

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.amount_in_dolars}$"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

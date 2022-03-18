from rest_framework import serializers

from .models import UserCoupon


class UserCouponSerializer(serializers.ModelSerializer):
    coupon = serializers.StringRelatedField()

    class Meta:
        model = UserCoupon
        fields = [
            "id",
            "code",
            "valid",
            "coupon",
        ]


class UserCouponDetailSerializer(UserCouponSerializer):
    amount = serializers.ReadOnlyField(source="coupon.amount")

    class Meta:
        model = UserCoupon
        fields = UserCouponSerializer.Meta.fields + [
            "amount",
        ]
        read_only_fields = ("id", "code")

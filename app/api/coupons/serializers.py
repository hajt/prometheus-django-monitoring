from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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

    def validate(self, validated_data):
        if validated_data["valid"] is True:
            raise ValidationError({"valid": "This field might be only 'false'"})

        return validated_data

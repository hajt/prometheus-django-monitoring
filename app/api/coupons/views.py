from django.utils.timezone import now, timedelta

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Coupon, UserCoupon
from .serializers import UserCouponDetailSerializer, UserCouponSerializer


class UserCouponViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch", "post"]

    def get_queryset(self):
        return UserCoupon.objects.filter(user__username=self.request.user.username).select_related(
            "user"
        )

    def get_serializer_class(self):
        return UserCouponSerializer if self.action == "list" else UserCouponDetailSerializer

    def create(self, request):
        user = self.request.user

        if user.coupons.filter(valid=True):
            raise ValidationError({"error": "Valid coupon already exists"})

        lock_in_minutes = 5
        last_user_coupon = (
            user.coupons.filter(
                valid=False, created_at__gte=now() - timedelta(minutes=lock_in_minutes)
            )
            .order_by("created_at")
            .last()
        )

        if last_user_coupon:
            time_left = (last_user_coupon.created_at + timedelta(minutes=lock_in_minutes)) - now()
            raise ValidationError(
                {
                    "error": f"Coupon create will be availible in {time_left.seconds//60} minutes \
                        {time_left.seconds%60} seconds"
                }
            )

        coupon = Coupon.objects.order_by("?").first()

        if not coupon:
            raise ValidationError({"error": "No coupons defined"})

        user_coupon = UserCoupon.objects.create(coupon=coupon, user=user)
        return Response(UserCouponDetailSerializer(user_coupon).data)

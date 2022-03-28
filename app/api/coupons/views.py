from django.urls import reverse
from django.utils.timezone import now, timedelta

from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .metrics import (
    coupon_create_last_status,
    coupon_create_time,
    last_user_activity_time,
    requests_total,
)
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

    def initial(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        requests_total.labels(
            endpoint=self._get_endpoint(pk), method=self.request.method, user=user
        ).inc()
        last_user_activity_time.labels(user=user).set(now().timestamp())
        return super().initial(request, *args, **kwargs)

    def create(self, request):
        user = self.request.user

        self._validate_valid_coupon_exists(user)
        self._validate_coupon_created_within_5_minutes(user)

        coupon = Coupon.objects.order_by("?").first()

        self._validate_coupon_type_exists(coupon, user)

        start_time = now().timestamp()
        user_coupon = UserCoupon.objects.create(coupon=coupon, user=user)
        coupon_create_time.observe(now().timestamp() - start_time)
        coupon_create_last_status.labels(user=user).state("success")

        return Response(UserCouponDetailSerializer(user_coupon).data)

    def _validate_valid_coupon_exists(self, user):
        if user.coupons.filter(valid=True):
            coupon_create_last_status.labels(user=user).state("error")
            raise ValidationError({"error": "Valid coupon already exists"})

    def _validate_coupon_created_within_5_minutes(self, user):
        lock_in_minutes = 5
        last_user_coupon = (
            user.coupons.filter(
                valid=False, created_at__gte=now() - timedelta(minutes=lock_in_minutes)
            )
            .order_by("created_at")
            .last()
        )

        if last_user_coupon:
            coupon_create_last_status.labels(user=user).state("error")
            time_left = (last_user_coupon.created_at + timedelta(minutes=lock_in_minutes)) - now()
            raise ValidationError(
                {
                    "error": f"Coupon create will be availible in {time_left.seconds//60} minutes {time_left.seconds%60} seconds"  # noqa: E501
                }
            )

    def _validate_coupon_type_exists(self, coupon, user):
        if not coupon:
            coupon_create_last_status.labels(user=user).state("error")
            raise ValidationError({"error": "No coupons defined"})

    def _get_endpoint(self, pk=None):
        return f"{reverse('coupons-list')}{pk}/" if pk else reverse("coupons-list")

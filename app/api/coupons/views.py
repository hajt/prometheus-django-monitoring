from rest_framework import viewsets

from .models import UserCoupon
from .serializers import UserCouponDetailSerializer, UserCouponSerializer


class UserCouponViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "patch"]

    def get_queryset(self):
        return UserCoupon.objects.filter(user__username=self.request.user.username).select_related(
            "user"
        )

    def get_serializer_class(self):
        return UserCouponSerializer if self.action == "list" else UserCouponDetailSerializer

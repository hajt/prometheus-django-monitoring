from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import UserCoupon
from .serializers import UserCouponDetailSerializer, UserCouponSerializer


class UserCouponViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCouponSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        return UserCoupon.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return UserCouponDetailSerializer if self.action == "retrieve" else self.serializer_class

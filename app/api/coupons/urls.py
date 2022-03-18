from rest_framework import routers

from .views import UserCouponViewSet


router = routers.SimpleRouter()
router.register("coupons", UserCouponViewSet, basename="coupons")

urlpatterns = router.urls

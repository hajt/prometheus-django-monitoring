from django.contrib import admin

from .models import Coupon, UserCoupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("__str__", "amount")


@admin.register(UserCoupon)
class UserCouponAdmin(admin.ModelAdmin):
    list_display = ("code", "coupon", "valid", "user")

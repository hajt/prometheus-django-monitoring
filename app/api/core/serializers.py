from django.contrib.auth import get_user_model

from rest_framework import serializers


# from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", "email"]

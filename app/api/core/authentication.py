from rest_framework import authentication


class Authentication(authentication.TokenAuthentication):
    keyword = "Bearer"

from rest_framework import serializers
from django.contrib.auth.models import User
from re import fullmatch

from utils.Responses import ErrorResponses


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, min_length=5)
    password = serializers.CharField(min_length=8,max_length=128)
    confirm_password = serializers.CharField(min_length=8,max_length=128)

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise serializers.ValidationError(detail=ErrorResponses.USERNAME_IS_TAKEN)
        except User.DoesNotExist:
            return username

    def validate_password(self, password):
        if not fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
            raise serializers.ValidationError("Password must contain at least one number and one letter.")
        return password

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(detail="password and confirm_password are not match.")
        return super(UserRegisterSerializer, self).validate(attrs)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


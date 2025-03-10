from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from auth_module.serializers import UserLoginSerializer, UserRegisterSerializer
from utils.Responses import ErrorResponses


class UserLogView(APIView):
    def post(self, request):
        """ user register """
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        user = User(username=username)
        user.set_password(password)
        user.save()
        return Response({"data":"User created."}, status=status.HTTP_200_OK)


    def put(self, request):
        """ user login """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data=ErrorResponses.WRONG_LOGIN_DATA, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(password):
            return Response(data=ErrorResponses.WRONG_LOGIN_DATA, status=status.HTTP_400_BAD_REQUEST)
        data = {
            "access_token": str(AccessToken.for_user(user)),
            "refresh_token": str(RefreshToken.for_user(user)),
            "user_id": user.id,
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request):
        """ user logout """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = request.data["refresh_token"]
            tk = RefreshToken(refresh_token)
            tk.blacklist()
            return Response({"data":"Successfully logged out."}, status=status.HTTP_204_NO_CONTENT)

        except Exception:
            return Response(data=ErrorResponses.TOKEN_IS_EXPIRED_OR_INVALID, status=status.HTTP_400_BAD_REQUEST)






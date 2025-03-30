from django.contrib.auth import user_logged_in
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from auth_module.models import User, New


class UserLogView(GenericAPIView):

    def post(self, request):
        user = User(username="sfsssff",email="ali.s@gmail.com")
        user.set_password('<PASSWORD>1qwe')
        user.save()
        return Response({"data": ""}, status=status.HTTP_201_CREATED)

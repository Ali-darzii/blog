from django.contrib.auth import user_logged_in
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from auth_module.models import User


class UserLogView(GenericAPIView):

    def post(self, request):
        # user = User(username="aqa_meti")
        # user.set_password("sdfawioksfdnropwe1")
        # user.insert_one()
        alls = User.get_all(["-username"])

        return Response({"data": alls}, status=status.HTTP_201_CREATED)

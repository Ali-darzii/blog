from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from blog_module.models import Blog
from blog_module.serializers import BlogSerializer
from utils.permission import IsOwner


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_permissions(self):
        if not self.action == 'list' or not self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsOwner]
        self.permission_classes = [AllowAny]
        return super(BlogViewSet, self).get_permissions()
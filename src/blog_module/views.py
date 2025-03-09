from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status 
from blog_module.models import Blog
from blog_module.serializers import BlogSerializer
from utils.permission import IsOwner
from rest_framework.exceptions import PermissionDenied

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        blog = self.get_object()
        if blog.author != self.request.user:
            raise PermissionDenied("You are not allowed to update this blog")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You are not allowed to destroy this blog")
        instance.delete()
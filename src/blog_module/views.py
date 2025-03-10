from codecs import replace_errors
from idlelib.macosx import isAquaTk

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from blog_module.models import Blog
from blog_module.serializers import BlogSerializer
from utils.permission import IsOwner


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(),IsOwner()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
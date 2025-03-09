from rest_framework import serializers

from blog_module.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ("id","text","title","author","created_at","updated_at")
        read_only_fields = ("id","created_at","updated_at","author")
from django.urls import path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'blog', views.BlogViewSet, basename='Blogs')

from . import views
urlpatterns = []
urlpatterns += router.urls
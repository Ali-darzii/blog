from django.urls import path
from . import views
urlpatterns = [
    path("user/auth/", views.UserLogView.as_view(), name="auth_user"),
]

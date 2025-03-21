from django.urls import path
from auth_module import views

urlpatterns = [
    path("user/auth/", views.UserLogView.as_view(), name="auth_user"),

]
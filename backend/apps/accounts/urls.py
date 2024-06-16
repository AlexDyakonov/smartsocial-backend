from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import UserDetailView, UserListView, UserRegistrationView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", UserListView.as_view(), name="user-list"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("<int:id>/", UserDetailView.as_view(), name="user-detail"),
]

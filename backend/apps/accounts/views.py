from django.shortcuts import render
from rest_framework import generics

from .models import User
from .serializers import (
    UserDetailSerializer,
    UserListSerializer,
    UserRegistrationSerializer,
)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "id"

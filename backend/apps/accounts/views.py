from django.shortcuts import render
from rest_framework import generics

from .models import User
from .serializers import UserListSerializer, UserRegistrationSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

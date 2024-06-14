from django.urls import path

from .views import AddFileToOrder

urlpatterns = [
    path("create", AddFileToOrder.as_view()),
]

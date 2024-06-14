from django.urls import path

from .views import AddFileToBooking

urlpatterns = [
    path("create", AddFileToBooking.as_view()),
]

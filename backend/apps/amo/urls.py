from django.urls import path

from .views import (
    AmoBookingsAPIView
)

urlpatterns = [
    path("bookings/", AmoBookingsAPIView.as_view(), name="amo-booking"),
]

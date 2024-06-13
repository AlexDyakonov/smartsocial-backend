from django.urls import path

from .views import (
    BuyerListCreateAPIView,
    BuyerRetrieveUpdateAPIView,
    CartListCreateAPIView,
    CartRetrieveUpdateAPIView,
    EventsAvailableApiView,
    PlacesAvailableApiView,
)
from .amo import BookingsAmoAPIView

urlpatterns = [
    path("buyers/", BuyerListCreateAPIView.as_view(), name="buyer-list-create"),
    path("buyers/<int:pk>/", BuyerRetrieveUpdateAPIView.as_view(), name="buyer-detail"),
    path("carts/", CartListCreateAPIView.as_view(), name="cart-create"),
    path("carts/<int:pk>/", CartRetrieveUpdateAPIView.as_view(), name="cart-detail"),
    path(
        "places/available/", PlacesAvailableApiView.as_view(), name="places-available"
    ),
    path(
        "places/<int:pk>/events/available/",
        EventsAvailableApiView.as_view(),
        name="events-available",
    ),
    path("bookings/amo/", BookingsAmoAPIView.as_view(), name="bookings-amo")
]

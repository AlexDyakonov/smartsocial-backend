from django.urls import path
from .views import (
    CartListCreateAPIView,
    CartRetrieveUpdateAPIView,
    BuyerListCreateAPIView,
    BuyerRetrieveUpdateAPIView,
    OrderAPIView,
    PlacesAvailableApiView,
    EventsAvailableApiView,
)

urlpatterns = [
    path('buyers/', BuyerListCreateAPIView.as_view(), name='buyer-list-create'),
    path('buyers/<int:pk>/', BuyerRetrieveUpdateAPIView.as_view(), name='buyer-detail'),
    path('carts/', CartListCreateAPIView.as_view(), name='cart-create'),
    path('carts/<int:pk>/', CartRetrieveUpdateAPIView.as_view(), name='cart-detail'),
    path('carts/<int:pk>/order/', OrderAPIView.as_view(), name='cart-order'),
    path('places/available/', PlacesAvailableApiView.as_view(), name='places-available'),
    path('places/<int:pk>/events/available/', EventsAvailableApiView.as_view(), name='events-available'),
]

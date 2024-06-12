from django.urls import path
from .views import (
    PlaceListCreateAPIView,
    PlaceRetrieveUpdateDestroyAPIView,
    EventListCreateAPIView,
    EventRetrieveUpdateDestroyAPIView,
    TicketListCreateAPIView,
    TicketRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('places/', PlaceListCreateAPIView.as_view(), name='place-list-create'),
    path('places/<int:pk>/', PlaceRetrieveUpdateDestroyAPIView.as_view(), name='place-detail'),
    path('events/', EventListCreateAPIView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventRetrieveUpdateDestroyAPIView.as_view(), name='event-detail'),
    path('tickets/', TicketListCreateAPIView.as_view(), name='ticket-list-create'),
    path('tickets/<int:pk>/', TicketRetrieveUpdateDestroyAPIView.as_view(), name='ticket-detail'),
]

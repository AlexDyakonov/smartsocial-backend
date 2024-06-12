from datetime import datetime, timedelta

from apps.core.models import Event, Place
from apps.core.serializers import EventSerializer, PlaceOutputSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .dto import EventWithDate, EventWithDateSerializer
from .models import Buyer, Cart
from .serializers import BuyerSerializer, CartInputSerializer, CartOutputSerializer


class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CartInputSerializer
        return CartOutputSerializer


class CartRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer

    def get_serializer_class(self):
        if self.request.method == "PUT" or self.request.method == "PATCH":
            return CartInputSerializer
        return CartOutputSerializer


class BuyerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class BuyerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class PlacesAvailableApiView(APIView):
    serializer_class = PlaceOutputSerializer

    def get(self, request):
        queryset = Place.objects.all()
        if queryset:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class EventsAvailableApiView(APIView):
    serializer_class = EventWithDateSerializer

    def get(self, request, pk):
        queryset = Event.objects.filter(place_id=pk).all()
        events = [
            EventWithDate(
                id=e.id,
                place_id=e.place.id,
                name=e.name,
                description=e.description,
                capacity=e.max_capacity,
                tickets=e.tickets.all(),
                start_datetime=datetime.now(),
                end_datetime=datetime.now() + timedelta(hours=1),
            )
            for e in queryset
        ]
        serializer = self.serializer_class(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

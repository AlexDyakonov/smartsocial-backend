from datetime import datetime

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .dto import EventWithDateSerializer, EventWithDate
from .models import Cart, Buyer
from apps.core.models import Place, Event
from apps.booking.models import Booking
from apps.core.serializers import PlaceOutputSerializer

import recurring_ical_events as rec_ical

from .serializers import (
    CartInputSerializer,
    CartOutputSerializer,
    BuyerSerializer,
)


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
        events_queryset = Event.objects.filter(place_id=pk).all()
        try:
            start_datetime = datetime.fromisoformat(request.query_params.get('start_datetime'))
            end_datetime = datetime.fromisoformat(request.query_params.get('end_datetime'))
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use ISO 8601 format: YYYY-MM-DDTHH:MM:SS"},
                status=status.HTTP_400_BAD_REQUEST
            )

        events_with_date: list[EventWithDate] = []
        for event in events_queryset:
            cal = event.icalendar()
            events = rec_ical.of(cal).between(start_datetime, end_datetime)

            for e in events:
                event_with_date: EventWithDate = EventWithDate(
                    id=event.id,
                    place_id=event.place.id,
                    name=event.name,
                    description=event.description,
                    capacity=event.max_capacity,
                    start_datetime=e["DTSTART"].dt,
                    end_datetime=e["DTEND"].dt
                )
                events_with_date.append(event_with_date)
            for e in events_with_date:
                e.capacity -= Booking.objects.filter(
                    event_id=e.id, time=e.start_datetime
                ).count()
        serializer = self.serializer_class(events_with_date, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

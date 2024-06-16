import dataclasses
from datetime import datetime

import dateutil.parser
import recurring_ical_events as rec_ical
from apps.booking.models import Booking
from apps.core.models import Event, Place
from apps.core.serializers import PlaceOutputSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .dto import EventWithDate, EventWithDateSerializer, TicketWithDate
from .models import Buyer, Cart
from .serializers import BookingSerializer, BuyerSerializer, CartSerializer
from apps.amo.views import post_orders


class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


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
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "start_datetime",
                openapi.IN_QUERY,
                description="start datetime",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "end_datetime",
                openapi.IN_QUERY,
                description="end datetime",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, pk):
        try:
            start_datetime = dateutil.parser.isoparse(
                request.query_params.get("start_datetime")
            )
            end_datetime = dateutil.parser.isoparse(
                request.query_params.get("end_datetime")
            )
        except ValueError:
            return Response(
                {
                    "error": "Invalid date format. Use ISO 8601 format: YYYY-MM-DDTHH:MM:SS"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        events_queryset = Event.objects.filter(place_id=pk).all()
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
                    end_datetime=e["DTEND"].dt,
                )
                events_with_date.append(event_with_date)
            for e in events_with_date:
                e.capacity -= Booking.objects.filter(
                    event_id=e.id, time=e.start_datetime
                ).count()
        serializer = EventWithDateSerializer(events_with_date, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketsAvailableApiView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "start_datetime",
                openapi.IN_QUERY,
                description="start datetime",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "end_datetime",
                openapi.IN_QUERY,
                description="end datetime",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def get(self, request, pk):
        try:
            start_datetime = dateutil.parser.isoparse(
                request.query_params.get("start_datetime")
            )
            end_datetime = dateutil.parser.isoparse(
                request.query_params.get("end_datetime")
            )
        except ValueError:
            return Response(
                {
                    "error": "Invalid date format. Use ISO 8601 format: YYYY-MM-DDTHH:MM:SS"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        event: Event = Event.objects.filter(pk=pk).first()
        cal = event.icalendar()
        events = rec_ical.of(cal).between(start_datetime, end_datetime)

        dates = []
        for e in events:
            dates.append(e["DTSTART"].dt)
        tickets_with_date: list[TicketWithDate] = []
        for ticket in event.tickets.all():
            for date in dates:
                tickets_with_date.append(
                    TicketWithDate(
                        ticket_id=ticket.id,
                        event_id=event.id,
                        event_name=event.name,
                        name=ticket.name,
                        type=ticket.type,
                        price=ticket.price,
                        personas=ticket.personas,
                        time=date,
                    )
                )

        return Response(
            list(map(dataclasses.asdict, tickets_with_date)), status=status.HTTP_200_OK
        )


class BookingVisitAPIView(APIView):
    def get(self, request, pk):
        b: Booking = Booking.objects.filter(pk=pk).first()
        b.visited = not b.visited
        b.save()
        post_orders([b.order])
        return Response(BookingSerializer(b).data, status.HTTP_200_OK)

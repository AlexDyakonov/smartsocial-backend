from rest_framework import generics, status
from rest_framework.views import APIView, Response

from .models import Event, Place, Ticket
from .serializers import (
    EventSerializer,
    PlaceInputSerializer,
    PlaceOutputSerializer,
    TicketSerializer,
)


class PlaceListCreateAPIView(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceOutputSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PlaceInputSerializer
        return PlaceOutputSerializer


class PlaceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceOutputSerializer

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PlaceInputSerializer
        return PlaceOutputSerializer


class EventListCreateAPIView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventTicketsAPIView(APIView):
    serializer_class = TicketSerializer

    def get(self, request, pk):
        tickets = Event.objects.filter(pk=pk).first().tickets.all()
        return Response(
            self.serializer_class(tickets, many=True).data, status.HTTP_200_OK
        )


class TicketListCreateAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

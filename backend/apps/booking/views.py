from datetime import datetime, timedelta

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .dto import EventWithDateSerializer, EventWithDate
from .models import Cart, Buyer, Order
from .serializers import OrderSerializer
from apps.core.models import Place, Event
from apps.core.serializers import PlaceOutputSerializer, EventSerializer

from .serializers import (
    CartInputSerializer,
    CartOutputSerializer,
    BuyerSerializer,
)


class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartInputSerializer
        return CartOutputSerializer


class CartRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return CartInputSerializer
        return CartOutputSerializer


class BuyerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class BuyerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class OrderAPIView(APIView):
    serializer_class = OrderSerializer

    def post(self, request, pk):
        try:
            cart = Cart.objects.filter(pk=pk).first()
        except Cart.DoesNotExist:
            return Response({"error": "Cart does not exist"}, status=status.HTTP_404_NOT_FOUND)

        existing_order = Order.objects.filter(cart=cart).first()
        if existing_order:
            return Response({"error": "Order already exists for this cart"}, status=status.HTTP_400_BAD_REQUEST)

        # TODO kassa
        order_data = {'cart': cart.id, 'payment': "TODO", 'status': 'pending', 'total': 0}
        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        queryset = Order.objects.filter(cart_id=pk).first()
        if queryset:
            serializer = self.serializer_class(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "No order found for this cart"}, status=status.HTTP_404_NOT_FOUND)


class PlacesAvailableApiView(APIView):
    serializer_class = PlaceOutputSerializer

    def get(self, request):
        queryset = Place.objects.all()
        if queryset:
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventsAvailableApiView(APIView):
    serializer_class = EventWithDateSerializer

    def get(self, request, pk):
        queryset = Event.objects.filter(place_id=pk).all()
        events = [EventWithDate(
            id=e.id,
            place_id=e.place.id,
            name=e.name,
            description=e.description,
            capacity=e.max_capacity,
            tickets=e.tickets.all(),

            start_datetime=datetime.now(),
            end_datetime=datetime.now() + timedelta(hours=1),
        ) for e in queryset]
        serializer = self.serializer_class(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

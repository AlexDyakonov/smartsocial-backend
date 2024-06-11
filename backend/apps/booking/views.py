from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, Buyer, Order
from .serializers import OrderSerializer

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

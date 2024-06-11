from rest_framework import generics
from .models import Cart, Buyer
from .serializers import (
    CartInputSerializer,
    CartOutputSerializer,
    BuyerSerializer,
)


class CartListCreateAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartInputSerializer


class CartRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartOutputSerializer


class BuyerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class BuyerRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

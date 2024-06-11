from django.urls import path
from .views import (
    CartListCreateAPIView,
    CartRetrieveUpdateAPIView,
    BuyerListCreateAPIView,
    BuyerRetrieveUpdateAPIView
)

urlpatterns = [
    path('buyers/', BuyerListCreateAPIView.as_view(), name='buyer-list-create'),
    path('buyers/<int:pk>/', BuyerRetrieveUpdateAPIView.as_view(), name='buyer-detail'),
    path('carts/', CartListCreateAPIView.as_view(), name='cart-create'),
    path('carts/<int:pk>/', CartRetrieveUpdateAPIView.as_view(), name='cart-detail'),
]

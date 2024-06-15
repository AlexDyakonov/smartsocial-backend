from django.urls import path

from .views import (
    BookingsByOrderIdAPIView,
    PaymentListView,
    PaymentProcessingView,
    PaymentStatusView,
    yookassa_webhook,
)

urlpatterns = [
    path("yookassa-webhook/", yookassa_webhook, name="yookassa-webhook"),
    path("create/", PaymentProcessingView.as_view()),
    path("check/<str:payment_id>/", PaymentStatusView.as_view(), name="payment-status"),
    path(
        "order/<str:payment_id>/bookings/",
        BookingsByOrderIdAPIView.as_view(),
        name="bookings-by-order",
    ),
    path("", PaymentListView.as_view(), name="payment-list"),
]

from django.urls import path

from .views import (
    PaymentProcessingView,
    PaymentStatusView,
    send_purchase_email_view,
    yookassa_webhook,
    BookingsByOrderIdAPIView
)

urlpatterns = [
    path("yookassa-webhook/", yookassa_webhook, name="yookassa-webhook"),
    path("create/", PaymentProcessingView.as_view()),
    path("check/<str:payment_id>/", PaymentStatusView.as_view(), name="payment-status"),
    path("order/<str:id>/bookings/", BookingsByOrderIdAPIView.as_view(), name="bookings-by-order"),
    path("test-mail/", send_purchase_email_view),
]

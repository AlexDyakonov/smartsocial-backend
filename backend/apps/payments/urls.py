from django.urls import path

from .views import (
    BookingsByOrderIdAPIView,
    PaymentCancelView,
    PaymentItemInputView,
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
    path("list/", PaymentListView.as_view(), name="payment-list"),
    path("add-item/", PaymentItemInputView.as_view(), name="payment-add-item"),
    path(
        "cancel/<str:payment_id>/", PaymentCancelView.as_view(), name="payment-cancel"
    ),
]

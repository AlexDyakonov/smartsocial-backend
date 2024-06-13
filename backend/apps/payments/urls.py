from django.urls import path

from .views import PaymentProcessingView, yookassa_webhook

urlpatterns = [
    path('yookassa-webhook/', yookassa_webhook, name='yookassa-webhook'),
    path("create", PaymentProcessingView.as_view()),
]

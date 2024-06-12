from django.urls import path

from .views import PaymentProcessingView

urlpatterns = [
    path("process-payment", PaymentProcessingView.as_view()),
]

from django.urls import path

from .views import PaymentProcessingView

urlpatterns = [
    path("create", PaymentProcessingView.as_view()),
]

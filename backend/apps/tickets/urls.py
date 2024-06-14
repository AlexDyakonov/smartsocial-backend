from django.urls import path

from .views import CreateTicket

urlpatterns = [
    path("generate", CreateTicket.as_view()),
]

from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path("", include("apps.core.urls")),
    path("", include("apps.booking.urls")),
    path("tickets/", include("apps.tickets.urls")),
    path("payments/", include("apps.payments.urls")),
]

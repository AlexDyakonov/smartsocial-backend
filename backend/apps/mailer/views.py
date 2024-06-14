from django.conf import settings
from django.shortcuts import redirect, render

from django.urls import reverse
from rest_framework import generics
from apps.booking.models import Buyer

from .models import Mailing
from .serializers import (
    MailingSerializerReadOnly,
    MailingSerializerWriteOnly,
)
from .tasks import send_mailing


class MailingCreateView(generics.CreateAPIView):
    serializer_class = MailingSerializerWriteOnly
    queryset = Mailing.objects.all()

    def perform_create(self, serializer: MailingSerializerWriteOnly):
        mailing = serializer.save()
        emails: list = serializer.validated_data.get("emails")
        send_mailing.delay(emails, mailing.id)


class MailingListView(generics.ListAPIView):
    serializer_class = MailingSerializerReadOnly
    queryset = Mailing.objects.all()


class MailingRetrieveView(generics.RetrieveAPIView):
    serializer_class = MailingSerializerReadOnly
    queryset = Mailing.objects.all()


def mailing_admin(request):
    if request.user.is_authenticated:
        user = request.user

        content = {
            "user": user,
            "site_settings": settings.JAZZMIN_SETTINGS,
            "admin_url": reverse("admin:index"),
            "buyers": Buyer.objects.all(),
        }

        return render(request, "mailer-admin/send-mail-page.html", content)
    else:
        return redirect("admin:index")

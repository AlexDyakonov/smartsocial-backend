from django.http import HttpResponse
from rest_framework.views import APIView

from django.db.models import Sum
from .dto import DealDTO, deal_to_json
from apps.booking.models import Booking, Ticket
from backend.settings import AMOCRM_ACCESS_TOKEN
import requests


class AmoBookingsAPIView(APIView):
    def get(self, request):
        bookings = Booking.objects.select_related('event', 'ticket').values(
            'event__name',
            'ticket__place__name',
            'ticket__type',
            'ticket__price',
            'time',
        ).annotate(
            total_price=Sum('ticket__price')
        ).order_by('time')

        def booking_to_deal(booking):
            return DealDTO(
                booking['event__name'],
                int(booking['total_price']),
                booking['ticket__place__name'],
                booking['event__name'],
                Ticket(type=booking['ticket__type']).get_type_display(),
                int(booking['ticket__price']),
                int(booking['total_price'] // booking['ticket__price']),
                booking['time']
            )

        deals = list(map(booking_to_deal, bookings))
        x = post_deals(deals)
        print(x.text)
        return HttpResponse("")


def post_deals(deals: list[DealDTO]):
    url = 'https://forvantar.amocrm.ru/api/v4/leads'
    json_data = list(map(deal_to_json, deals))
    headers = {
        'Authorization': f'Bearer {AMOCRM_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    return requests.post(url, json=json_data, headers=headers)

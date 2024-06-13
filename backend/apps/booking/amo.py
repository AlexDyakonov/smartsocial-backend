import csv
import io
from django.http import HttpResponse
from rest_framework.views import APIView

from .models import Booking


class BookingsAmoAPIView(APIView):

    def get(self, request):
        bookings = Booking.objects.select_related('event', 'ticket', 'cart__buyer').all()

        buffer = io.StringIO()
        writer = csv.writer(buffer)

        writer.writerow([
            "Название сделки",
            "Бюджет сделки",
            "Ответственный за сделку",
            "Дата создания (сделка)",
            "Кем создана сделка",
            "Тег сделки",
            "Полное имя (контакт)",
            "Мобильный телефон (контакт)",
            "Личный email (контакт)",
            "Этап сделки"
        ])

        for booking in bookings:
            deal_name = booking.event.name
            budget = booking.ticket.price
            responsible = "Иван Иванов"
            creation_date = booking.time.strftime("%d.%m.%Y %H:%M")
            created_by = "Иван Иванов"
            deal_tag = "покупка билета"
            buyer = booking.cart.buyer
            full_name = f"{buyer.first_name} {buyer.last_name}"
            phone = buyer.phone
            email = buyer.email
            deal_stage = "Оплачен"

            writer.writerow([
                deal_name,
                budget,
                responsible,
                creation_date,
                created_by,
                deal_tag,
                full_name,
                phone,
                email,
                deal_stage
            ])

        response = HttpResponse(buffer.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=bookings.csv'

        return response

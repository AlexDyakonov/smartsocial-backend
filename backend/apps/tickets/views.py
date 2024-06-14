from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .generator import create_ticket_template


class AddFileToBooking(APIView):
    def get(self, request):
        ticket_info = {
            "buyer_name": "Иван Иванов",
            "total_cost": 500,
            "seat_count": 4,
            "qr_data": "https://example.com/validate_ticket?id=123456",
            "tickets": [
                {
                    "ticket_number": 3,
                    "place_name": "Название места 3",
                    "event_name": "Мероприятие 1",
                    "date": "Дата 1",
                    "time": "Время 1",
                    "cost": "Бесплатно",
                    "ticket_type": "Детский",
                },
            ],
        }

        create_ticket_template(ticket_info, "ticket_template.pdf")
        return Response(status=status.HTTP_200_OK)

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .generator import generate_ticket
from .serializers import OrderPaymentIdSerializer
from .utils import get_ticket_info


class CreateTicket(generics.CreateAPIView):
    serializer_class = OrderPaymentIdSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            order_id = serializer.validated_data.get("order_id")

            ticket_info = get_ticket_info(order_id)
            if not ticket_info:
                return Response(
                    {"error": "Error fetching ticket info"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if generate_ticket(ticket_info, order_id):
                return Response(
                    {"ticket_url": "kolomnago.ru"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Error creating ticket"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

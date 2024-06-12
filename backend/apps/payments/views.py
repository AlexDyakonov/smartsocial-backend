from rest_framework import generics, status
from rest_framework.response import Response

from .services import YooKassaService


class PaymentProcessingView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        cart_id = request.data.get("cart_id")
        payment_response = YooKassaService.create_payment_embedded("10", cart_id)
        payment_id = payment_response.get("id")
        payment_status = payment_response.get("status")
        confirmation_token = payment_response.get("confirmation", {}).get(
            "confirmation_token"
        )

        return Response(
            {
                "message": "Success",
                "confirmation_token": f"{confirmation_token}",
                "payment_id": f"{payment_id}",
                "payment_status": f"{payment_status}",
                "return_url": "https://kolomnago.ru",
                "cart_id": cart_id,
            },
            status=status.HTTP_200_OK,
        )

from apps.booking.models import Buyer, Cart
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Order
from .serializers import PaymentProcessingSerializer
from .services import YooKassaService


class PaymentProcessingView(generics.GenericAPIView):
    serializer_class = PaymentProcessingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_id = serializer.validated_data.get("cart_id")
        buyer_data = serializer.validated_data.get("buyer")

        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            buyer, created = Buyer.objects.update_or_create(
                email=buyer_data["email"],
                defaults={
                    "phone": buyer_data["phone"],
                    "first_name": buyer_data["first_name"],
                    "last_name": buyer_data["last_name"],
                },
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        cart.buyer = buyer
        cart.save()

        cart_total = cart.total

        payment_response = YooKassaService.create_payment_embedded(cart_total, cart_id)
        payment_id = payment_response.get("id")
        payment_status = payment_response.get("status")
        confirmation_token = payment_response.get("confirmation", {}).get(
            "confirmation_token"
        )

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    cart=cart,
                    total=cart_total,
                    payment_id=payment_id,
                    return_url="https://kolomnago.ru",
                    confirmation_token=confirmation_token,
                    payment_status=payment_status,
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "message": "Success",
                "confirmation_token": confirmation_token,
                "payment_id": payment_id,
                "payment_status": payment_status,
                "return_url": "https://kolomnago.ru",
                "cart_id": cart_id,
                "order_id": order.id,
            },
            status=status.HTTP_200_OK,
        )

import json

from apps.booking.models import Buyer, Cart
from apps.payments.models import Order
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Order
from .serializers import PaymentProcessingSerializer
from .services import YooKassaService


class PaymentProcessingView(generics.GenericAPIView):
    serializer_class = PaymentProcessingSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_id = serializer.validated_data.get("cart_id")
        buyer_data = serializer.validated_data.get("buyer")

        cart = Cart.objects.filter(id=cart_id).first()
        if not cart:
            return Response(
                {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            buyer, created = Buyer.objects.update_or_create(
                email=buyer_data["email"],
                defaults={
                    "phone": buyer_data.get("phone"),
                    "first_name": buyer_data.get("first_name"),
                    "last_name": buyer_data.get("last_name"),
                },
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        cart.buyer = buyer
        cart.save(update_fields=["buyer"])

        existing_order = Order.objects.filter(
            cart_id=cart_id, payment_status="pending"
        ).first()
        if existing_order:
            return Response(
                {
                    "message": "Existing unpaid order found",
                    "order_id": existing_order.id,
                    "payment_status": existing_order.payment_status,
                    "confirmation_token": existing_order.confirmation_token,
                    "payment_id": existing_order.payment_id,
                },
                status=status.HTTP_200_OK,
            )

        payment_response = YooKassaService.create_payment_embedded("10", cart_id)
        if not payment_response:
            return Response(
                {"error": "Payment service error"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        payment_id = payment_response.get("id")
        payment_status = payment_response.get("status")
        confirmation_token = payment_response.get("confirmation", {}).get(
            "confirmation_token"
        )

        if payment_id and payment_status:
            try:
                with transaction.atomic():
                    order = Order.objects.create(
                        cart=cart,
                        total=cart.total,
                        payment_id=payment_id,
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
                    "cart_id": cart_id,
                    "order_id": order.id,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid payment response"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@csrf_exempt
def yookassa_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            payment_id = data.get("object", {}).get("id")
            status = data.get("object", {}).get("status")

            if payment_id and status:
                try:
                    order = Order.objects.get(payment_id=payment_id)
                    order.payment_status = status
                    order.save()
                    return JsonResponse({"status": "success"}, status=200)
                except Order.DoesNotExist:
                    return JsonResponse({"error": "Order not found"}, status=404)
            else:
                return JsonResponse({"error": "Invalid data"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)

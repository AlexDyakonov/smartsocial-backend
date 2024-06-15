import json

from apps.booking.models import Buyer, Cart
from apps.payments.models import Order
from apps.tickets.generator import generate_ticket
from apps.tickets.utils import get_ticket_info
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Order
from .serializers import PaymentProcessingSerializer, PaymentStatusSerializer
from .services import YooKassaService


class PaymentStatusView(generics.RetrieveAPIView):
    serializer_class = PaymentStatusSerializer

    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get("payment_id")
        order = Order.objects.filter(payment_id=payment_id).first()

        if not order:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if order.payment_status == "succeeded" and order.ticket_file:
            return Response(
                {
                    "payment_status": "succeeded",
                    "ticket_url": f"{order.ticket_file.url}",
                    "total": f"{order.total}",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "payment_status": order.payment_status,
                    "total": f"{order.total}",
                },
                status=status.HTTP_200_OK,
            )


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
                    order = Order.objects.filter(payment_id=payment_id).first()
                    order.payment_status = status
                    order.save()

                    if generate_ticket(get_ticket_info(payment_id), payment_id):
                        return JsonResponse({"status": "success"}, status=200)
                    else:
                        return Response(
                            {"error": "Error creating ticket"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )

                except Order.DoesNotExist:
                    return JsonResponse({"error": "Order not found"}, status=404)
            else:
                return JsonResponse({"error": "Invalid data"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)

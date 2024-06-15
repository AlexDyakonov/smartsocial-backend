from apps.booking.models import Buyer
from rest_framework import serializers

from .models import Order


class BuyerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ["email", "phone", "first_name", "last_name"]


class PaymentProcessingSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField(required=True)
    buyer = BuyerPaymentSerializer(required=True)


class PaymentStatusSerializer(serializers.Serializer):
    payment_id = serializers.CharField(required=True)


class PaymentListOutputSerializer(serializers.ModelSerializer):
    buyer = BuyerPaymentSerializer(source="cart.buyer", read_only=True)

    class Meta:
        model = Order
        fields = [
            "buyer",
            "payment_id",
            "total",
            "created_at",
            "payment_status",
            "ticket_file",
        ]

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


class PaymentIdSerializer(serializers.Serializer):
    payment_id = serializers.CharField(help_text="Unique identifier for a payment.")

    def validate_payment_id(self, value):
        """
        Check that the payment_id exists in the database and is associated with an order.
        You might want to add more complex validations depending on your business logic.
        """
        if not Order.objects.filter(payment_id=value).exists():
            raise serializers.ValidationError(
                "No order found with the given payment ID."
            )
        return value


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


class PaymentItemInputSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField(required=True)
    total = serializers.FloatField(required=True)

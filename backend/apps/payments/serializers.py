from apps.booking.models import Buyer
from rest_framework import serializers


class BuyerPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ["email", "phone", "first_name", "last_name"]


class PaymentProcessingSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField(required=True)
    buyer = BuyerPaymentSerializer(required=True)

from rest_framework import serializers


class PaymentProcessingSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField(required=True)

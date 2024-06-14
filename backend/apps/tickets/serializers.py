from rest_framework import serializers


class OrderPaymentIdSerializer(serializers.Serializer):
    order_id = serializers.CharField(required=True, max_length=36)

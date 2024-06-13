from apps.core.models import Ticket
from apps.core.serializers import TicketSerializer
from rest_framework import serializers

from .models import Buyer, Cart, CartTicket


class CartTicketInputSerializer(serializers.ModelSerializer):
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())

    class Meta:
        model = CartTicket
        fields = ("ticket", "time", "quantity")


class CartTicketOutputSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(many=False)

    class Meta:
        model = CartTicket
        fields = ("id", "ticket", "time", "quantity")


class CartInputSerializer(serializers.ModelSerializer):
    tickets = CartTicketInputSerializer(many=True)
    buyer = serializers.PrimaryKeyRelatedField(
        queryset=Buyer.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Cart
        fields = ("id", "buyer", "tickets")

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        cart = Cart.objects.create(**validated_data)
        for ticket_data in tickets_data:
            CartTicket.objects.create(cart=cart, **ticket_data)
        return cart

    def update(self, instance, validated_data):
        tickets_data = validated_data.pop("tickets", [])
        CartTicket.objects.filter(cart=instance).delete()
        for ticket_data in tickets_data:
            CartTicket.objects.create(cart=instance, **ticket_data)
        return instance


class CartOutputSerializer(serializers.ModelSerializer):
    buyer = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    tickets = CartTicketOutputSerializer(many=True)

    class Meta:
        model = Cart
        fields = ("id", "buyer", "created_at", "tickets")


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ("id", "email", "phone", "first_name", "last_name")

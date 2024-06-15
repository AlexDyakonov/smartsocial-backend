from apps.core.models import Ticket, Event
from apps.core.serializers import TicketSerializer, EventSerializer
from rest_framework import serializers

from .models import Buyer, Cart, CartTicket


class CartTicketInputSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    personas = serializers.SerializerMethodField()
    id = serializers.IntegerField(source='ticket.id', read_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    event_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CartTicket
        fields = ("ticket", "time", "quantity", "name", "type", "price", "personas", "id", "event", "event_name")

    def get_name(self, obj):
        return obj.ticket.name

    def get_event_id(self, obj: CartTicket):
        return obj.ticket

    def get_event_name(self, obj):
        return obj.event.name

    def get_type(self, obj):
        return obj.ticket.type

    def get_price(self, obj):
        return obj.ticket.price

    def get_personas(self, obj):
        return obj.ticket.personas


class CartTicketOutputSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(many=False)
    event = EventSerializer(many=False)

    class Meta:
        model = CartTicket
        fields = ("id", "ticket", "time", "quantity", "event")


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

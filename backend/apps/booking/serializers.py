from datetime import datetime

from .models import Buyer, Cart, CartTicket, Booking

from rest_framework import serializers

from apps.core.models import Ticket, Event
from apps.core.serializers import TicketSerializer


class CartTicketSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ticket.name', read_only=True)
    type = serializers.CharField(source='ticket.type', read_only=True)
    price = serializers.DecimalField(source='ticket.price', max_digits=10, decimal_places=2, read_only=True)
    personas = serializers.IntegerField(source='ticket.personas', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)

    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    ticket_id = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())

    class Meta:
        model = CartTicket
        fields = ['ticket_id', 'name', 'type', 'price', 'personas', 'event_id', 'event_name', 'quantity',
                  'time']


class CartSerializer(serializers.ModelSerializer):
    tickets = CartTicketSerializer(many=True)

    class Meta:
        model = Cart
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        cart = Cart.objects.create(**validated_data)
        for ticket_data in tickets_data:
            CartTicket.objects.create(
                cart=cart,
                ticket=ticket_data.get('ticket_id'),
                event=ticket_data.get('event_id'),
                time=ticket_data.get('time'),
                quantity=ticket_data.get('quantity'),
            )
        return cart

    def update(self, instance, validated_data):
        tickets_data = validated_data.pop('tickets')
        instance.buyer = validated_data.get('buyer', instance.buyer)
        instance.save()

        for ticket_data in tickets_data:
            ticket_id = ticket_data.get('ticket_id').id
            event_id = ticket_data.get('event_id').id
            CartTicket.objects.update_or_create(
                cart=instance,
                ticket_id=ticket_id,
                event_id=event_id,
                defaults={
                    'quantity': ticket_data.get('quantity', 0),
                    'time': ticket_data.get('time')
                }
            )

        return instance


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ("id", "email", "phone", "first_name", "last_name")


class BookingSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(many=False, read_only=True)

    class Meta:
        model = Booking
        fields = ("id", "event", "ticket", "time", "visited", "quantity")

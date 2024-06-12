from apps.core.models import Event, Ticket
from django.db import models


class Buyer(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class Cart(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartTicket(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="tickets")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    time = models.DateTimeField()
    quantity = models.IntegerField()


class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    time = models.DateTimeField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

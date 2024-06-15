from apps.booking.models import Cart
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.booking.models import Booking


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    confirmation_token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_file = models.FileField(upload_to="tickets/", null=True, blank=True)
    qr_code = models.ImageField(upload_to="qr_codes/", null=True, blank=True)

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Ожидание оплаты"),
        ("waiting_for_capture", "Платеж оплачен, ожидают списания"),
        ("succeeded", "Платеж успешно завершен"),
        ("canceled", "Платеж отменен"),
    ]

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
    )


@receiver(post_save, sender=Order)
def create_bookings(sender, instance, **kwargs):
    print(instance.cart.tickets.all())
    for t in instance.cart.tickets.all():
        for _ in range(t.quantity):
            Booking.objects.create(
                event=t.event,
                ticket=t.ticket,
                time=t.time,
                cart=t.cart
            )

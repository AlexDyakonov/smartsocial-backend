from apps.booking.models import Cart
from django.db import models


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    confirmation_token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_file = models.FileField(upload_to="tickets/", null=True, blank=True)

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

from booking.models import Cart
from django.db import models


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    return_url = models.TextField(null=True, blank=True)
    confirmation_token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Ожидание оплаты"),
        ("paid", "Оплачено"),
        ("failed", "Ошибка оплаты"),
        ("refunded", "Возврат средств"),
    ]

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
    )

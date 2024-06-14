from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cart",
        "total",
        "payment_id",
        "payment_status",
        "created_at",
        "ticket_file",
    )
    list_filter = ("payment_status", "created_at")
    search_fields = ("cart__id", "payment_id", "confirmation_token")


admin.site.register(Order, OrderAdmin)

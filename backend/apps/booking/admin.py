from django.contrib import admin

from .models import Booking, Buyer, Cart, CartTicket


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone", "first_name", "last_name")
    search_fields = ("id", "email", "phone", "first_name", "last_name")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "created_at")
    list_filter = ("buyer", "created_at")
    search_fields = ("id",)
    readonly_fields = ("id", "created_at")


@admin.register(CartTicket)
class CartTicketAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "ticket", "time", "quantity")
    list_filter = ("time", "quantity")
    search_fields = ("id",)
    readonly_fields = ("id",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "ticket", "time", "cart", "file")
    list_filter = ("time",)
    search_fields = ("id",)
    readonly_fields = ("id",)

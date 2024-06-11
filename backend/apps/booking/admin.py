from django.contrib import admin
from .models import Buyer, Cart, CartTicket, Booking, Order


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'first_name', 'last_name')
    search_fields = ('id', 'email', 'phone', 'first_name', 'last_name')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'created_at')
    list_filter = ('buyer', 'created_at')
    search_fields = ('id',)
    readonly_fields = ('id', 'created_at')

    def has_add_permission(self, request):
        # Disable the ability to add new carts directly from the admin
        return False


@admin.register(CartTicket)
class CartTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'ticket', 'time', 'quantity')
    list_filter = ('time', 'quantity')
    search_fields = ('id',)
    readonly_fields = ('id',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'ticket', 'time', 'cart')
    list_filter = ('time',)
    search_fields = ('id',)
    readonly_fields = ('id',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'payment', 'status', 'total')
    list_filter = ('status',)
    search_fields = ('id', 'payment', 'status')
    readonly_fields = ('id',)

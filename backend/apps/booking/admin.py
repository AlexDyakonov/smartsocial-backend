from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'created_at')
    list_filter = ('buyer', 'created_at')
    search_fields = ('id',)
    readonly_fields = ('id', 'created_at')

    def has_add_permission(self, request):
        # Disable the ability to add new carts directly from the admin
        return False

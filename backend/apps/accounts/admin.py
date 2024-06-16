from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_admin",
        "place",
    )
    list_filter = ("is_admin", "is_active", "place")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "middle_name",
                    "last_name",
                    "phone_number",
                    "place",
                )
            },
        ),
        (_("Permissions"), {"fields": ("is_active", "is_admin")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "password1",
                    "password2",
                    "place",
                ),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name", "phone_number")
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)

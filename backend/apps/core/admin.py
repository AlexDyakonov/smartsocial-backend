from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin

from .models import Event, Image, Place, Ticket


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ("image_tag",)
    fields = ("image_tag", "image", "caption")


@admin.register(Place)
class PlaceAdmin(GISModelAdmin):
    list_display = ("id", "name", "location")
    search_fields = ("name", "address")
    inlines = [ImageInline]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "place", "duration_minutes")
    search_fields = ("name", "place__name")


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "price", "place", "personas")
    search_fields = ("name", "type", "event__name")

from django.contrib import admin
from .models import Place, Event, Ticket
from django.contrib.gis.admin import GISModelAdmin


@admin.register(Place)
class PlaceAdmin(GISModelAdmin):
    list_display = ('id', 'name', 'location')
    search_fields = ('name', 'address')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'place', 'duration_minutes')
    search_fields = ('name', 'place__name')


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'price', 'place', 'personas')
    search_fields = ('name', 'type', 'event__name')

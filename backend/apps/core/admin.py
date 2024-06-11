from django.contrib import admin
from .models import Place, Event, Ticket, Schedule
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
    list_display = ('id', 'name', 'ticket_type', 'price', 'event', 'personas')
    search_fields = ('name', 'ticket_type', 'event__name')


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'min_capacity', 'max_capacity')
    search_fields = ('event__name',)

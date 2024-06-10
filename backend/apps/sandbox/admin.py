from django.contrib import admin
from .models import Point
from django.contrib.gis.admin import GISModelAdmin


@admin.register(Point)
class PointAdmin(GISModelAdmin):
    list_display = ('id', 'location')

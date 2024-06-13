import django.contrib.gis.geos as geos
from rest_framework import serializers

from .models import Event, Place, Ticket


class PointField(serializers.Field):
    def to_representation(self, value):
        return {"lat": value.y, "lon": value.x}

    def to_internal_value(self, data):
        try:
            lat = data["lat"]
            lon = data["lon"]
            return geos.Point(x=lon, y=lat)
        except (KeyError, TypeError):
            raise serializers.ValidationError("Invalid input for a Point instance.")


class PlaceInputSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = Place
        fields = ("name", "description", "address", "location", "images")


class PlaceOutputSerializer(serializers.ModelSerializer):
    location = PointField()

    class Meta:
        model = Place
        fields = ("id", "name", "description", "address", "location", "images")


class EventSerializer(serializers.ModelSerializer):
    place = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all())

    class Meta:
        model = Event
        fields = (
            "id",
            "place",
            "name",
            "description",
            "duration_minutes",
            "icalendar_data",
            "min_capacity",
            "max_capacity",
            "tickets",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "name", "type", "price", "place", "personas")

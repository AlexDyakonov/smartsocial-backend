from rest_framework import serializers
from .models import Place, Event, Ticket, Schedule
import django.contrib.gis.geos as geos


class PlaceInputSerializer(serializers.ModelSerializer):
    location = serializers.ListField(child=serializers.FloatField())

    class Meta:
        model = Place
        fields = ('name', 'description', 'address', 'location', 'images')

    def create(self, validated_data):
        location = geos.Point(validated_data.pop('location')[0], validated_data.pop('location')[1])
        return Place.objects.create(location=location, **validated_data)

    def update(self, instance, validated_data):
        instance.location = geos.Point(validated_data.pop('location')[0], validated_data.pop('location')[1])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class PlaceOutputSerializer(serializers.ModelSerializer):
    location = serializers.ListField(child=serializers.FloatField())

    class Meta:
        model = Place
        fields = ('id', 'name', 'description', 'address', 'location', 'images')


class EventSerializer(serializers.ModelSerializer):
    place = serializers.PrimaryKeyRelatedField(queryset=Place.objects.all())

    class Meta:
        model = Event
        fields = ('id', 'place', 'name', 'description', 'duration_minutes')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'name', 'ticket_type', 'price', 'event', 'personas')


class ScheduleSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), many=True)

    class Meta:
        model = Schedule
        fields = ('id', 'event', 'min_capacity', 'max_capacity', 'icalendar_data', 'tickets')

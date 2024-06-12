from rest_framework import serializers
from .models import Place, Event, Ticket
import django.contrib.gis.geos as geos


class PlaceInputSerializer(serializers.ModelSerializer):
    location = serializers.ListField(child=serializers.FloatField())

    class Meta:
        model = Place
        fields = ('name', 'description', 'address', 'location', 'images')

    def create(self, validated_data):
        location_list = validated_data.pop('location')
        location = geos.Point(location_list[0], location_list[1])
        return Place.objects.create(location=location, **validated_data)

    def update(self, instance, validated_data):
        location_list = validated_data.pop('location')
        instance.location = geos.Point(location_list[0], location_list[1])
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
        fields = (
            'id',
            'place',
            'name',
            'description',
            'duration_minutes',
            'icalendar_data',
            'min_capacity',
            'max_capacity',
            'tickets',
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'name', 'type', 'price', 'place', 'personas')

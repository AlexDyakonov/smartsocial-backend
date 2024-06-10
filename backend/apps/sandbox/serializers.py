from rest_framework import serializers
from .models import Point
import django.contrib.gis.geos as geos


class PointInputSerializer(serializers.ModelSerializer):
    location = serializers.ListField(child=serializers.FloatField())

    class Meta:
        model = Point
        fields = ('location',)

    def create(self, validated_data):
        location = geos.Point(validated_data['location'][0], validated_data['location'][1])
        return Point.objects.create(location=location)

    def update(self, instance, validated_data):
        instance.location = geos.Point(validated_data['location'][0], validated_data['location'][1])
        instance.save()
        return instance


class PointOutputSerializer(serializers.ModelSerializer):
    location = serializers.ListField(child=serializers.FloatField())

    class Meta:
        model = Point
        fields = ('location',)

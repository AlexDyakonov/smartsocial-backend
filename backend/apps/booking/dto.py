import dataclasses
from datetime import datetime
from rest_framework import serializers


@dataclasses.dataclass
class EventWithDate:
    id: int
    place_id: int
    name: str
    description: str
    capacity: int
    start_datetime: datetime
    end_datetime: datetime


@dataclasses.dataclass
class TicketWithDate:
    ticket_id: int
    event_name: str
    event_id: int
    name: str
    type: str
    price: int
    personas: int
    time: datetime


class EventWithDateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    place_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    capacity = serializers.IntegerField()
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()

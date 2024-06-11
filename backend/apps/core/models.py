from django.db import models
from django.contrib.gis.db import models as gis_models
import icalendar as ical


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    location = gis_models.PointField()
    images = models.JSONField()

    def __str__(self):
        return self.name


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration_minutes = models.IntegerField()

    def __str__(self):
        return self.name


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    ticket_type = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    personas = models.IntegerField()

    def __str__(self):
        return self.name


class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    min_capacity = models.IntegerField()
    max_capacity = models.IntegerField()
    icalendar_data = models.TextField()
    tickets = models.ManyToManyField(Ticket)

    def icalendar(self):
        return ical.Calendar.from_ical(self.icalendar)

    def __str__(self):
        return f"{self.event.name}"

import os

import icalendar as ical
from django.contrib.gis.db import models as gis_models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify


class Place(models.Model):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    abbreviation = models.CharField(max_length=56, blank=True, null=True)
    description = models.TextField(null=False, blank=False)
    address = models.TextField(null=False, blank=False)
    location = gis_models.PointField()

    def __str__(self):
        return self.name


def get_image_path(instance, filename):
    clean_name = slugify(instance.place.name)
    return os.path.join("place_images", clean_name, filename)


class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=get_image_path)
    caption = models.CharField(max_length=255, blank=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.image.url)

    image_tag.short_description = "Image"

    def __str__(self):
        return self.caption if self.caption else f"Изображение {self.place.name}"


class Ticket(models.Model):
    TICKET_TYPE_CHOICES = [
        ("family", "Семейный"),
        ("group", "Групповой"),
        ("adult", "Взрослый"),
        ("child", "Детский"),
        ("discount", "Льготный"),
    ]

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TICKET_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    personas = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class Event(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False, blank=False)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=False, blank=False)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(0)])
    icalendar_data = models.TextField()
    min_capacity = models.IntegerField(validators=[MinValueValidator(0)])
    max_capacity = models.IntegerField(validators=[MinValueValidator(0)])
    tickets = models.ManyToManyField(Ticket)

    def icalendar(self):
        return ical.Calendar.from_ical(self.icalendar_data)

    def __str__(self):
        return self.name

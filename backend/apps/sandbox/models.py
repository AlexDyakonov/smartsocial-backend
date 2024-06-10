from django.contrib.gis.db import models


class Point(models.Model):
    location = models.PointField()

    def __str__(self):
        return f"Point({self.location.x}, {self.location.y})"

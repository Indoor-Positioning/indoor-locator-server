from django.db import models


# Create your models here.
class FloorPlan(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField()

    def __str__(self):
        return self.name


class FingerPrintedLocation(models.Model):
    floor_plan = models.ForeignKey('FloorPlan')
    x_coord = models.FloatField()
    y_coord = models.FloatField()


class PointOfInterest(models.Model):
    name = models.CharField(max_length=20)
    floor_plan = models.ForeignKey('FloorPlan')
    x_coord = models.FloatField()
    y_coord = models.FloatField()

    def __str__(self):
        return self.name


class FingerPrint(models.Model):
    location = models.ForeignKey('FingerPrintedLocation')
    magnetic_x = models.FloatField()
    magnetic_y = models.FloatField()
    magnetic_z = models.FloatField()
    orientation_x = models.FloatField()
    orientation_y = models.FloatField()
    orientation_z = models.FloatField()
    wifi_rssi = models.FloatField()
import json

from django.db import models
from django.conf import settings


# Create your models here.
class FloorPlan(models.Model):
    name = models.CharField(max_length=40)
    resource_name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def as_json(self):
        return dict(
            id=self.id,
            name=self.name,
            resourceName=self.resource_name
        )


class FingerPrintedLocation(models.Model):
    floor_plan = models.ForeignKey('FloorPlan')
    related_poi = models.ForeignKey('PointOfInterest', blank=True, null=True)
    is_poi = models.BooleanField(default=False)
    x_coord = models.FloatField()
    y_coord = models.FloatField()

    def __str__(self):
        return  "ID: {} FLOOR_PLAN: {}".format(self.id, self.floor_plan.__str__())

    def as_json(self):
        return dict(
            id=self.id,
            floorPlanId=self.floor_plan_id,
            relatedPoi=self.related_poi_id if self.is_poi else -1,
            isPoi=self.is_poi,
            xCoord=self.x_coord,
            yCoord=self.y_coord
        )

    def as_poi_json(self):
        if self.is_poi:
            poi = PointOfInterest.objects.get(pk=self.related_poi_id)
            return dict(
                id=poi.id,
                name=poi.name if poi.name is not None else "N/A",
                floorPlanId=self.floor_plan_id,
                relatedFingerPrintedLocId=self.id,
                xCoord=self.x_coord,
                yCoord=self.y_coord)

    @classmethod
    def add_from_json(cls, location):
        loc = FingerPrintedLocation()
        loc.floor_plan_id = location["floorPlanId"]
        loc.is_poi = location["isPoi"]
        loc.x_coord = location["xCoord"]
        loc.y_coord = location["yCoord"]
        loc.save()
        return loc

    @classmethod
    def add_poi_from_json(cls, poi):
        related_loc = FingerPrintedLocation()
        related_loc.floor_plan_id = poi["floorPlanId"]
        related_loc.is_poi = True
        related_loc.x_coord = poi["xCoord"]
        related_loc.y_coord = poi["yCoord"]
        related_loc.save()

        poi = PointOfInterest()
        poi.save()
        related_loc.related_poi_id = poi.id
        related_loc.save()
        return related_loc


class Creator(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name  + ' ' + self.last_name


class PointOfInterest(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='pointOfInterest/', blank=True)
    creator = models.ForeignKey(Creator, null=True)

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

    def __str__(self):
        return self.location.floor_plan.__str__()

    @classmethod
    def add_from_json(cls, fingerprints):
        for fingerprint in fingerprints:
            fp = FingerPrint()
            fp.location_id = fingerprint["fingerPrintedLocationId"]
            fp.magnetic_x = fingerprint["magneticX"]
            fp.magnetic_y = fingerprint["magneticY"]
            fp.magnetic_z = fingerprint["magneticZ"]
            fp.orientation_x = fingerprint["orientationX"]
            fp.orientation_y = fingerprint["orientationY"]
            fp.orientation_z = fingerprint["orientationZ"]
            fp.wifi_rssi = fingerprint["wifiRssi"]
            fp.save()

    @classmethod
    def get_from_json(cls, fingerprint):
        fp = FingerPrint()
        fp.magnetic_x = fingerprint["magneticX"]
        fp.magnetic_y = fingerprint["magneticY"]
        fp.magnetic_z = fingerprint["magneticZ"]
        fp.orientation_x = fingerprint["orientationX"]
        fp.orientation_y = fingerprint["orientationY"]
        fp.orientation_z = fingerprint["orientationZ"]
        fp.wifi_rssi = fingerprint["wifiRssi"]
        return fp


class UserLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    location = models.ForeignKey(FingerPrintedLocation)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.user.username

import json

from django.db import models


# Create your models here.
class FloorPlan(models.Model):
    name = models.CharField(max_length=40)
    resource_name = models.CharField(max_length=20)

    def __str__(self):
        return "ID: {}, Name: {}".format(self.id, self.name)

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

    def as_json(self):
        return dict(
            id=self.id,
            floorPlanId=self.floor_plan_id,
            relatedPoi=self.related_poi_id if self.related_poi is not None else -1,
            isPoi=self.is_poi,
            xCoord=self.x_coord,
            yCoord=self.y_coord
        )

    @classmethod
    def add_from_json(cls, location):
        loc = FingerPrintedLocation()
        loc.floor_plan_id = location["floorPlanId"]
        loc.is_poi = location["isPoi"]
        loc.x_coord = location["xCoord"]
        loc.y_coord = location["yCoord"]
        loc.save()
        return loc

    def __str__(self):
        return "ID: {},  X: {:.2f},   Y: {:.2f}".format(self.id, self.x_coord, self.y_coord)


class PointOfInterest(models.Model):
    name = models.CharField(max_length=20)
    floor_plan = models.ForeignKey('FloorPlan')
    fingerprinted_loc = models.ForeignKey('FingerPrintedLocation')
    x_coord = models.FloatField()
    y_coord = models.FloatField()

    @classmethod
    def add_from_json(cls, poi_json):
        related_loc = FingerPrintedLocation()
        related_loc.floor_plan_id = poi_json["floorPlanId"]
        related_loc.is_poi = True
        related_loc.x_coord = poi_json["xCoord"]
        related_loc.y_coord = poi_json["yCoord"]
        related_loc.save()

        poi = PointOfInterest()
        poi.floor_plan_id = poi_json["floorPlanId"]
        poi.fingerprinted_loc_id = related_loc.id
        poi.x_coord = poi_json["xCoord"]
        poi.y_coord = poi_json["yCoord"]
        poi.save()
        related_loc.related_poi_id = poi.id
        related_loc.save()
        return poi

    def as_json(self):
        return dict(
            id=self.id,
            name=self.name if self.name is not None else "N/A",
            floorPlanId=self.floor_plan_id,
            relatedFingerPrintedLocId=self.fingerprinted_loc_id,
            xCoord=self.x_coord,
            yCoord=self.y_coord)

    def __str__(self):
        return "ID: {},  X: {:.2f},   Y: {:.2f}".format(self.id, self.x_coord, self.y_coord)


class FingerPrint(models.Model):
    location = models.ForeignKey('FingerPrintedLocation')
    magnetic_x = models.FloatField()
    magnetic_y = models.FloatField()
    magnetic_z = models.FloatField()
    orientation_x = models.FloatField()
    orientation_y = models.FloatField()
    orientation_z = models.FloatField()
    wifi_rssi = models.FloatField()

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

    def __str__(self):
        return "Magnetic field: ({:.2f}, {:.2f}, {:.2f}), Orientation: ({:.2f}, {:.2f}, {:.2f}), Rssi: {: .2f}"\
            .format(self.magnetic_x, self.magnetic_y, self.magnetic_z, self.orientation_x,
                    self.orientation_y, self.magnetic_z, self.wifi_rssi)
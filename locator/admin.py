from django.contrib import admin
from .models import *

# Register your models here.

class FloorPanAdmin(admin.ModelAdmin):
    model = FloorPlan
    list_display = ('__str__', 'id_with_name', )

    def id_with_name(self, obj):
        return "ID: {}, Name: {}".format(obj.id, obj.name)


class PointOfInterestAdmin(admin.ModelAdmin):
    model = PointOfInterest
    list_display = ('__str__', 'floor_plan' ,'id_with_coords', )

    def id_with_coords(self, obj):
        return "ID: {},  X: {:.2f},   Y: {:.2f}".format(obj.id, obj.x_coord, obj.y_coord)


class FingerPrintedLocationAdmin(admin.ModelAdmin):
    model = FingerPrintedLocation
    list_display = ('__str__', 'floor_plan', 'related_poi', 'is_poi', )



admin.site.register(FloorPlan, FloorPanAdmin)
admin.site.register(PointOfInterest, PointOfInterestAdmin)
admin.site.register(FingerPrintedLocation, FingerPrintedLocationAdmin)
admin.site.register(FingerPrint)

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
    list_display = ('__str__', 'return_id', )

    def return_id(self, obj):
        return "ID: {}".format(obj.id)


class FingerPrintedLocationAdmin(admin.ModelAdmin):
    model = FingerPrintedLocation
    list_display = ('__str__', 'is_poi', 'related_poi', )
    list_filter = ('floor_plan', )


class FingerPrintAdmin(admin.ModelAdmin):
    model = FingerPrint
    list_display = ('__str__', 'metrics_summary',)
    list_filter = ('location__floor_plan', )


    def metrics_summary(self, obj):
        return "Magnetic field: ({:.2f}, {:.2f}, {:.2f}), Orientation: ({:.2f}, {:.2f}, {:.2f}), Rssi: {: .2f}"\
                .format(obj.magnetic_x, obj.magnetic_y, obj.magnetic_z, obj.orientation_x,
                    obj.orientation_y, obj.magnetic_z, obj.wifi_rssi)


admin.site.register(FloorPlan, FloorPanAdmin)
admin.site.register(PointOfInterest, PointOfInterestAdmin)
admin.site.register(FingerPrintedLocation, FingerPrintedLocationAdmin)
admin.site.register(FingerPrint, FingerPrintAdmin)

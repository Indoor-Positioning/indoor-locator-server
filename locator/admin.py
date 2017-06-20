from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(
    [FloorPlan, FingerPrintedLocation, PointOfInterest, FingerPrint]
)

from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Creator, PointOfInterest, FingerPrintedLocation


class PointsOfInterestSuggestionView(View):
    def get(self, request, *args, **kwargs):
        creator_id = self.request.GET.get('creator', None)
        creator = get_object_or_404(Creator, pk=creator_id)
        points_of_interest = PointOfInterest.objects.filter(creator=creator)
        results = FingerPrintedLocation.objects.filter(related_poi__in=points_of_interest).values('floor_plan_id', 'x_coord', 'y_coord', 'related_poi__name', 'related_poi__image')
        return JsonResponse({'results': list(results)},status=200, safe=False)
        

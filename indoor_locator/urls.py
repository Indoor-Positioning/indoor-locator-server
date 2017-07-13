"""indoor_locator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from locator.models import UserLocation
from locator.views import PointsOfInterestSuggestionView

class HomePageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        # TODO: Needs Optimization
        # TODO: Display only todays locations
        # TODO: filter by Floor PLAN
        context['old_locations'] = UserLocation.objects.all()
        context['users'] = UserLocation.objects.values('user_id', 'user__username').distinct()
        return context



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePageView.as_view(template_name="index.html"), name="homepage"),
    url(r'^suggestions/$', PointsOfInterestSuggestionView.as_view(), name="suggestions"),
]

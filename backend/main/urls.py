from django.urls import path, include
from . import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'schools', views.SchoolView)
router.register(r'city', views.CityView)
router.register(r'country', views.CountryView)


urlpatterns = [
    path("", include(router.urls)),

]

from rest_framework import viewsets, permissions, filters
from . import models, serializer
from django_filters.rest_framework import DjangoFilterBackend


class CountryView(viewsets.ModelViewSet):
    """Country ViewSet"""
    queryset = models.Country.objects.all()
    serializer_class = serializer.CountrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CityView(viewsets.ModelViewSet):
    """City ViewSet"""
    queryset = models.City.objects.all()
    serializer_class = serializer.CitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', ]
    
    
class SchoolView(viewsets.ModelViewSet):
    """School ViewSet"""
    queryset = models.School.objects.all()
    serializer_class = serializer.SchoolSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['city', "city__country"]

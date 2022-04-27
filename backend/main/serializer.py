
from rest_framework import serializers
from . import models


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ("id", "title")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = ("id", "title")


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.School
        fields = ("__all__")


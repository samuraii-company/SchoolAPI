from django.test import TestCase
from main.models import Country, City
from main.serializer import CountrySerializer, CitySerializer
from oauth.serializer import RegisterSerializer
from rest_framework import serializers
from oauth.models import User


class CountrySerializerTestCase(TestCase):
    def test_ok(self):
        """
        Test Country Serializer
        """
        country1 = Country.objects.create(title="Russia")
        country2 = Country.objects.create(title="Germany")
        data = CountrySerializer([country1, country2], many=True).data
        
        expected_adta = [
            {
                "id": country1.id,
                "title": "Russia"
            },
            {
                "id": country2.id,
                "title": "Germany"
            },
        ]
        
        self.assertEqual(data, expected_adta)
        
        
class CitySerializerTestCase(TestCase):
    def test_ok(self):
        """
        Test City Serializer
        """
        country = Country.objects.create(title="Russia")
        city = City.objects.create(title="Moscow", country=country)
        city2 = City.objects.create(title="Ufa", country=country)
        
        data = CitySerializer([city,city2], many=True).data
        
        expected_adta = [
            {
                "id": city.id,
                "title": "Moscow"
            },
            {
                "id": city2.id,
                "title": "Ufa"
            },
        ]
        
        self.assertEqual(data, expected_adta)

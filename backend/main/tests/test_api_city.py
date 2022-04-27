from rest_framework.test import APITestCase, APIClient
from main.models import City, Country
from main.serializer import CitySerializer
from django.urls import reverse
from rest_framework import status
from oauth.models import User
import json

class CityLogicTestCase(APITestCase):
    def setUp(self):
        self.country1 = Country.objects.create(title="Russia")
        self.country2 = Country.objects.create(title="USA")
        self.city = City.objects.create(title="Moscow", country=self.country1)
        self.city2 = City.objects.create(title="New York", country=self.country2)
        self.city3 = City.objects.create(title="Ufa", country=self.country1)
        self.city4 = City.objects.create(title="Miami", country=self.country2)

        self.user = User.objects.create(
            email="test@gmail.com",
            password="1234567890",
        )
        self.client = APIClient()

    def test_get_all(self):
        """
        Test Get all citys
        """
        url = reverse("city-list")
        response = self.client.get(url)
        serializer_data = CitySerializer([self.city, self.city2, self.city3, self.city4], many=True).data
        
        count = City.objects.all().count()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(count, len(response.data))
        self.assertEqual(serializer_data, response.data)
        
    def test_by_id(self):
        """
        Test city by id
        """
        url = reverse("city-detail",  kwargs={'pk': 2})
        response = self.client.get(url)
        serializer_data = CitySerializer(self.city2).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        
    def test_create_city_fail(self):
        """
        Test create city [UNAUTHORIZED]
        return 401 status code
        """
        url = reverse("city-list")
        response = self.client.post(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_create_city_success(self):
        """
        Test create city
        return 201 status code
        """
        self.client.force_authenticate(user=self.user)

        url = reverse("country-list")
        data = {"title": "Kirov"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual("Kirov", response.data.get("title"))
        
    def test_update_city_fail(self):
        """
        Test update city [UNAUTHORIZED]
        return 401 status code
        """
        url = reverse("country-detail", kwargs={'pk': 1})
        response = self.client.put(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_update_city_success(self):
        """
        Test update city
        return 200 status code
        """
        self.client.force_authenticate(user=self.user)

        url = reverse("country-detail", kwargs={'pk': 1})
        data = {"title": "Ufa"}
        old_country = City.objects.filter(id=1).first()
        _old = CitySerializer(old_country).data
        self.assertEqual("Moscow", _old.get("title"))
        
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("Ufa", response.data.get("title"))
        
        
    def test_delete_city_fail(self):
        """
        Test delete city [UNAUTHORIZED]
        return 401 status code
        """
        url = reverse("country-detail", kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_delete_city_success(self):
        """
        Test delete city
        return 200 status code
        """
        self.client.force_authenticate(user=self.user)
        old_count = City.objects.all().count()
        self.assertEqual(4, old_count)
        url = reverse("city-detail", kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        new_count = City.objects.all().count()
        self.assertEqual(3, new_count)
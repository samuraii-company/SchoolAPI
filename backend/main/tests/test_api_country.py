from rest_framework.test import APITestCase, APIClient
from main.models import Country
from main.serializer import CountrySerializer
from django.urls import reverse
from rest_framework import status
from oauth.models import User
import json

class CountryLogicTestCase(APITestCase):
    def setUp(self):
        self.country1 = Country.objects.create(title="Russia")
        self.country2 = Country.objects.create(title="Germany")
        self.user = User.objects.create(
            email="test@gmail.com",
            password="1234567890",
        )
        self.client = APIClient()

    def test_get_all(self):
        """
        Test Get all country
        """
        url = reverse("country-list")
        response = self.client.get(url)
        serializer_data = CountrySerializer([self.country1, self.country2], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        
    def test_by_id(self):
        """
        Test country by id
        """
        url = reverse("country-detail",  kwargs={'pk': 1})
        response = self.client.get(url)
        serializer_data = CountrySerializer(self.country1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        
    def test_create_country_fail(self):
        """
        Test create country [UNAUTHORIZED]
        return 401 status code
        """
        url = reverse("country-list")
        response = self.client.post(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_create_country_success(self):
        """
        Test create country
        return 201 status code
        """
        self.client.force_authenticate(user=self.user)

        url = reverse("country-list")
        data = {"title": "USA"}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual("USA", response.data.get("title"))
        
    def test_update_country_fail(self):
        """
        Test update country [UNAUTHORIZED]
        return 401 status code
        """
        url = reverse("country-detail", kwargs={'pk': 1})
        response = self.client.put(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_update_country_success(self):
        """
        Test update country
        return 200 status code
        """
        self.client.force_authenticate(user=self.user)

        url = reverse("country-detail", kwargs={'pk': 1})
        data = {"title": "USA"}
        old_country = Country.objects.filter(id=1).first()
        _old = CountrySerializer(old_country).data
        self.assertEqual("Russia", _old.get("title"))
        
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("USA", response.data.get("title"))
        
        
    def test_delete_country_fail(self):
        """
        Test delete country [UNAUTHORIZED]
        return 401 status code
        """
        url = reverse("country-detail", kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_delete_country_success(self):
        """
        Test delete country
        return 200 status code
        """
        self.client.force_authenticate(user=self.user)
        old_count = Country.objects.all().count()
        self.assertEqual(2, old_count)
        url = reverse("country-detail", kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        new_count = Country.objects.all().count()
        self.assertEqual(1, new_count)
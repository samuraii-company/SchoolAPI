from rest_framework.test import APITestCase, APIClient
from main.models import City, Country, School
from main.serializer import SchoolSerializer
from django.urls import reverse
from rest_framework import status
from oauth.models import User
import json

class SchoolLogicTestCase(APITestCase):
    def setUp(self):
        self.country1 = Country.objects.create(title="Russia")
        self.city = City.objects.create(title="Moscow", country=self.country1)
        self.school = School.objects.create(
            title="Test",
            city=self.city
        )
        self.school2 = School.objects.create(
            title="Test2",
            city=self.city
        )
        self.user = User.objects.create(
            email="test@gmail.com",
            password="1234567890",
        )
        self.client = APIClient()

    def test_get_all(self):
        """
        Test Get all schools
        """
        url = reverse("school-list")
        response = self.client.get(url)
        serializer_data = SchoolSerializer([self.school, self.school2], many=True).data
        
        count = School.objects.all().count()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(count, len(response.data))
        self.assertEqual(serializer_data, response.data)
        
    def test_by_id(self):
        """
        Test school by id
        """
        url = reverse("school-detail",  kwargs={'pk': 1})
        response = self.client.get(url)
        serializer_data = SchoolSerializer(self.school).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        
    def test_create_school_fail(self):
        """
        Test create school [UNAUTHORIZED]
        return 401 status code
        """
        url = reverse("school-list")
        response = self.client.post(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_create_school_success(self):
        """
        Test create school
        return 201 status code
        """
        self.client.force_authenticate(user=self.user)

        url = reverse("school-list")
        school ={"title":"Test3", "city":1}
        response = self.client.post(url, data=json.dumps(school), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual("Test3", response.data.get("title"))
        
    def test_update_school_fail(self):
        """
        Test update school [UNAUTHORIZED]
        return 401 status code
        """
        url = reverse("school-detail", kwargs={'pk': 1})
        response = self.client.put(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_update_school_success(self):
        """
        Test update city
        return 200 status code
        """
        self.client.force_authenticate(user=self.user)

        url = reverse("country-detail", kwargs={'pk': 1})
        data = {"title": "Test4", "city":1}
        old_country = School.objects.filter(id=1).first()
        _old = SchoolSerializer(old_country).data
        self.assertEqual("Test", _old.get("title"))
        
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual("Test4", response.data.get("title"))
        
        
    def test_delete_city_fail(self):
        """
        Test delete city [UNAUTHORIZED]
        return 401 status code
        """
        url = reverse("school-detail", kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        
    def test_delete_city_success(self):
        """
        Test delete city
        return 200 status code
        """
        self.client.force_authenticate(user=self.user)
        old_count = School.objects.all().count()
        self.assertEqual(2, old_count)
        url = reverse("school-detail", kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        new_count = School.objects.all().count()
        self.assertEqual(1, new_count)
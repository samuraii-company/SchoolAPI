from rest_framework.test import APITestCase, APIClient
from main.serializer import CountrySerializer
from rest_framework.exceptions import ErrorDetail
from django.urls import reverse
from rest_framework import status
from oauth.models import User
from oauth.serializer import RegisterSerializer
import json
from rest_framework import serializers


class AuthTestCase(APITestCase):
    
    def setUp(self):
        self.register_data = {
            "email": "test222@gmail.com",
            "password": "supersecretpasswordever1222213",
            "password2": "supersecretpasswordever1222213",
        }
        
        self.register_data_didnt_match = {
            "email": "test222@gmail.com",
            "password": "supersecretpasswordever1222213",
            "password2": "supersecretpasswordever1222212",
        }
        
        self.register_data_too_short = {
            "email": "test222@gmail.com",
            "password": "12223",
            "password2": "12223",
        }
        
        self.login_data = {
            "email": "test222@gmail.com",
            "password": "supersecretpasswordever1222213",
        }
        
        self.login_data_bad = {
            "email": "test222@gmail.com",
            "password": "1112121213313124141241241",
        }
    
    def test_create_account(self):
        """
        Test Create new account
        """
        users_count = User.objects.all().count()
        self.assertEqual(users_count, 0)
        url = reverse("register")
        request = self.client.post(url, data=json.dumps(self.register_data), content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, request.status_code)
        users_count = User.objects.all().count()
        self.assertEqual(users_count, 1)
        
    def test_create_account_didnt_match(self):
        """
        Test Create new account failed
        Password fields didn't match.
        """
        url = reverse("register")
        request = self.client.post(url, data=json.dumps(self.register_data_didnt_match), content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)
        
    def test_create_account_too_short(self):
        """
        Test Create new account failed
        password is too short. It must contain at least 8 characters.
        """
        url = reverse("register")
        request = self.client.post(url, data=json.dumps(self.register_data_too_short), content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    def test_login_success(self):
        """
        Test login
        return: access token
        return: refresh_token
        """
        url = reverse("register")
        request = self.client.post(url, data=json.dumps(self.register_data), content_type='application/json')
        url = reverse("token_obtain_pair")
        request = self.client.post(url, data=json.dumps(self.login_data), content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, request.status_code)
        
    def test_login_failed(self):
        """
        Test login failed
        """
        url = reverse("register")
        request = self.client.post(url, data=json.dumps(self.register_data), content_type='application/json')
        url = reverse("token_obtain_pair")
        request = self.client.post(url, data=json.dumps(self.login_data_bad), content_type='application/json')
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, request.status_code)
        self.assertEqual("No active account found with the given credentials", request.data["detail"])
        
    def test_refresh_token(self):
        """
        Test Refresh Token
        """
        url = reverse("register") 
        request = self.client.post(url, data=json.dumps(self.register_data), content_type='application/json')
        url = reverse("token_obtain_pair")
        request = self.client.post(url, data=json.dumps(self.login_data), content_type='application/json')
        token_access = request.data.get("access")
        token_refresh = request.data.get("refresh")
        url = reverse("token_refresh") 
        refresh_request = self.client.post(url, data=json.dumps({"refresh": token_refresh}), content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, refresh_request.status_code)
        new_token = refresh_request.data.get("access")
        self.assertNotEqual(token_access, new_token)
        

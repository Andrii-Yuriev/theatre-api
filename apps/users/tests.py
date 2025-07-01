from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

USER_CREATE_URL = "/api/auth/users/"


class UserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a new user is successful"""
        payload = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
        }
        response = self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(pk=response.data["id"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_create_user_with_existing_username(self):
        """Test error is raised for existing username"""
        get_user_model().objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword123",
        )
        payload = {
            "email": "test2@example.com",
            "username": "testuser",
            "password": "testpassword456",
        }
        response = self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# @Author: Lam
# @Date:   29/05/2020 20:59


from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status  # Easier to understand http codes
# Test api Client for making api requests
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Test the users API (Public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_OK(self):
        """Test for creating a valid user and its successful"""
        payload = {
            'email': 'test@google.com',
            'password': 'testpass',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Creating a user that already exists (fails)"""

        payload = {
            'email': 'test@google.com',
            'password': 'testpass',
            'name': 'Test Name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pass_too_short(self):
        """Test that the password is >5 characters"""

        payload = {
            'email': 'test@google.com',
            'password': 'testp',
            'name': 'Test Name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Testing a token is created for user"""

        payload = {
            'email': 'test@example.com',
            'password': 'test12345',
        }

        # Create a User to test against (using the function we have)
        create_user(**payload)

        # Make request with POST to create it
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test to check that token is not created if invalid credentials are given"""

        create_user(
            email='test.example.com',
            password='test12123',
        )
        payload = {
            'email': 'test@example.com',
            'password': 'wrong',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that if user doesnt exists === token is not created"""

        payload = {
            'email': 'test@example.com',
            'password': 'test12345',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_missing_fields(self):
        """Test that email & password are required"""

        res = self.client.post(TOKEN_URL, {'email': 'notAnEmail', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

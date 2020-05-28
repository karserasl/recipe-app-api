# @Author: Administrator
# @Date:   28/05/2020 23:35


from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        """Test for new user with an email is OK"""
        email = 'testemail@gmail.com'
        password = 'testpassword'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test if the email for the new user is normalized."""
        email = 'testemail@EXAMPLE.COM'
        user = get_user_model().objects.create_user(email, 'test123456')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test for creating user with empty email raise error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123456')

    def test_create_new_superuser(self):
        """Test for creating superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123456'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

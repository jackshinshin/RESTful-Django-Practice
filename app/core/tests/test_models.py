from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_create_user_with_email_successfull(self):
        # Test creating a new user with successful email notice
        email = "curryisalegend@gmail.com"
        password = '123456'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        # because password is encrypted, it can only be checked in this way
        self.assertTrue(user.check_password(password))
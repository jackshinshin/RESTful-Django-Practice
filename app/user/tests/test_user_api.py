from distutils.sysconfig import customize_compiler
import inspect
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.management.base import BaseCommand

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

# Helper function that can be used for different tests
def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserAPITests(TestCase):
    # Test the user API
    def setUp(self) -> None:
        self.cmd = BaseCommand()
        self.client = APIClient()

    def test_create_valid_user_success(self):
        # Test creating user with valid payload is successful
        self.cmd.stdout.write(f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        payload = {
            'email' : 'test@gmail.com',
            'password' : 'test',
            'name': 'Test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # Ensuring password is not passed to the user for security purposes
        self.assertNotIn('password', res.data)
        
        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))
        
    def test_user_exists(self):
        # Test creating a user that already exists fails
        self.cmd.stdout.write(f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        payload = {
            'email' : 'test@gmail.com',
            'password' : 'test'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
       
        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

    def test_password_too_short(self):
        # Test that the password must be more than 5 characters
        self.cmd.stdout.write(f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        payload = {
            'email' : 'test@gmail.com', 
            'password' : 'sh'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)
        
        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))
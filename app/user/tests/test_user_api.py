import inspect
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.management.base import BaseCommand


from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
CURRENT_USER_URL = reverse('user:currentuser')

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
        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        payload = {
            'email': 'test@gmail.com',
            'password': 'test123',
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
        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        payload = {
            'email': 'test@gmail.com',
            'password': 'test123',
            'name': 'test'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

    def test_password_too_short(self):
        # Test that the password must be more than 5 characters
        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        payload = {
            'email': 'test@gmail.com',
            'password': 'sh',
            'name': 'test'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

    def test_create_token_for_user(self):
        # Test that a token is created for the user
        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        user_info = {
            'name': 'Test',
            'email': 'test@gmail.com',
            'password': 'test123'
        }
        create_user(**user_info)
        
        payload = {
            'email': user_info['email'],
            'password': user_info['password']
        }
        
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

    def test_create_token_invalid_credentials(self):
        # Test that token is not created if invalid credentials are given

        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        create_user(email='test@gmail.com', password='testpass')
        payload = {
            'email': 'test@gmail.com',
            'password': 'wrong'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

    def test_create_token_no_user(self):
        # Test that token is not created if user doesn't exist
        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

    def test_create_token_missing_field(self):
        # Test that email and password are required
        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

    def test_retrieve_user_unauth(self):
        # Test that authtication is required for users

        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        res = self.client.get(CURRENT_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))


class PrivateUserAPITest(TestCase):
    # Authentication is required before making requests to the api

    def setUp(self) -> None:
        self.user = create_user(
            email='test@gmail.com',
            password='test1233',
            name='Test'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.cmd = BaseCommand()

    def test_retrieve_profile_success(self):
        # Test retrieving profile for logged in users
        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        res = self.client.get(CURRENT_USER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

    def test_post_me_not_allowed(self):
        # Test that POST is not allowed on the me url

        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        res = self.client.post(CURRENT_USER_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

    def test_update_user_profile(self):
        # Test updating th euser profile for authenticated user

        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        payload = {
            'name': 'newone',
            'password': 'anotherpassword'
        }

        res = self.client.patch(CURRENT_USER_URL, payload)

        # Update the user from the latest data in the database after sending the patch request
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

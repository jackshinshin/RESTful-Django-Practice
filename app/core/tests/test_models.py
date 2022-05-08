from multiprocessing.sharedctypes import Value
from django.test import TestCase
from django.contrib.auth import get_user_model
import inspect
from django.core.management.base import BaseCommand
class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        cmd = BaseCommand()
        cmd.stdout.write(f'--------Test {cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')
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
        
        cmd.stdout.write(cmd.style.SUCCESS('OK!'))
        
    def test_normalize_email(self):
        cmd = BaseCommand()
        cmd.stdout.write(f'--------Test {cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')
        email = "fsadnomif@FASGFASDFAD"
        user = get_user_model().objects.create_user(
            email,
            'randomcharacters'
        )
        self.assertEqual(user.email, email.lower())
        
        cmd.stdout.write(cmd.style.SUCCESS('OK!'))

    def test_new_user_invalid_email(self):
        cmd = BaseCommand()
        cmd.stdout.write(f'--------Test {cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "tasdfds")
            
        cmd.stdout.write(cmd.style.SUCCESS('OK!'))
        
    def test_create_superuser(self):
        cmd = BaseCommand()
        cmd.stdout.write(f'--------Test {cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )
        # is_superuser is included in the permissionmixin
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
        cmd.stdout.write(cmd.style.SUCCESS('OK!'))
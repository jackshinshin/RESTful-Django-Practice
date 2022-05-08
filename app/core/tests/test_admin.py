import inspect
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.management.base import BaseCommand
class AdminSiteTests(TestCase):
    # Create a setup function that runs before any tests do

    def setUp(self):
        self.cmd = BaseCommand()
        # accessible to the class
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@gmail.com',
            password = '123456'
        )
        # force_login makes it easier to test without having to manually log in to django admin page
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@gmail.com',
            password = '123456',
            name = 'Test'
        )
        # Default django admin requires a username to create a user
        # But we seeks to provide only emails, so a few changes have to be made in the admin.py file
    def test_users_listed(self):
        # Test that users are listed on user page
        
        self.cmd.stdout.write(f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))
        
    def test_user_change_page(self):
        # Test that the user edit page works
        
        self.cmd.stdout.write(f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')
        
        # admin/core/user/1
        url = reverse('admin:core_user_change', args = [self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!')) 

    def test_create_user_page(self):
        # Test that the create user page works
        self.cmd.stdout.write(f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        
        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

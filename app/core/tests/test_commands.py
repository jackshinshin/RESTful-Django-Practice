from unittest.mock import patch
# allow commands to be called
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
from django.core.management.base import BaseCommand
import inspect


class CommandTests(TestCase):
    def setUp(self) -> None:
        self.cmd = BaseCommand()

    def test_wait_for_db_ready(self):
        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')
        # Test waiting for db when db is available
        with patch('django.db.utils.ConnectionHandler.__getitem__') as getitem:
            getitem.return_value = True
            # In django convention, the call_command function search for custom commands in the directory call "management/commands"
            call_command('wait_for_db')
            self.assertEqual(getitem.call_count, 1)
        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

    # The decorator avoids called sleep function (in the tested command) to reduce waiting time
    # When using patch as a decorator, an argument is needed
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, required_arg):

        self.cmd.stdout.write(
            f'--------Test {self.cmd.style.WARNING(inspect.currentframe().f_code.co_name)} begins--------')
        # Test waiting for db
        with patch('django.db.utils.ConnectionHandler.__getitem__') as getitem:
            getitem.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(getitem.call_count, 6)

        self.cmd.stdout.write(self.cmd.style.SUCCESS('OK!'))

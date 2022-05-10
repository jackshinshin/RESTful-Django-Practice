import time

# Import conneciton moodules
from django.db import connections
from django.db.utils import OperationalError
# Used to create custom command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # Django command to pause execution until database is available

    def handle(self, *args, **options):

        self.stdout.write('Waiting for database....')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(
                    'Database is unavailabe, waiting for 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))

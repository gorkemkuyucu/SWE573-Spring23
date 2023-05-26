"""
To solve the bug app is starting before the db
"""
import time
from psycopg2 import OperationalError as OperationalError2
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Checking whether DB is up')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (OperationalError, OperationalError2):
                self.stdout.write('Waiting DB to start')
                time.sleep(2)
        
        self.stdout.write(self.style.SUCCESS('DB is up!'))
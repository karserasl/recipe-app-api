# @Author: Administrator
# @Date:   29/05/2020 19:19


import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause execution until DB is ready and available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for DB...')
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('DB unavailable, waiting for 1 sec...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database Available!'))

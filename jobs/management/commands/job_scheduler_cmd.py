import time
from django.core.management.base import BaseCommand
from jobs import job_scheduler


class Command(BaseCommand):
    help = 'Create initial data for Management App scheduler'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Start scheduler'))
        job_scheduler.start_scheduler()
        time.sleep(0.5)
        self.stdout.write(self.style.SUCCESS('Finish scheduler'))

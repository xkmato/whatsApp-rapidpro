from django.core.management import BaseCommand
from whatapp.app.stack import YowsupEchoStack

__author__ = 'kenneth'


class Command(BaseCommand):
    def handle(self, *args, **options):
        y = YowsupEchoStack()
        y.start()

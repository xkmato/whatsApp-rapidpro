from django.core.management import BaseCommand
from whatapp.app.stack import YowsupEchoStack
from whatapp.exceptions import WhatsAppError

__author__ = 'kenneth'


class Command(BaseCommand):
    def handle(self, *args, **options):
        def go():
            try:
                y = YowsupEchoStack()
                y.start()
            except WhatsAppError:
                go()

        go()

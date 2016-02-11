from datetime import datetime
import logging
from django.core.management import BaseCommand
from whatapp.app.models import Message
from whatapp.app.send_stack import YowsupSendStack
from whatapp.exceptions import WhatsAppError

__author__ = 'kenneth'

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        messages = Message.objects.filter(direction=Message.OUTGOING, status=Message.QUEUED).order_by('created_on')[:6]

        # somebody already handled these messages, move on
        if not messages:
            print "No more messages"
            return

        for message in messages:
            try:
                print "[%s] Processing message %s" % (str(datetime.now()), message.text)
                msg = [(message.urn, message.text)]
                y = YowsupSendStack(msg)
                y.start()
            except KeyboardInterrupt:
                message.status = Message.SENT
                message.save()
                print "Message sent to %s" % message.urn
                continue
            except Exception as e:
                message.status = Message.SENT
                message.save()
                print "Message message to %s failed: %s" % (message.urn, str(e))

from django.conf import settings
from django.db import models
import requests
from whatapp.exceptions import WhatsAppError

__author__ = 'kenneth'


class Message(models.Model):
    INCOMING = 'I'
    OUTGOING = 'O'

    QUEUED = 'Q'
    SENT = 'S'

    text = models.TextField()
    urn = models.CharField(max_length=40)
    direction = models.CharField(choices=(('Incoming', INCOMING), ('Outgoing', OUTGOING)), max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=(('Queued', QUEUED), ('Sent', SENT)), default=QUEUED, max_length=1)
    rapidpro_id = models.CharField(max_length=40, blank=True, null=True)

    def __unicode__(self):
        d = "to" if self.direction == Message.OUTGOING else "from"
        return "%s --> %s" % (d, self.urn)

    def notify_rapidpro_received(self):
        if self.direction != Message.INCOMING:
            raise WhatsAppError("Trying to send in an outgoing message")

        r = requests.post(settings.RAPIDPRO_NOTIFY_RECEIVED, data={"from": self.urn, 'text': self.text})
        if 199 < r.status_code > 399:
            print "Message %s from %s not sent" % (str(self.pk), self.urn)
        else:
            self.status = Message.SENT
            self.save()

    def notify_rapidpro_sent(self):
        if self.direction != Message.OUTGOING:
            return
        requests.post(settings.RAPIDPRO_NOTIFY_SENT, data={'id': self.rapidpro_id})

    @classmethod
    def receive(cls, msg, fro):
        return cls.objects.create(text=msg, urn=fro, direction=Message.INCOMING)

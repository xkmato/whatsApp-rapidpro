from datetime import datetime
from whatapp.app.models import Message
from whatapp.app.send_stack import YowsupSendStack

__author__ = 'kenneth'


def send_message_out(message):
    print "[%s] Processing message %s" % (str(datetime.now()), message.text)
    msg = [(message.urn, message.text)]
    y = YowsupSendStack(msg)
    y.start()
    message.status = Message.SENT
    message.save()

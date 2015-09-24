import logging
from whatapp.app import tasks
from whatapp.app.models import Message
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
__author__ = 'kenneth'

logger = logging.getLogger(__name__)


class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        print("Received %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
        m = Message.receive(messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False))
        tasks.push_to_rapidpro.delay([m])

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Received image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            m = Message.receive(messageProtocolEntity.url, messageProtocolEntity.getFrom(False))
            tasks.push_to_rapidpro.delay([m])

        elif messageProtocolEntity.getMediaType() == "location":
            print("Received location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))
            m = Message.receive("(%s, %s)" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude()), messageProtocolEntity.getFrom(False))
            tasks.push_to_rapidpro.delay([m])

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Received vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
            m = Message.receive("(%s, %s)" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData()), messageProtocolEntity.getFrom(False))
            tasks.push_to_rapidpro.delay([m])

        else:
            print("Received unsupported message")

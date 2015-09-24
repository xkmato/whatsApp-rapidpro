from whatapp.app.models import Message

__author__ = 'kenneth'


from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
import threading
import logging
logger = logging.getLogger(__name__)

class SendLayer(YowInterfaceLayer):

    #This message is going to be replaced by the @param message in YowsupSendStack construction
    #i.e. list of (jid, message) tuples
    PROP_MESSAGES = "org.openwhatsapp.yowsup.prop.sendclient.queue"


    def __init__(self):
        super(SendLayer, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()

    #call back function when there is a successful connection to whatsapp server
    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        self.lock.acquire()
        for target in self.getProp(self.__class__.PROP_MESSAGES, []):
            #getProp() is trying to retreive the list of (jid, message) tuples, if none exist, use the default []
            phone, message = target
            if '@' in phone:
                messageEntity = TextMessageProtocolEntity(message, to = phone)
            elif '-' in phone:
                messageEntity = TextMessageProtocolEntity(message, to = "%s@g.us" % phone)
            else:
                messageEntity = TextMessageProtocolEntity(message, to = "%s@s.whatsapp.net" % phone)
            #append the id of message to ackQueue list
            #which the id of message will be deleted when ack is received.
            self.ackQueue.append(messageEntity.getId())
            self.toLower(messageEntity)
        self.lock.release()

    #after receiving the message from the target number, target number will send a ack to sender(us)
    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        self.lock.acquire()
        #if the id match the id in ackQueue, then pop the id of the message out
        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))

        if not len(self.ackQueue):
            self.lock.release()
            logger.info("Message sent")
            raise KeyboardInterrupt()
        self.lock.release()

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback


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
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
        Message.receive(messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False))

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            Message.receive(messageProtocolEntity.url, messageProtocolEntity.getFrom(False))

        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))
            Message.receive("(%s, %s)" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude()), messageProtocolEntity.getFrom(False))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
            Message.receive("(%s, %s)" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData()), messageProtocolEntity.getFrom(False))
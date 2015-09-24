from django.conf import settings
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer, YowCryptLayer, AuthError
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.logger import YowLoggerLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.stanzaregulator import YowStanzaRegulator
from yowsup.stacks import YowStack
from whatapp.app.send_layer import SendLayer

__author__ = 'kenneth'


class YowsupSendStack(object):
    def __init__(self, messages, encryption_enabled=True):
        """
        :param credentials:
        :param messages: list of (jid, message) tuples
        :param encryptionEnabled:
        :return:
        """

        if encryption_enabled:
            from yowsup.layers.axolotl import YowAxolotlLayer
            layers = (
                SendLayer,
                (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer),
                YowAxolotlLayer,
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )
        else:
            layers = (
                SendLayer,
                (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer),
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )

        self.stack = YowStack(layers)
        self.stack.setProp(SendLayer.PROP_MESSAGES, messages)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self.stack.setCredentials(settings.CREDENTIALS)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
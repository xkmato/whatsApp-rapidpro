from django.conf import settings
from yowsup.layers.protocol_calls import YowCallsProtocolLayer
from yowsup.layers.protocol_iq import YowIqProtocolLayer
from yowsup.layers.protocol_media import YowMediaProtocolLayer
from yowsup.stacks import YowStack
from .layer import EchoLayer
from yowsup.layers import YowLayerEvent, YowParallelLayer
from yowsup.layers.auth import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers.stanzaregulator import YowStanzaRegulator
from yowsup.layers.protocol_receipts import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.logger import YowLoggerLayer


__author__ = 'kenneth'


class YowsupEchoStack(object):
    def __init__(self, encryption_enabled=True):
        if encryption_enabled:
            from yowsup.layers.axolotl import YowAxolotlLayer
            layers = (
                EchoLayer,
                YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowMediaProtocolLayer, YowIqProtocolLayer, YowCallsProtocolLayer]),
                YowAxolotlLayer,
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )
        else:
            layers = (
                EchoLayer,
                YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowMediaProtocolLayer, YowIqProtocolLayer, YowCallsProtocolLayer]),
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )

        self.stack = YowStack(layers)
        self.stack.setCredentials(settings.CREDENTIALS)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop(timeout=120)
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
        except Exception as e:
            print ("Another Error: %s" % str(e))

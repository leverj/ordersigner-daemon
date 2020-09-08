from collections import namedtuple as named_tuple
from json import dumps, loads
from operator import itemgetter as item_getter

from leverj_ordersigner import futures, spot
from twisted.internet import address, protocol
from twisted.protocols import basic

Order = named_tuple('Order', ('type', 'order', 'instrument', 'signer'))


class OrderSigner:
    """
    Provides an object-oriented facade for the leverj_ordersigner lib.
    """

    TYPE_FUTURES = 'futures'
    TYPE_SPOT = 'spot'

    def sign(self, order: Order) -> str:
        """
        Returns the correct signature for the provided order object.
        """
        if order.type == self.TYPE_FUTURES:
            return self.sign_futures(
                order.order,
                order.instrument,
                order.signer,
            )
        elif order.type == self.TYPE_SPOT:
            return self.sign_spot(
                order.order,
                order.instrument,
                order.signer,
            )

    def sign_futures(self, order: dict, instrument: dict, signer: str) -> str:
        return futures.sign_order(order, instrument, signer)

    def sign_spot(self, order: dict, instrument: dict, signer: str) -> str:
        return spot.sign_order(order, instrument, signer)


class SigningProtocol(basic.LineReceiver):
    """
    Processes individual requests received by the server.
    """

    def __init__(self, order_signer: OrderSigner) -> None:
        self.order_signer = order_signer

    def lineReceived(self, line: bytes) -> None:
        order = Order(
            *item_getter('type', 'order', 'instrument', 'signer')(loads(line))
        )

        try:
            signature = self.order_signer.sign(order)
        except Exception as e:
            result = {
                'ok': False,
                'error': {
                    'type': type(e).__name__,
                    'message': str(e),
                    'context': getattr(e, 'context', {}),
                },
            }
        else:
            result = {
                'ok': True,
                'signature': signature,
            }

        self.transport.write(dumps(result).encode('utf-8') + self.delimiter)

    def rawDataReceived(self, data):
        raise RuntimeError(f'Raw data not supported (received {data!r})')


class SigningProtocolFactory(protocol.Factory):
    """
    Constructs a new protocol instance for each new client connection.
    """
    protocol = SigningProtocol

    def buildProtocol(self, addr: address.UNIXAddress) -> SigningProtocol:
        p = self.protocol(OrderSigner())
        p.factory = self
        return p

from collections import namedtuple as named_tuple
from json import dumps, loads
from operator import itemgetter as item_getter

from leverj_ordersigner import futures, spot
from twisted.internet import address, protocol
from twisted.protocols import basic

Order = named_tuple('Order', ('order', 'instrument', 'signer'))


class OrderSigner:
    """
    Provides an object-oriented facade for the leverj_ordersigner lib.
    """

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
            *item_getter('order', 'instrument', 'signer')(loads(line))
        )

        self.transport.write(dumps({
            'ok': True,
            'signature': self.order_signer.sign_spot(*order),
        }).encode('utf-8') + self.delimiter)

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

from json import dumps
from unittest import TestCase

from twisted.internet import address, testing

from ordersigner_daemon import SigningProtocol, SigningProtocolFactory
from ordersigner_daemon.testing import MockOrderSigner


class SigningProtocolTest(TestCase):
    def setUp(self) -> None:
        factory = SigningProtocolFactory()

        self.order_signer = MockOrderSigner()

        self.protocol: SigningProtocol = \
            factory.buildProtocol(address.UNIXAddress(b'test'))
        self.protocol.order_signer = self.order_signer

        self.transport = testing.StringTransport()

        self.protocol.makeConnection(self.transport)

    def test_futures_success(self) -> None:
        """
        Client sends a valid futures transaction for signing.
        """
        self.order_signer.futures_sig = '0xb4dc0de'

        self.protocol.dataReceived(dumps({
            # Stripping out all but the bare essentials to keep test readable.
            # See tests for ``leverj_ordersigner`` project for real-world
            # example of a valid future order.
            'type': 'futures',
            'instrument': {},
            'order': {},
            'signer': '0x1337',
        }).encode('utf-8') + self.protocol.delimiter)

        self.assertEqual(self.transport.value(), dumps({
            'ok': True,
            'signature': self.order_signer.futures_sig,
        }).encode('utf-8') + self.protocol.delimiter)

    def test_spot_success(self) -> None:
        """
        Client sends a valid spot transaction for signing.
        """
        self.order_signer.spot_sig = '0xb4dc0de'

        self.protocol.dataReceived(dumps({
            # Stripping out all but the bare essentials to keep test readable.
            # See tests for ``leverj_ordersigner`` project for real-world
            # example of a valid spot order.
            'type': 'spot',
            'instrument': {},
            'order': {},
            'signer': '0x1337',
        }).encode('utf-8') + self.protocol.delimiter)

        self.assertEqual(self.transport.value(), dumps({
            'ok': True,
            'signature': self.order_signer.spot_sig,
        }).encode('utf-8') + self.protocol.delimiter)

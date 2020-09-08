from json import dumps
from unittest import TestCase

from ordersigner_daemon.testing import MockOrderSigner
from twisted.internet import address, testing

from ordersigner_daemon import SigningProtocol, SigningProtocolFactory


class SigningProtocolTest(TestCase):
    def setUp(self) -> None:
        factory = SigningProtocolFactory()

        self.order_signer = MockOrderSigner()

        self.protocol: SigningProtocol = \
            factory.buildProtocol(address.UNIXAddress(b'test'))
        self.protocol.order_signer = self.order_signer

        self.transport = testing.StringTransport()

        self.protocol.makeConnection(self.transport)

    def test_happy_path(self) -> None:
        """
        Client sends a valid transaction for signing.
        """
        self.order_signer.spot_sig = '0xb4dc0de'

        self.protocol.dataReceived(dumps({
            'instrument': {
                'symbol': 'LEVETH',
                'quote': {
                    'address': '0x0000000000000000000000000000000000000000',
                    'decimals': 18
                },
                'base': {
                    'address': '0x167cdb1aC9979A6a694B368ED3D2bF9259Fa8282',
                    'decimals': 9
                }
            },
            'order': {
                'accountId': '0x167cdb1aC9979A6a694B368ED3D2bF9259Fa8282',
                'side': 'buy',
                'quantity': 12.3343,
                'price': 23.44322,
                'orderType': 'LMT',
                'instrument': 'LEVETH',
                'timestamp': 12382173200872,
                'expiryTime': 1238217320021122,
            },
            'signer': '0xb98ea45b6515cbd6a5c39108612b2cd5ae184d5eb0d72b21389a1fe6db01fe0d',
        }).encode('utf-8') + self.protocol.delimiter)

        self.assertEqual(self.transport.value(), dumps({
            'ok': True,
            'signature': self.order_signer.spot_sig,
        }).encode('utf-8') + self.protocol.delimiter)

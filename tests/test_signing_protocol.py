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
            'type': 'futures',
            'instrument': {
                'id': '1',
                'symbol': 'BTCDAI',
                'name': 'BTC/DAI',
                'status': 'active',
                'tickSize': 1,
                'quoteSignificantDigits': 0,
                'baseSignificantDigits': 4,
                'baseSymbol': 'BTC',
                'quoteSymbol': 'DAI',
                'maxLeverage': 100,
                'topic': 'index_BTCUSD',
                'quote': {
                    'name': 'DAI',
                    'address': '0xb0F776EB352738CF25710d92Fca2f4A5e2c24D3e',
                    'symbol': 'DAI',
                    'decimals': 18
                }
            },
            'order': {
                'accountId': '0xc21b183A8050D1988117B86408655ff974d021A0',
                'originator': '0x10758C328A02B511d2a7B8f55459929Fa760411f',
                'instrument': '1',
                'price': 9380,
                'quantity': 1,
                'marginPerFraction': '191428571428571430000',
                'side': 'buy',
                'orderType': 'SLM',
                'timestamp': 1595560081494041,
                'quote': '0xb0F776EB352738CF25710d92Fca2f4A5e2c24D3e',
                'isPostOnly': False,
                'reduceOnly': False,
                'clientOrderId': 1,
                'triggerPrice': 9385
            },
            'signer': '0xae9edfad7fa29b0d6e14b045b5e74f3360e041545cf64236e81e616849072d65',
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
            'type': 'spot',
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

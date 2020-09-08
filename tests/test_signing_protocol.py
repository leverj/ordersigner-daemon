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

    def _send(self, payload: dict) -> None:
        """
        Simulates sending a payload to the server.
        """
        self.protocol.dataReceived(
            dumps(payload).encode('utf-8') + self.protocol.delimiter,
        )

    def _expect(self, payload: dict) -> None:
        """
        Asserts that the server sent back the correct response.
        """
        self.assertEqual(
            self.transport.value(),
            dumps(payload).encode('utf-8') + self.protocol.delimiter,
        )

    def test_futures_success(self) -> None:
        """
        Client sends a valid futures transaction for signing.
        """
        self.order_signer.futures_sig = '0xb4dc0de'

        self._send({
            # Stripping out all but the bare essentials to keep test readable.
            # See tests for ``leverj_ordersigner`` project for real-world
            # example of a valid future order.
            'type': 'futures',
            'instrument': {},
            'order': {},
            'signer': '0x1337',
        })

        self._expect({
            'ok': True,
            'signature': self.order_signer.futures_sig,
        })

    def test_spot_success(self) -> None:
        """
        Client sends a valid spot transaction for signing.
        """
        self.order_signer.spot_sig = '0xb4dc0de'

        self._send({
            # Stripping out all but the bare essentials to keep test readable.
            # See tests for ``leverj_ordersigner`` project for real-world
            # example of a valid spot order.
            'type': 'spot',
            'instrument': {},
            'order': {},
            'signer': '0x1337',
        })

        self._expect({
            'ok': True,
            'signature': self.order_signer.spot_sig,
        })

    def test_signing_error(self) -> None:
        """
        An error occurs while attempting to generate the signature.
        """
        error = ValueError('The private key must be exactly 32 bytes long.')
        error.context = {'actual': '0x0'}
        self.order_signer.spot_sig = error

        self._send({
            'type': 'spot',
            'instrument': {},
            'order': {},
            'signer': '0x1337',
        })

        self._expect({
            'ok': False,
            'error': {
                'type': 'ValueError',
                'message': str(error),
                'context': error.context
            },
        })

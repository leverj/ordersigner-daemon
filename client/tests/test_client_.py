# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from twisted.internet import testing
from twisted.python import failure
from twisted.trial import unittest
from ujson import dumps

from leverj_ordersigner_client import ErrorResponse, OrderSignerClient, \
    UnprocessableResponse


class ClientTest(unittest.TestCase):
    def setUp(self):
        self.transport = testing.StringTransport()

        self.client = OrderSignerClient()
        self.client.makeConnection(self.transport)

    def test_futures_happy_path(self):
        """
        Sending a valid futures transaction for signing.
        """
        d = self.client.sign_futures(
            # Stripping out all but the bare essentials to keep test readable.
            # See tests for ``leverj_ordersigner`` project for real-world
            # example of a valid future order.
            instrument={'symbol': 'LEVETH'},
            order={'side': 'buy'},
            signer='0x1337',
        )

        # Check that correct request was sent by client.
        self.assertEqual(
            self.transport.value(),

            dumps({
                'type': self.client.TYPE_FUTURES,
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
                'signer': '0x1337',
            }).encode('utf-8') + self.client.delimiter,
        )

        # Simulate response from daemon.
        expected = '0xb4dc0de'
        self.client.lineReceived(dumps({
            'ok': True,
            'signature': expected,
        }).encode('utf-8'))

        d.addCallback(self.assertEqual, expected)
        return d

    def test_spot_happy_path(self):
        """
        Sending a valid spot transaction for signing.
        """
        d = self.client.sign_spot(
            # Stripping out all but the bare essentials to keep test readable.
            # See tests for ``leverj_ordersigner`` project for real-world
            # example of a valid future order.
            instrument={'symbol': 'LEVETH'},
            order={'side': 'buy'},
            signer='0x1337',
        )

        # Check that correct request was sent by client.
        self.assertEqual(
            self.transport.value(),

            dumps({
                'type': self.client.TYPE_SPOT,
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
                'signer': '0x1337',
            }).encode('utf-8') + self.client.delimiter,
        )

        # Simulate response from daemon.
        expected = '0xb4dc0de'
        self.client.lineReceived(dumps({
            'ok': True,
            'signature': expected,
        }).encode('utf-8'))

        d.addCallback(self.assertEqual, expected)
        return d

    def test_error_response(self):
        """
        The daemon sends back a non-success response.
        """
        d = self.client.sign_futures(
            instrument={'symbol': 'LEVETH'},
            order={'side': 'buy'},
            signer='0x0',
        )


        # Simulate response from daemon.
        expected = {
            'type': 'ValueError',
            'message': 'The private key must be exactly 32 bytes long.',
            'context': {'actual': 0x0},
        }

        self.client.lineReceived(dumps({
            'ok': False,
            'error': expected,
        }).encode('utf-8'))

        def checkFailure(f):
            # type: (failure.Failure) -> None
            self.assertIsInstance(f.value, ErrorResponse)
            self.assertEqual(f.value.type, expected['type'])
            self.assertEqual(f.value.message, expected['message'])
            self.assertEqual(f.value.context, expected['context'])

        d.addErrback(checkFailure)
        return d

    def test_unprocessable_response(self):
        """
        For some reason, the daemon sent back something that doesn't conform
        to the protocol.
        """
        d = self.client.sign_futures(
            instrument={'symbol': 'LEVETH'},
            order={'side': 'buy'},
            signer='0x0',
        )

        # Simulate strange response from daemon.
        raw_payload = dumps({
            'message': 'Hello, world!',
        }).encode('utf-8')

        self.client.lineReceived(raw_payload)

        def checkFailure(f):
            # type: (failure.Failure) -> None
            self.assertIsInstance(f.value, UnprocessableResponse)
            self.assertEqual(f.value.line, raw_payload)

        d.addErrback(checkFailure)
        return d

    def test_non_json_response(self):
        """
        Delving even further into the bizarre, the server sends back something
        that isn't even JSON.
        """
        d = self.client.sign_futures(
            instrument={'symbol': 'LEVETH'},
            order={'side': 'buy'},
            signer='0x0',
        )

        # Simulate even stranger response from daemon.
        raw_payload = b'Hello, world!'

        self.client.lineReceived(raw_payload)

        def checkFailure(f):
            # type: (failure.Failure) -> None
            self.assertIsInstance(f.value, UnprocessableResponse)
            self.assertEqual(f.value.line, raw_payload)

        d.addErrback(checkFailure)
        return d

from unittest import TestCase

import filters as f
from filters.test import BaseFilterTestCase
from twisted.internet import address, testing
from ujson import dumps, loads

from ordersigner_daemon import Order
from ordersigner_daemon.protocol import SigningProtocol, SigningProtocolFactory
from ordersigner_daemon.testing import MockOrderSigner
from ordersigner_daemon.validation import OrderSignerRequest


class SigningProtocolTest(TestCase):
    def setUp(self) -> None:
        factory = SigningProtocolFactory()

        self.order_signer = MockOrderSigner()

        self.protocol: SigningProtocol = \
            factory.buildProtocol(address.UNIXAddress(b'test'))
        self.protocol.order_signer = self.order_signer
        self.protocol.print_exceptions = False

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
            loads(self.transport.value()),
            payload,
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
            'instrument': {'symbol': 'LEVETH'},
            'order': {'side': 'buy'},
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
            'instrument': {'symbol': 'LEVETH'},
            'order': {'side': 'buy'},
            'signer': '0x1337',
        })

        self._expect({
            'ok': True,
            'signature': self.order_signer.spot_sig,
        })

    def test_validation_error(self) -> None:
        """
        The input does not pass validation.
        """
        self._send({
            'type': 'spot',
            # Something's not quite right here...
            'instrument': None,
            'order': {'side': 'buy'},
            'signer': '0x1337',
        })

        self._expect({
            'ok': False,
            'error': {
                'type': ValueError.__name__,
                'message': SigningProtocol.MSG_VALIDATION_FAILED,
                'context': {
                    'instrument': [{
                        'code': f.Required.CODE_EMPTY,
                        'message': f.Required.templates[f.Required.CODE_EMPTY],
                    }]
                }
            }
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
            'instrument': {'symbol': 'LEVETH'},
            'order': {'side': 'buy'},
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


class InputValidationTest(BaseFilterTestCase):
    filter_type = OrderSignerRequest

    def test_pass_happy_path(self) -> None:
        """
        Valid request is valid.
        """
        order = {
            # Stripping out all but the bare essentials to keep test readable.
            # See tests for ``leverj_ordersigner`` project for real-world
            # example of a valid future order.
            'type': 'futures',
            'instrument': {'symbol': 'LEVETH'},
            'order': {'side': 'buy'},
            'signer': '0x1337',
        }

        self.assertFilterPasses(
            dumps(order),
            Order(**order),
        )

    def test_fail_empty(self) -> None:
        """
        Request is empty bytes.
        """
        self.assertFilterErrors(
            '',
            [f.Required.CODE_EMPTY],
        )

    def test_fail_not_json(self) -> None:
        """
        Request is not valid JSON.
        """
        self.assertFilterErrors(
            '{',
            [f.JsonDecode.CODE_INVALID],
        )

    def test_fail_not_dict(self) -> None:
        """
        Request is valid JSON, but not a dict.
        """
        self.assertFilterErrors(
            dumps(['futures', {}, {}, '0x1337']),
            [f.Type.CODE_WRONG_TYPE],
        )

    def test_fail_type_missing(self) -> None:
        """
        Request is missing ``type``.
        """
        self.assertFilterErrors(
            dumps({
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
                'signer': '0x1337',
            }),
            {'type': [f.FilterMapper.CODE_MISSING_KEY]},
        )

    def test_fail_type_none(self) -> None:
        """
        ``type`` is null.
        """
        self.assertFilterErrors(
            dumps({
                'type': None,
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
                'signer': '0x1337',
            }),

            {'type': [f.Required.CODE_EMPTY]},
        )

    def test_fail_type_wrong_type(self) -> None:
        """
        ``type`` value is not a string.
        """
        self.assertFilterErrors(
            dumps({
                'type': ['futures', 'spot'],
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
                'signer': '0x1337',
            }),

            {'type': [f.Type.CODE_WRONG_TYPE]},
        )

    def test_fail_type_not_valid_choice(self) -> None:
        """
        ``type`` value is not a valid choice.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'foo',
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
                'signer': '0x1337',
            }),

            {'type': [f.Choice.CODE_INVALID]},
        )

    def test_fail_instrument_missing(self) -> None:
        """
        Request is missing ``instrument``.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'spot',
                'order': {'side': 'buy'},
                'signer': '0x1337',
            }),

            {'instrument': [f.FilterMapper.CODE_MISSING_KEY]},
        )

    def test_fail_instrument_none(self) -> None:
        """
        ``instrument`` is null.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'spot',
                'instrument': None,
                'order': {'side': 'buy'},
                'signer': '0x1337',
            }),

            {'instrument': [f.Required.CODE_EMPTY]},
        )

    def test_fail_instrument_wrong_type(self) -> None:
        """
        ``instrument`` value is not a dict.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'spot',
                'instrument': True,
                'order': {'side': 'buy'},
                'signer': '0x1337',
            }),

            {'instrument': [f.Type.CODE_WRONG_TYPE]},
        )

    def test_fail_order_missing(self) -> None:
        """
        Request is missing ``order``.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'spot',
                'instrument': {'symbol': 'LEVETH'},
                'signer': '0x1337',
            }),

            {'order': [f.FilterMapper.CODE_MISSING_KEY]},
        )

    def test_fail_order_none(self) -> None:
        """
        ``order`` is null.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'spot',
                'instrument': {'symbol': 'LEVETH'},
                'order': None,
                'signer': '0x1337',
            }),

            {'order': [f.Required.CODE_EMPTY]},
        )

    def test_fail_order_wrong_type(self) -> None:
        """
        ``order`` value is not a dict.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'spot',
                'instrument': {'symbol': 'LEVETH'},
                'order': True,
                'signer': '0x1337',
            }),

            {'order': [f.Type.CODE_WRONG_TYPE]},
        )

    def test_fail_signer_missing(self) -> None:
        """
        Request is missing ``signer``.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'spot',
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
            }),

            {'signer': [f.FilterMapper.CODE_MISSING_KEY]},
        )

    def test_fail_signer_none(self) -> None:
        """
        ``signer`` is null.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'spot',
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
                'signer': None,
            }),

            {'signer': [f.Required.CODE_EMPTY]},
        )

    def test_fail_signer_wrong_type(self) -> None:
        """
        ``signer`` value is not a string.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'spot',
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
                'signer': True,
            }),

            {'signer': [f.Type.CODE_WRONG_TYPE]},
        )

    def test_fail_signer_empty(self) -> None:
        """
        ``signer`` value is a string, but it's empty.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'spot',
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
                'signer': '',
            }),

            {'signer': [f.Required.CODE_EMPTY]},
        )

    def test_fail_extra_key(self) -> None:
        """
        Request contains an unexpected key.
        """
        self.assertFilterErrors(
            dumps({
                'type': 'futures',
                'instrument': {'symbol': 'LEVETH'},
                'order': {'side': 'buy'},
                'signer': '0x1337',
                'foo': 'bar',
            }),

            {'foo': [f.FilterMapper.CODE_EXTRA_KEY]},
        )

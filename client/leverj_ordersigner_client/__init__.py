# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from collections import deque

from twisted.internet import base, defer, endpoints, reactor
from twisted.protocols import basic
from ujson import dumps, loads

__all__ = [
    'async_create_client',
    'ErrorResponse',
    'NonSuccessResponse',
    'OrderSignerClient',
    'UnprocessableResponse',
]

DEFAULT_INTERFACE = 'unix:/tmp/leverj-ordersigner-daemon.sock'


def async_create_client(use_reactor=reactor, interface=DEFAULT_INTERFACE):
    # type: (base.ReactorBase, str) -> defer.Deferred
    """
    Asynchronously creates a new client instance and establishes a connection
    to the daemon.

    Note that this function returns a :py:cls:`defer.Deferred` instance, so
    you'll need to attach a callback to send requests once the connection is
    established.

    .. important::
        The client will not connect to the daemon until you start the reactor.

    Refer to the project ``README`` for more information and examples.

    :param use_reactor: The reactor (event loop) to use.  Unless you are trying
    to accomplish something very specific, you can probably keep the default
    value.

    :param interface: Interface to connect to.  This should match the interface
    that you specified when starting the daemon.

    :return: A deferred that will resolve with the :py:cls:`OrderSignerClient`
    instance.
    """
    client = endpoints.clientFromString(use_reactor, interface)

    return endpoints.connectProtocol(client, OrderSignerClient())


class NonSuccessResponse(ValueError):
    """
    Base class that indicates that the client received a non-success response
    from the daemon.
    """


class ErrorResponse(NonSuccessResponse):
    """
    Indicates that the client received an error response from the daemon.
    """

    # noinspection PyShadowingBuiltins
    def __init__(self, type, message, context):
        # type: (str, str, dict) -> None
        super(ErrorResponse, self).__init__(
            'Daemon sent {type}: {message}'.format(
                type=type,
                message=message,
            )
        )

        self.type = type
        self.message = message
        self.context = context


class UnprocessableResponse(NonSuccessResponse):
    """
    Indicates that the client received a response that does not conform to the
    protocol (e.g., not valid JSON, has unexpected structure, etc.).

    This can happen if, for example, the client accidentally connected to the
    wrong unix socket (e.g., it got back a message from a very confused
    Postgres server).
    """

    def __init__(self, line):
        # type: (bytes) -> None
        super(UnprocessableResponse, self).__init__(
            'Daemon sent unprocessable response: {line!r}'.format(line=line)
        )

        self.line = line


# :kludge: Twisted's BaseProtocol class is an old-style class in Python 2, so
# we have to add ``object`` base explicitly.
# https://stackoverflow.com/a/18392639
class OrderSignerClient(basic.LineOnlyReceiver, object):
    """
    Interface for requesting transaction signatures from the OrderSigner
    daemon.
    """
    TYPE_FUTURES = 'futures'
    TYPE_SPOT = 'spot'

    def __init__(self):
        super(OrderSignerClient, self).__init__()

        self._queue = deque()

    def sign_futures(self, order, instrument, signer):
        # type: (dict, dict, str) -> defer.Deferred
        """
        Sends a request to sign a futures order.
        """
        return self._send({
            'type': self.TYPE_FUTURES,
            'instrument': instrument,
            'order': order,
            'signer': signer,
        })

    def sign_spot(self, order, instrument, signer):
        # type: (dict, dict, str) -> defer.Deferred
        """
        Sends a request to sign a spot order.
        """
        return self._send({
            'type': self.TYPE_SPOT,
            'instrument': instrument,
            'order': order,
            'signer': signer,
        })

    def lineReceived(self, line):
        # type: (bytes) -> None
        """
        Called when the daemon sends a response back to the client.
        """
        d = self._queue.popleft()  # type: defer.Deferred

        try:
            decoded = loads(line.decode('utf-8'))  # type: dict
        except ValueError:
            d.errback(UnprocessableResponse(line))
        else:
            if decoded.get('ok', False):
                d.callback(decoded['signature'])
            else:
                try:
                    error = ErrorResponse(**decoded['error'])
                except KeyError:
                    error = UnprocessableResponse(line)

                d.errback(error)

    def _send(self, payload):
        # type: (dict) -> defer.Deferred
        """
        Sends a request to the daemon.
        """
        d = defer.Deferred()

        # We are reusing the same transport instance (i.e., open connection)
        # for every request, so we can safely assume that the daemon will
        # respond to requests in the same order that we make them.
        self._queue.append(d)

        self.sendLine(dumps(payload).encode('utf-8'))
        return d

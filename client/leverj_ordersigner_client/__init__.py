# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from collections import deque

from twisted.internet import defer
from twisted.protocols import basic
from ujson import dumps, loads


class OrderSignerClient(basic.LineOnlyReceiver):
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
            'order': order,
            'instrument': instrument,
            'signer': signer,
        })

    def sign_spot(self, order, instrument, signer):
        # type: (dict, dict, str) -> defer.Deferred
        """
        Sends a request to sign a spot order.
        """
        return self._send({
            'type': self.TYPE_SPOT,
            'order': order,
            'instrument': instrument,
            'signer': signer,
        })

    def lineReceived(self, line):
        # type: (bytes) -> None
        """
        Called when the daemon sends a response back to the client.
        """
        d = self._queue.popleft()  # type: defer.Deferred
        d.callback(loads(line.decode('utf-8')))

    def _send(self, payload):
        # type: (dict) -> defer.Deferred
        """
        Sends a request to the daemon.
        """
        d = defer.Deferred()
        self._queue.append(d)
        self.sendLine(dumps(payload).encode('utf-8'))
        return d

from traceback import print_exc

import filters as f
from twisted.internet import address, protocol
from twisted.protocols import basic
from ujson import dumps

from ordersigner_daemon import OrderSigner
from ordersigner_daemon.validation import OrderSignerRequest

__all__ = [
    'SigningProtocol',
    'SigningProtocolFactory',
]

# Cache an instance of the filter in the module, so that we don't have to
# re-initialise it every time a new request is received.
request_filter = OrderSignerRequest()


class SigningProtocol(basic.LineOnlyReceiver):
    """
    Processes individual requests received by the server.
    """

    MSG_VALIDATION_FAILED = 'Invalid input; see context for more info.'

    def __init__(self, order_signer: OrderSigner) -> None:
        self.order_signer = order_signer
        self.print_exceptions = True

    def lineReceived(self, line: bytes) -> None:
        filter_runner = f.FilterRunner(request_filter, line)

        if filter_runner.is_valid():
            try:
                signature = self.order_signer.sign(filter_runner.cleaned_data)
            except Exception as e:
                if self.print_exceptions:
                    print_exc()

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
        else:
            result = {
                'ok': False,
                'error': {
                    'type': ValueError.__name__,
                    'message': self.MSG_VALIDATION_FAILED,
                    'context': filter_runner.get_errors(),
                },
            }

        self.sendLine(dumps(result).encode('utf-8'))


class SigningProtocolFactory(protocol.Factory):
    """
    Constructs a new protocol instance for each new client connection.
    """
    protocol = SigningProtocol

    def buildProtocol(self, addr: address.UNIXAddress) -> SigningProtocol:
        p = self.protocol(OrderSigner())
        p.factory = self
        return p

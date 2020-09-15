"""
Example script showing how to send a request to the daemon to sign a spot
order.

In order for this script to run, you will need to start a daemon process.
Refer to the documentation in the ``leverj-ordersigner-daemon`` project for
more information.
"""
from sys import stderr

from twisted.internet import defer, reactor
from twisted.python import failure

from leverj_ordersigner_client import OrderSignerClient, async_create_client


def main():
    # Create a client instance and connect to the daemon.
    # Note that this function returns a :py:cls:`defer.Deferred` instance, as
    # the connection is established asynchronously.
    d = async_create_client(reactor)  # type: defer.Deferred

    # Attach a callback that will be executed when the client successfully
    # establishes a connection to the daemon.
    d.addCallback(clientConnected)

    # Attach an errback that will be executed if the client is unable to
    # establish a connection (e.g., if the daemon isn't running).
    d.addErrback(clientConnectionFailure)

    # Start the reactor.
    # Note that this will block on the current thread until ``reactor.stop()``
    # is called (e.g., in a callback/errback).
    reactor.run()

    # Any code that occurs after ``reactor.run()`` will NOT be executed until
    # ``reactor.stop()`` gets called.
    print('All done!')


def clientConnected(client):
    # type: (OrderSignerClient) -> None
    """
    Runs when the client successfully establishes a connection to the daemon.
    """

    # Call the client's ``sign_spot()`` method to request a signature for a
    # spot order (use ``sign_futures()`` for futures orders).
    #
    # Note that these methods return :py:cls:`defer.Deferred` instances, so you
    # will need to attach callback functions to process the resulting
    # signatures.
    d = client.sign_spot(
        instrument={
            'symbol': 'LEVETH',
            'quote': {
                'address': '0x0000000000000000000000000000000000000000',
                'decimals': 18,
            },
            'base': {
                'address': '0x167cdb1aC9979A6a694B368ED3D2bF9259Fa8282',
                'decimals': 9,
            }
        },

        order={
            'accountId': '0x167cdb1aC9979A6a694B368ED3D2bF9259Fa8282',
            'side': 'buy',
            'quantity': 12.3343,
            'price': 23.44322,
            'orderType': 'LMT',
            'instrument': 'LEVETH',
            'timestamp': 12382173200872,
            'expiryTime': 1238217320021122,
        },

        signer='0xb98ea45b6515cbd6a5c39108612b2cd5ae184d5eb0d72b21389a1fe6db01fe0d',
    )  # type: defer.Deferred

    # Attach a callback to the :py:cls:`defer.Deferred` instance to handle the
    # signature returned by the daemon.
    def responseReceived(signature):
        # type: (str) -> None
        """
        Executed when the client successfully receives a signature from the
        daemon.

        :param signature: The signature in 0x format.
        """
        assert signature == '0xaad62800f307299a33dae10908c559bd7cd4658a3803e6b587e0f5bf95a052c17783324ec07b629c30e3a41eb20b4ace2787304c50a00b5cdcbd6bc22dbbded11b'
        print('Signature verified!', signature)

        # Drop the connection to the daemon.
        # Note that the client can send as many requests as it wants before
        # closing the connection.
        client.transport.loseConnection()

        # Stop the reactor and
        reactor.stop()

    d.addCallback(responseReceived)

    # Attach an errback to the :py:cls:`defer.Deferred` instance to handle any
    # error that prevented a successful signing.
    def requestFailed(failure_):
        # type: (failure.Failure) -> None
        """
        Executed if something goes wrong while parsing a response from the
        daemon (e.g., the daemon sent back an error response to indicate that
        something was wrong with the request inputs).

        :param failure_: Contains details about the exception that caused the
        failure.
        """
        failure_.printTraceback(stderr)

    d.addErrback(requestFailed)


def clientConnectionFailure(failure_):
    # type: (failure.Failure) -> None
    """
    Executed if the client is unable to establish a connection to the daemon.

    :param failure_: Contains details about the exception that caused the
    failure.
    """
    try:
        reactor.stop()
    finally:
        failure_.printTraceback(stderr)


if __name__ == '__main__':
    main()

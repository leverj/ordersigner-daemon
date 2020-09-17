from sys import stderr

from codetiming import Timer
from leverj_ordersigner_client import OrderSignerClient, async_create_client
from tqdm import tqdm
from twisted.internet import reactor

from resources import instruments, orders, signer


def main():
    d = async_create_client(reactor)
    d.addCallback(client_connected)
    d.addErrback(client_connection_failure)
    reactor.run()


def client_connected(client):
    # type: (OrderSignerClient) -> None
    """
    Runs when the client successfully establishes a connection to the daemon.
    """
    progress = tqdm(orders)

    def response_received(actual, expected):
        progress.update()
        if progress.n >= progress.total:
            progress.close()
            reactor.stop()
            t.stop()

        assert actual == expected

    def request_failed(failure_):
        failure_.printTraceback(stderr)
        reactor.stop()

    t = Timer()
    t.start()
    for order in orders:
        d = client.sign_spot(
            order,
            instruments[order['instrument']],
            signer,
        )

        d.addCallback(
            response_received,
            expected=order['signature'],
        )
        d.addErrback(request_failed)


def client_connection_failure(failure_):
    try:
        reactor.stop()
    finally:
        failure_.printTraceback(stderr)


if __name__ == '__main__':
    main()

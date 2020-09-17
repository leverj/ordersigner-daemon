"""
Defines the ``leverj-ordersigner`` as a subcommand for ``twistd``.

Note that this module must (magically) contain ``Options`` and ``makeService``.

For more info about how this plugin gets installed into ``twistd``, see the
``/daemon/twisted/plugins`` directory (relative to the top level of this
project).
"""

from twisted.application import internet, service
from twisted.internet import endpoints, reactor
from twisted.python import usage

from ordersigner_daemon.protocol import SigningProtocolFactory

name = 'leverj-ordersigner'

class Options(usage.Options):
    optParameters = [
        ['interface', 'i', 'unix:/tmp/leverj-ordersigner-daemon.sock', 'Interface to listen for client connections (see docs for twisted.internet.endpoints.serverFromString)'],
    ]


def makeService(options):
    service_ = internet.StreamServerEndpointService(
        endpoints.serverFromString(
            reactor,
            options['interface'],
        ),
        SigningProtocolFactory(),
    )

    service_.setServiceParent(service.Application(name))

    return service_

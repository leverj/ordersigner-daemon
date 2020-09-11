# Configures the application for ``twistd``.
# See ``README.rst`` for more information.
from twisted.application import internet, service
from twisted.internet import endpoints, reactor

from ordersigner_daemon.protocol import SigningProtocolFactory

application = service.Application('leverj-ordersigner-daemon')

service = internet.StreamServerEndpointService(
    endpoints.serverFromString(
        reactor,
        'unix:/tmp/leverj-ordersigner-daemon.sock',
    ),
    SigningProtocolFactory(),
)
service.setServiceParent(application)

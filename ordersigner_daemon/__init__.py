from json import dumps

from twisted.internet import protocol


class SigningProtocol(protocol.Protocol):
    def dataReceived(self, data: bytes) -> None:
        self.transport.write(dumps({
            'ok': True,
            'signature': '0xaad62800f307299a33dae10908c559bd7cd4658a3803e6b587e0f5bf95a052c17783324ec07b629c30e3a41eb20b4ace2787304c50a00b5cdcbd6bc22dbbded11b',
        }).encode('utf-8'))


class SigningProtocolFactory(protocol.Factory):
    protocol = SigningProtocol

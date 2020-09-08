import typing
from ordersigner_daemon import OrderSigner


class MockOrderSigner(OrderSigner):
    """
    Mock interface for the ``leverj_ordersigner`` lib, used for testing.

    Set an instance's ``futures_sig`` and/or ``spot_sig`` attribute to specify
    the signature (``str``) that should be returned from the corresponding
    ``sign_*`` method.

    To simulate an exception being raised during the signing process, set the
    attribute to an ``Exception`` instance.

    Examples:
    >>> order_signer = MockOrderSigner()
    >>> order_signer.spot_sig = '0xb4dc0de'
    >>> assert order_signer.sign_spot({}, {}, '') == '0xb4dc0de'

    >>> order_signer = MockOrderSigner()
    >>> order_signer.spot_sig = RuntimeError('Simulating an error')
    >>> try:
    >>>     order_signer.sign_spot({}, {}, '')
    >>> except RuntimeError as e:
    >>>     assert str(e) == 'Simulating an error'
    """
    def __init__(self):
        super().__init__()

        self.futures_sig: typing.Optional[typing.Union[str, Exception]] = None
        self.spot_sig: typing.Optional[typing.Union[str, Exception]] = None

    def sign_futures(self, order: dict, instrument: dict, signer: str) -> str:
        if isinstance(self.futures_sig, Exception):
            raise self.futures_sig

        return self.futures_sig

    def sign_spot(self, order: dict, instrument: dict, signer: str) -> str:
        if isinstance(self.spot_sig, Exception):
            raise self.spot_sig

        return self.spot_sig

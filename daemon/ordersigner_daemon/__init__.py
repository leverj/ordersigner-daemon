from collections import namedtuple as named_tuple

from leverj_ordersigner import futures, spot

__all__ = [
    'Order',
    'OrderSigner',
]

Order = named_tuple('Order', ('type', 'order', 'instrument', 'signer'))


class OrderSigner:
    """
    Provides an object-oriented facade for the leverj_ordersigner lib.
    """

    TYPE_FUTURES = 'futures'
    TYPE_SPOT = 'spot'

    def sign(self, order: Order) -> str:
        """
        Returns the correct signature for the provided order object.
        """
        if order.type == self.TYPE_FUTURES:
            return self.sign_futures(
                order.order,
                order.instrument,
                order.signer,
            )
        elif order.type == self.TYPE_SPOT:
            return self.sign_spot(
                order.order,
                order.instrument,
                order.signer,
            )

    def sign_futures(self, order: dict, instrument: dict, signer: str) -> str:
        return futures.sign_order(order, instrument, signer)

    def sign_spot(self, order: dict, instrument: dict, signer: str) -> str:
        return spot.sign_order(order, instrument, signer)

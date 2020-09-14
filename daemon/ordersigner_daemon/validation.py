import filters as f
from ujson import loads

from ordersigner_daemon import Order, OrderSigner


# noinspection PyUnusedLocal
def loads_shim(value, *args, **kwargs):
    """
    Compat shim so that we can use ultimate json with ``JsonDecode`` filter
    (which attempts to call ``loads`` with ``object_pairs_hook=OrderedDict``
    for compatibility with Python 3.5).
    """
    return loads(value)


class OrderSignerRequest(f.BaseFilter):
    """
    Validates an incoming request for the OrderSigner.
    """

    def _apply(self, value: bytes) -> Order:
        parsed = self._filter(
            value,
            f.Unicode | f.Required | f.JsonDecode(loads_shim) | f.FilterMapper(
                {
                    'instrument': f.Type(dict) | f.Required,
                    'order': f.Type(dict) | f.Required,
                    'signer': f.Type(str) | f.Required,

                    'type': f.Type(str) | f.Required | f.Choice({
                        OrderSigner.TYPE_FUTURES,
                        OrderSigner.TYPE_SPOT,
                    }),
                },

                allow_missing_keys=False,
                allow_extra_keys=False,
            ),
        )

        if self._has_errors:
            return None

        return Order(**parsed)

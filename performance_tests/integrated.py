"""
Tests the performance of signing transactions directly in the app via the
``leverj-ordersigner`` lib.

.. note::
    The daemon does **not** need to be running during this test.
"""
from codetiming import Timer
from leverj_ordersigner import spot
from tqdm import tqdm

from resources import instruments, orders, signer

def main():
    with Timer():
        for order in tqdm(orders):
            result = spot.sign_order(
                order=order,
                order_instrument=instruments[order['instrument']],
                signer=signer,
            )

            assert result == order['signature']

if __name__ == '__main__':
    main()

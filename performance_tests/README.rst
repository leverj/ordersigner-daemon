Leverj OrderSigner Daemon Performance Tests
===========================================
These tests compare the performance of using the client-daemon setup vs. integrating the ``leverj-ordersigner`` library directly into an application.

There are two tests:

1. ``integrated.py``
    Shows performance of an application signing transactions in the same process, instead of using the daemon.

2. ``daemon.py``
    Shows performance of an application interfacing with the daemon in an asynchronous manner.

Running Tests
-------------
It is recommended that you run the tests in a separate virtualenv, as a few additional dependencies are required.

Install the additional dependencies via pip:

.. code-block:: bash

    pip install -r requirements.txt

The tests can be run using Python 3.8 or later (earlier versions might work but are unsupported).

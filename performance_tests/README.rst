Leverj OrderSigner Daemon Performance Tests
===========================================
These tests compare the performance of using the client-daemon setup vs. integrating the ``leverj-ordersigner`` library directly into an application.

There are three tests:

1. ``integrated.py``
    Shows performance of an application signing transactions in the same process, instead of using the daemon.

2. ``daemon_single_thread.py``
    Shows performance of an application interfacing with the daemon in a single thread.

3. ``daemon_multi_threaded.py``
    Shows performance of an application interfacing with the daemon using multiple threads.

Running Tests
-------------
It is recommended that you run the tests in a separate virtualenv, as a few additional dependencies are required.

Install the additional dependencies

The daemon tests can run in Python 2 or Python 3, however the integrated test will only run in Python 3.

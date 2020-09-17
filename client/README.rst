Leverj OrderSigner Client
=========================
The client provides a way for applications to interface with the Leverj OrderSigner Daemon.

Setup
-----
You will need Python 3.8 or later to install the client (earlier versions may work but are unsupported).  Python 2.7 is also supported but not recommended, as `Python 2 reached its end of life on January 1st, 2020`_.

To install the library into your `virtualenv`_:

.. code-block:: bash

    pip install leverj-ordersigner-client

Usage
-----
See `examples/sign_spot.py <./examples/sign_spot.py>`_ for an example showing how to use the client to request a signature for an order.

The client uses `Twisted`_ under the hood, so there are a few things you'll need to keep in mind:

* The client sends requests asynchronously, so you'll need to get comfortable using `Deferreds`_ to handle the results from calling the client (the example script linked above shows how to do this).
* The client can only operate while Twisted's `Reactor`_ is running.  The code will need to call ``reactor.run()`` in order to execute client requests.
    .. note::
        ``reactor.run()`` blocks until ``reactor.stop()`` is called (e.g., in a callback or errback).  You will need to consider whether it is OK to block until all client requests are handled, or if the code should run the reactor in a separate thread.

Development
-----------
If you are working on the ``leverj-ordersigner-client`` project locally, you will need to install additional dependencies (only has to be done once):

.. code-block:: bash

    pip install -e '.[dev]'

Documentation
^^^^^^^^^^^^^
This project uses `Sphinx`_ as its docs builder.  To build documentation files, run the following command:

.. code-block:: bash

    make html -C docs

Unit Tests
^^^^^^^^^^
To execute unit tests in the current virtualenv, run the following command:

.. code-block:: bash

    trial tests

In addition, you can use `Tox`_ to run unit tests in each supported version of Python:

.. code-block:: bash

    tox

.. _Deferreds: https://twistedmatrix.com/documents/current/core/howto/defer.html
.. _Python 2 reached its end of life on January 1st, 2020: https://pip.pypa.io/en/latest/development/release-process/#python-2-support
.. _Reactor: https://twistedmatrix.com/documents/current/core/howto/reactor-basics.html
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _Tox: https://tox.readthedocs.io/en/latest/
.. _Twisted: https://twistedmatrix.com/documents/current/core/howto/clients.html
.. _virtualenv: https://virtualenv.pypa.io/en/stable/

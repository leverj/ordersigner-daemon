Leverj OrderSigner Daemon
=========================
The daemon provides an interface for generating transaction signatures.  Notably, `Web3.py`_ is only compatible with Python 3, so this provides a means by which clients written in Python 2.7 can take advantage of the transaction signing functionality without having to be rewritten in Python 3.

Setup
-----
You will need Python 3.8 or later to run the daemon (earlier versions may work but are unsupported).

To install the library into your `virtualenv`_:

.. code-block:: bash

    pip install leverj-ordersigner-daemon

Running the Daemon
------------------
This project uses `Twisted`_ for event-driven networking functionality.  To run the daemon, use the `twistd`_ executable:

.. code-block:: bash

    twistd leverj-ordersigner

``twistd`` will create the following files when it runs:

* ``twistd.log``: process logs.
* ``twistd.pid``: contains the process ID of the daemon process.  You can use
  this to terminate the daemon like so:

  .. code-block:: bash

    kill `cat twistd.pid`

.. tip::
    Call ``twistd -n leverj-ordersigner`` to run the daemon process in the foreground.

Interacting with the Daemon
^^^^^^^^^^^^^^^^^^^^^^^^^^^
The daemon listens for new requests via a `Unix Domain Socket`_ located at
``/tmp/leverj-ordersigner-daemon.sock`` (can be seen in the output from the
daemon when it starts up)::

    > twistd -n leverj-ordersigner
    2020-09-17T17:02:44+1200 [twisted.scripts._twistd_unix.UnixAppLogger#info] twistd 20.3.0 (/bin/python 3.8.5) starting up.
    2020-09-17T17:02:44+1200 [twisted.scripts._twistd_unix.UnixAppLogger#info] reactor class: twisted.internet.selectreactor.SelectReactor.
    2020-09-17T17:02:44+1200 [-] SigningProtocolFactory starting on '/tmp/leverj-ordersigner-daemon.sock'
    2020-09-17T17:02:44+1200 [ordersigner_daemon.protocol.SigningProtocolFactory#info] Starting factory <ordersigner_daemon.protocol.SigningProtocolFactory object at 0x10fcaca30>

To interact with the daemon manually, you can use ``netcat``::

    > nc -U /tmp/leverj-ordersigner-daemon.sock

Send a serialised order in JSON format, terminated with ``\r\n`` (e.g., press :kbd:`Ctrl+V`, then :kbd:`Return` — this should appear as ``^M`` in the terminal).  You will receive a JSON response with the corresponding transaction signature::

    nc -U /tmp/leverj-ordersigner-daemon.sock
    {"type": "spot", "instrument": {"symbol": "LEVETH", "quote": {"address": "0x0000000000000000000000000000000000000000", "decimals": 18}, "base": {"address": "0x167cdb1aC9979A6a694B368ED3D2bF9259Fa8282", "decimals": 9}}, "order": {"accountId": "0x167cdb1aC9979A6a694B368ED3D2bF9259Fa8282", "side": "buy", "quantity": 12.3343, "price": 23.44322, "orderType": "LMT", "instrument": "LEVETH", "timestamp": 12382173200872, "expiryTime": 1238217320021122}, "signer": "0xb98ea45b6515cbd6a5c39108612b2cd5ae184d5eb0d72b21389a1fe6db01fe0d"}
    ^M
    {"ok": true, "signature": "0xaad62800f307299a33dae10908c559bd7cd4658a3803e6b587e0f5bf95a052c17783324ec07b629c30e3a41eb20b4ace2787304c50a00b5cdcbd6bc22dbbded11b"}


.. important::
    Ensure that you escape all non-ASCII content and/or that your terminal uses UTF-8 encoding.

Note that, due to the way Unix Domain Sockets work, the daemon **can** handle connections from multiple clients simultaneously.  For more information, see `How do Unix Domain Sockets differentiate between multiple clients?`_

.. tip::
    You can specify an alternative interface (e.g., TCP) like this:

    .. code-block:: bash

        twistd leverj-ordersigner -i tcp:12345:interface=127.0.0.1

    The above will start a daemon listening for TCP connections on localhost port 12345.

    See documentation for ``twisted.internet.endpoints.serverFromString`` for all possible options (note that some interfaces might not work properly; this project was designed explicitly to support Unix Domain Sockets).

Development
-----------
If you are working on the ``leverj-ordersigner-daemon`` project locally, you will need to install additional dependencies (only has to be done once):

.. code-block:: bash

    pip install -e '.[dev]'

Documentation
^^^^^^^^^^^^^
This project uses `Sphinx`_ as its docs builder.  To build documentation files, run the following command:

.. code-block:: bash

    make html -C docs

Unit Tests
^^^^^^^^^^
This project uses `nose2`_ as its test runner.  To execute unit tests in the current virtualenv, run the following command:

.. code-block:: bash

    nose2

In addition, you can use `Tox`_ to run unit tests in each supported version of Python:

.. code-block:: bash

    tox

.. _How do Unix Domain Sockets differentiate between multiple clients?: https://stackoverflow.com/a/9644495/
.. _nose2: https://docs.nose2.io/en/latest/
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _Tox: https://tox.readthedocs.io/en/latest/
.. _twistd: https://twistedmatrix.com/documents/current/core/howto/basics.html#twistd
.. _Twisted: https://twistedmatrix.com/trac/
.. _Unix Domain Socket: https://en.wikipedia.org/wiki/Unix_domain_socket
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _Web3.py: https://web3py.readthedocs.io/en/stable/

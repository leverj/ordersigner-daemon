Leverj OrderSigner Client
=========================
The client provides a way for applications to interface with the Leverj OrderSigner Daemon.

Setup
-----
You will need Python 3.8 or later to install the client.  Python 2.7 is also supported but not recommended, as `Python 2 reached its end of life on January 1st, 2020`_.

To install the library into your `virtualenv`_:

.. code-block:: bash

    pip install leverj-ordersigner-client

Usage
-----
* TODO: How to import and invoke the client.
* TODO: Managing transport instances.

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

.. _Python 2 reached its end of life on January 1st, 2020: https://pip.pypa.io/en/latest/development/release-process/#python-2-support
.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _Tox: https://tox.readthedocs.io/en/latest/
.. _virtualenv: https://virtualenv.pypa.io/en/stable/

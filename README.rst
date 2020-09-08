Leverj OrderSigner Daemon
=========================
TODO: overview and background, links to documentation

Setup
-----
.. code-block:: bash

    pipenv install -e .
    pipenv shell

Running the Daemon
------------------
.. code-block:: bash

    twistd -y daemon.tac

.. note::
    Make sure you've run ``pipenv shell`` first.

``twistd`` will create the following files when it runs:

* ``twisted.log``: process logs.
* ``twisted.pid``: contains the process ID of the daemon process.  You can use
  this to terminate the daemon like so:

  .. code-block:: bash

    kill `cat twisted.pid`

.. tip::
    Call ``twistd -ny daemon.tac`` to run the daemon process in the foreground.

Documentation
-------------
.. code-block:: bash

    make html -C docs

.. note::
    Make sure you've run ``pipenv shell`` first.

Unit Tests
----------
.. code-block:: bash

    tox

.. note::
    Make sure you've run ``pipenv shell`` first.

Releases
--------
1. Synchronise ``Pipfile`` dependencies with ``setup.py``:
    .. code-block:: bash

        pipenv-setup sync --dev --pipfile

    .. note::
        Make sure you've run ``pipenv shell`` first.

2. Increment version string in ``setup.py``.

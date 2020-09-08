Leverj OrderSigner Daemon
=========================
TODO: overview and background, links to documentation

Setup
-----
.. code-block:: bash

    pipenv install -e .
    pipenv shell

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

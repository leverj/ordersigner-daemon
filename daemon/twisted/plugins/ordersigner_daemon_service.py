"""
Installs the ``leverj-ordersigner`` plugin for ``twistd``.

Obsolete documentation can be found at
https://twistedmatrix.com/documents/current/core/howto/tap.html

After a **lot** of trial and error, I eventually discovered the following:

1. Must be in a folder called ``twisted/plugins``.
2. Must **not** contain any ``__init__.py`` files.
3. Must be included in ``packages`` in ``setup.py`` (see that file in this
   project for more info).
"""

from twisted.application import service

# This **must** be named ``serviceMaker`` for ``twistd`` to register it
# properly.
serviceMaker = service.ServiceMaker(
    # Friendly name for the plugin.
    # I'm not sure what this is used for.
    name='Leverj OrderSigner Daemon',

    # Corresponding module that contains the plugin.
    module='ordersigner_daemon.twisted',

    # Friendly description for the plugin.
    # Displayed when the user runs ``twistd --help``.
    # IMPORTANT: This string gets eval'd during tab completion (e.g., make sure
    # it doesn't contain any backticks).
    description='Daemon for signing Leverj transactions via leverj-ordersigner-client.',

    # Subcommand that the user types after ``twistd`` to run the plugin (i.e.,
    # ``twistd leverj-ordersigner``).
    tapname='leverj-ordersigner',
)

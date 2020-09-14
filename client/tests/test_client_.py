# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

from unittest import TestCase

from twisted.internet import testing

from leverj_ordersigner_client import OrderSignerClient


class ClientTest(TestCase):
    def setUp(self):
        self.transport = testing.StringTransport()

        self.client = OrderSignerClient()
        self.client.makeConnection(self.transport)

    def test_futures_happy_path(self):
        """
        Sending a valid futures transaction for signing.
        """
        pass

    def test_spot_happy_path(self):
        """
        Sending a valid spot transaction for signing.
        """
        pass

    def test_error_response(self):
        """
        The daemon sends back a non-success response.
        """
        pass

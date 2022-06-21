from http import client
import unittest
from unittest import mock
from unittest.mock import patch, mock_open, Mock, MagicMock
import socket
from writer import Connect_fun
from Model.models import Item


class TestWriter(unittest.TestCase):
    def test_connect(self):
        self.assertRaises(OSError,Connect_fun,'122.0.0.1',10365)
       
    def test_connect_overflow(self):
        self.assertRaises(OverflowError,Connect_fun,'127.0.0.1',9999999)


if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch

from reader import *


class ReaderTest(unittest.TestCase):
    @patch('reader.PrikaziMeni', return_value=1)
    @patch('reader.UzmiInterval', return_value='2022-12-12 22:22:22')
    def test_uzmi_istorijske_vrednosti(self, input1, input2):
        self.assertEqual(('2022-12-12 22:22:22', '2022-12-12 22:22:22', CodeEnum.CODE_ANALOG),
                         UzmiIstorijeskeVrednsoti())

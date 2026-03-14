import unittest
import sys
import os
import io
from contextlib import redirect_stdout

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source.BCDALU import BCDALU


class TestBCDALU(unittest.TestCase):
    def setUp(self):
        self.alu = BCDALU()

    def test_conversion(self):
        with redirect_stdout(io.StringIO()):
            num = 1234
            bcd = self.alu.int_to_bcd_8421(num)
            restored = self.alu.from_bcd_8421(bcd)
            self.assertEqual(restored, num)

            with self.assertRaises(ValueError):
                self.alu.int_to_bcd_8421(123456789)

    def test_addition(self):
        with redirect_stdout(io.StringIO()):
            res = self.alu.add_bcd_8421(15, 20)
            self.assertEqual(self.alu.from_bcd_8421(res), 35)

            res = self.alu.add_bcd_8421(8, 5)
            self.assertEqual(self.alu.from_bcd_8421(res), 13)

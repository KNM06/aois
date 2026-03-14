import unittest
import sys
import os
import io
from contextlib import redirect_stdout

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source.IntegerALU import IntegerALU


class TestIntegerALU(unittest.TestCase):
    def setUp(self):
        self.alu = IntegerALU()

    def test_conversions(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.alu.to_direct_code(5)[-3:], [1, 0, 1])
            self.assertEqual(self.alu.to_direct_code(-5)[0], 1)
            self.assertEqual(self.alu.to_direct_code(-5)[-3:], [1, 0, 1])

            inv = self.alu.to_inverse_code(-5)
            self.assertEqual(inv[0], 1)
            self.assertEqual(inv[-1], 0)

            twos = self.alu.to_additional_code(-1)
            self.assertTrue(all(bit == 1 for bit in twos))

            self.assertEqual(
                self.alu.from_additional_code(self.alu.to_additional_code(123)), 123
            )
            self.assertEqual(
                self.alu.from_additional_code(self.alu.to_additional_code(-123)), -123
            )

    def test_add_sub(self):
        with redirect_stdout(io.StringIO()):
            res = self.alu.add_additional(10, 5)
            self.assertEqual(self.alu.from_additional_code(res), 15)
            res = self.alu.add_additional(10, -5)
            self.assertEqual(self.alu.from_additional_code(res), 5)

            res = self.alu.sub_additional(10, 5)
            self.assertEqual(self.alu.from_additional_code(res), 5)
            res = self.alu.sub_additional(5, 10)
            self.assertEqual(self.alu.from_additional_code(res), -5)

    def test_mul_div(self):
        with redirect_stdout(io.StringIO()):
            res = self.alu.mul_direct(6, 7)
            self.assertEqual(self.alu.from_additional_code(res), 42)
            res = self.alu.mul_direct(-6, 7)
            self.assertEqual(res, self.alu.to_direct_code(-42))

            res = self.alu.div_direct(20, 5)
            self.assertEqual(self.alu.decode_div(res), 4.0)

            res_frac = self.alu.div_direct(5, 2)
            self.assertEqual(self.alu.decode_div(res_frac), 2.5)

            with self.assertRaises(ZeroDivisionError):
                self.alu.div_direct(10, 0)

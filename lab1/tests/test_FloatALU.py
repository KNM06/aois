import unittest
import sys
import os
import io
from contextlib import redirect_stdout

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from source.FloatALU import FloatALU


class TestFloatALU(unittest.TestCase):
    def setUp(self):
        self.alu = FloatALU()

    def test_ieee754_conversion(self):
        with redirect_stdout(io.StringIO()):
            zero = self.alu.float_to_ieee754(0.0)
            self.assertEqual(sum(zero), 0)

            val = 12.5
            arr = self.alu.float_to_ieee754(val)
            restored = self.alu.from_ieee754(arr)
            self.assertEqual(restored, val)

            val = -12.5
            arr = self.alu.float_to_ieee754(val)
            restored = self.alu.from_ieee754(arr)
            self.assertEqual(restored, val)

    def test_add_sub(self):
        with redirect_stdout(io.StringIO()):
            arr1 = self.alu.float_to_ieee754(2.5)
            arr2 = self.alu.float_to_ieee754(1.5)

            res = self.alu.add_ieee754(arr1, arr2)
            self.assertEqual(self.alu.from_ieee754(res), 4.0)

            res = self.alu.sub_ieee754(arr1, arr2)
            self.assertEqual(self.alu.from_ieee754(res), 1.0)

            res = self.alu.sub_ieee754(arr1, arr1)
            self.assertEqual(self.alu.from_ieee754(res), 0.0)

    def test_mul_div(self):
        with redirect_stdout(io.StringIO()):
            arr1 = self.alu.float_to_ieee754(2.0)
            arr2 = self.alu.float_to_ieee754(3.0)
            zero = self.alu.float_to_ieee754(0.0)

            res = self.alu.mul_ieee754_pure(arr1, arr2)
            self.assertEqual(self.alu.from_ieee754(res), 6.0)

            res = self.alu.div_ieee754_pure(arr2, arr1)
            self.assertEqual(self.alu.from_ieee754(res), 1.5)

            res_mul_zero = self.alu.mul_ieee754_pure(arr1, zero)
            self.assertEqual(self.alu.from_ieee754(res_mul_zero), 0.0)

            with self.assertRaises(ZeroDivisionError):
                self.alu.div_ieee754_pure(arr1, zero)

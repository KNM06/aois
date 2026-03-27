import unittest
from source.BooleanMath import BooleanMath


class TestBooleanMath(unittest.TestCase):
    def test_math(self):
        m = BooleanMath(
            [((0, 0), 0), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)], ["a", "b"]
        )
        self.assertEqual(
            m.get_post_classes(),
            {"T0": True, "T1": True, "S": False, "M": True, "L": False},
        )
        self.assertEqual(m.get_zhegalkin_polynomial(), "ab")
        self.assertEqual(m.get_fictitious_variables(), [])
        self.assertIn(("a",), m.get_boolean_derivatives())

        m2 = BooleanMath([((0,), 1), ((1,), 0)], ["a"])
        self.assertEqual(
            m2.get_post_classes(),
            {"T0": False, "T1": False, "S": True, "M": False, "L": True},
        )
        self.assertEqual(m2.get_zhegalkin_polynomial(), "1 ^ a")

        m3 = BooleanMath(
            [((0, 0), 1), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)], ["a", "b"]
        )
        self.assertEqual(m3.get_fictitious_variables(), ["a", "b"])
        self.assertEqual(
            BooleanMath([((0,), 0), ((1,), 0)], ["a"]).get_zhegalkin_polynomial(), "0"
        )

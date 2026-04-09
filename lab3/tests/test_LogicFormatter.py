import unittest
from source.LogicFormatter import LogicFormatter


class TestLogicFormatter(unittest.TestCase):
    def test_formatter(self):
        f, v = LogicFormatter.format_term, ["a", "b", "c"]
        self.assertEqual(f([1, 0, "-"], v, True), "(a & !b)")
        self.assertEqual(f([1, 0, "-"], v, False), "(!a V b)")
        self.assertEqual(f([1, "-", "-"], v, True), "a")
        self.assertEqual(f(["-", "-", "-"], v, True), "")
        fe = LogicFormatter.format_expr
        self.assertEqual(fe([(1, 0), (0, 1)], ["a", "b"], True), "(!a & b) V (a & !b)")
        self.assertEqual(fe([(1, 0), (0, 1)], ["a", "b"], False), "(a V !b) & (!a V b)")
        self.assertIsNone(fe([], v, True))

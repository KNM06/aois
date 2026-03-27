import unittest
from source.LogicParser import LogicParser


class TestLogicParser(unittest.TestCase):
    def test_parser(self):
        t = LogicParser.tokenize("a v b -> !c & (d ~ e)")
        self.assertEqual(
            t, ["a", "|", "b", "->", "!", "c", "&", "(", "d", "~", "e", ")"]
        )
        LogicParser.validate(t)
        for err in ["a + b"]:
            self.assertRaises(ValueError, LogicParser.tokenize, err)
        for err in [
            [],
            ["1a"],
            ["_a"],
            [")", "("],
            ["a", "b"],
            ["(", "a", ")", "b"],
            ["a", "&", "&", "b"],
            ["(", "(", "a", ")"],
            ["&", "a"],
            ["a", "&"],
        ]:
            self.assertRaises(ValueError, LogicParser.validate, err)
        rpn = LogicParser.to_rpn(t)
        self.assertEqual(rpn, ["a", "b", "|", "c", "!", "d", "e", "~", "&", "->"])
        ev = lambda expr, val: LogicParser.evaluate_rpn(LogicParser.to_rpn(expr), val)
        self.assertEqual(ev(["a", "&", "b"], {"a": 1, "b": 1}), 1)
        self.assertEqual(ev(["a", "|", "b"], {"a": 0, "b": 0}), 0)
        self.assertEqual(ev(["a", "->", "b"], {"a": 1, "b": 0}), 0)
        self.assertEqual(ev(["a", "~", "b"], {"a": 1, "b": 1}), 1)
        self.assertEqual(ev(["!", "a"], {"a": 0}), 1)
        self.assertRaises(
            ValueError, LogicParser.evaluate_rpn, ["a", "b", "!"], {"a": 1, "b": 1}
        )

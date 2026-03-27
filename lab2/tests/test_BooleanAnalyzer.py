import unittest, sys
from io import StringIO
from source.BooleanAnalyzer import BooleanAnalyzer


class TestBooleanAnalyzer(unittest.TestCase):
    def test_analyzer(self):
        h, sys.stdout = sys.stdout, StringIO()
        try:
            a = BooleanAnalyzer("a & b")
            self.assertTrue(a.is_valid)
            a.analyze()
            a2 = BooleanAnalyzer("a &")
            self.assertFalse(a2.is_valid)
            self.assertTrue(len(sys.stdout.getvalue()) > 0)
        finally:
            sys.stdout = h

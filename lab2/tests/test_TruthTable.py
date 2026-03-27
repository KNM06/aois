import unittest
from source.TruthTable import TruthTable


class TestTruthTable(unittest.TestCase):
    def test_tt(self):
        tt = TruthTable(["a", "b", "&"], ["a", "b"])
        self.assertEqual(tt.get_terms(1), [(1, 1)])
        self.assertEqual(tt.get_sdnf(), "(a & b)")
        self.assertEqual(tt.get_sknf(), "(a V b) & (a V !b) & (!a V b)")
        self.assertEqual(tt.get_numeric_forms(), ("V(3)", "&(0, 1, 2)"))
        self.assertEqual(tt.get_index_form(), 1)
        t0 = TruthTable(["a", "!", "a", "&"], ["a"])
        self.assertEqual(t0.get_sdnf(), "Тождественный ноль")
        t1 = TruthTable(["a", "!", "a", "|"], ["a"])
        self.assertEqual(t1.get_sknf(), "Тождественная единица")
        self.assertEqual(t1.get_numeric_forms(), ("V(0, 1)", "Пусто"))

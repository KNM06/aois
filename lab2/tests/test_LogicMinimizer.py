import unittest
from source.LogicMinimizer import LogicMinimizer


class TestLogicMinimizer(unittest.TestCase):
    def test_minimizer(self):
        m1 = LogicMinimizer(1, [(0, 0), (0, 1), (1, 0), (1, 1)], 2)
        self.assertEqual(m1.get_glued_str(["a", "b"]), "1")
        self.assertEqual(m1.get_minimized_str(["a", "b"]), "1")
        m0 = LogicMinimizer(0, [], 2)
        self.assertEqual(m0.get_minimized_str(["a", "b"]), "0")
        m = LogicMinimizer(1, [(0, 1, 0), (0, 1, 1), (1, 1, 0)], 3)
        self.assertTrue(len(m.prime_implicants) > 0 and len(m.essential_pis) > 0)
        self.assertIsInstance(m.get_glued_str(["a", "b", "c"]), str)
        self.assertIsInstance(m.get_minimized_str(["a", "b", "c"]), str)
        mc = LogicMinimizer(0, [(0, 0), (0, 1)], 2)
        self.assertEqual(mc.get_minimized_str(["a", "b"]), "a")

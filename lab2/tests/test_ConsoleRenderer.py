import unittest, sys
from io import StringIO
from source.ConsoleRenderer import ConsoleRenderer
from source.LogicMinimizer import LogicMinimizer


class TestConsoleRenderer(unittest.TestCase):
    def test_renderer(self):
        h, sys.stdout = sys.stdout, StringIO()
        try:
            r = ConsoleRenderer(["a", "b"])
            tt = [((0, 0), 0), ((0, 1), 0), ((1, 0), 0), ((1, 1), 1)]
            r.print_truth_table("a & b", tt)
            r.print_quine_table(LogicMinimizer(1, [(0, 0), (0, 1), (1, 0), (1, 1)], 2))
            m2 = LogicMinimizer(1, [(0, 1), (1, 1)], 2)
            m2.additional_pis.append((1, "-"))
            m2.redundant_pis.add(("-", 1))
            r.print_quine_table(m2)
            r.print_karnaugh_map(tt)
            ConsoleRenderer(["a"]).print_karnaugh_map([((0,), 0), ((1,), 1)])
            ConsoleRenderer(["a", "b", "c"]).print_karnaugh_map(
                [((i // 4, (i // 2) % 2, i % 2), 1) for i in range(8)]
            )
            ConsoleRenderer(["a", "b", "c", "d", "e"]).print_karnaugh_map(
                [
                    ((i // 16, (i // 8) % 2, (i // 4) % 2, (i // 2) % 2, i % 2), 1)
                    for i in range(32)
                ]
            )
            self.assertTrue(len(sys.stdout.getvalue()) > 0)
        finally:
            sys.stdout = h

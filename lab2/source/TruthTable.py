import itertools
from source.LogicParser import LogicParser
from source.LogicFormatter import LogicFormatter


class TruthTable:
    def __init__(self, rpn, variables):
        self.variables = variables
        self.table = []
        self._build(rpn)

    def _build(self, rpn):
        n = len(self.variables)
        for combo in itertools.product([0, 1], repeat=n):
            val_dict = dict(zip(self.variables, combo))
            res = LogicParser.evaluate_rpn(rpn, val_dict)
            self.table.append((combo, res))

    def get_terms(self, target_res):
        return [combo for combo, res in self.table if res == target_res]

    def get_sdnf(self):
        expr = LogicFormatter.format_expr(
            self.get_terms(1), self.variables, is_dnf=True
        )
        return expr if expr else "Тождественный ноль"

    def get_sknf(self):
        expr = LogicFormatter.format_expr(
            self.get_terms(0), self.variables, is_dnf=False
        )
        return expr if expr else "Тождественная единица"

    def get_numeric_forms(self):
        ones = [str(int("".join(map(str, c)), 2)) for c, r in self.table if r == 1]
        zeros = [str(int("".join(map(str, c)), 2)) for c, r in self.table if r == 0]
        return (
            f"V({', '.join(ones)})" if ones else "Пусто",
            f"&({', '.join(zeros)})" if zeros else "Пусто",
        )

    def get_index_form(self):
        return int("".join(str(res) for _, res in self.table), 2)

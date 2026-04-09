from source.LogicMinimizer import LogicMinimizer
from source.LogicFormatter import LogicFormatter


class Lab3Synthesizer:
    def __init__(self):
        self.gray_bcd = {
            0: (0, 0, 0, 0),
            1: (0, 0, 0, 1),
            2: (0, 0, 1, 1),
            3: (0, 0, 1, 0),
            4: (0, 1, 1, 0),
            5: (0, 1, 1, 1),
            6: (0, 1, 0, 1),
            7: (0, 1, 0, 0),
            8: (1, 1, 0, 0),
            9: (1, 1, 0, 1),
        }

    def synthesize_ods3(self) -> dict[str, str]:
        variables = ["X", "Y", "P_in"]

        s_terms = [(0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1)]
        p_terms = [(0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 1, 1)]

        s_sdnf = LogicFormatter.format_expr(s_terms, variables, is_dnf=True)
        p_sdnf = LogicFormatter.format_expr(p_terms, variables, is_dnf=True)

        return {"S": s_sdnf, "P_out": p_sdnf}

    def synthesize_gray_bcd_adder(self) -> dict[str, str]:
        variables = ["A3", "A2", "A1", "A0", "B3", "B2", "B1", "B0"]
        terms = {"P_out": [], "S3": [], "S2": [], "S1": [], "S0": []}

        for a in range(10):
            for b in range(10):
                result = a + b + 1
                tens = result // 10
                units = result % 10

                input_combo = self.gray_bcd[a] + self.gray_bcd[b]

                if tens > 0:
                    terms["P_out"].append(input_combo)

                units_gray = self.gray_bcd[units]
                if units_gray[0] == 1:
                    terms["S3"].append(input_combo)
                if units_gray[1] == 1:
                    terms["S2"].append(input_combo)
                if units_gray[2] == 1:
                    terms["S1"].append(input_combo)
                if units_gray[3] == 1:
                    terms["S0"].append(input_combo)

        minimized_expressions = {}
        for out_var, on_terms in terms.items():
            minimizer = LogicMinimizer(1, on_terms, 8)
            minimized_expressions[out_var] = minimizer.get_minimized_str(variables)

        return minimized_expressions

    def synthesize_down_counter(self) -> dict[str, str]:
        variables = ["Q2", "Q1", "Q0"]
        terms = {"T2": [], "T1": [], "T0": []}

        for state in range(8):
            q2, q1, q0 = (state >> 2) & 1, (state >> 1) & 1, state & 1

            next_state = (state - 1) % 8
            nq2, nq1, nq0 = (next_state >> 2) & 1, (next_state >> 1) & 1, next_state & 1

            combo = (q2, q1, q0)
            if q2 != nq2:
                terms["T2"].append(combo)
            if q1 != nq1:
                terms["T1"].append(combo)
            if q0 != nq0:
                terms["T0"].append(combo)

        minimized_expressions = {}
        for t_var, on_terms in terms.items():
            minimizer = LogicMinimizer(1, on_terms, 3)
            minimized_expressions[t_var] = minimizer.get_minimized_str(variables)

        return minimized_expressions

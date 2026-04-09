import itertools


class BooleanMath:
    def __init__(self, truth_table: list, variables: list[str]) -> None:
        self.tt = truth_table
        self.variables = variables

    def get_post_classes(self) -> dict[str, bool]:
        t0 = self.tt[0][1] == 0
        t1 = self.tt[-1][1] == 1

        n = len(self.tt)
        s = all(self.tt[i][1] != self.tt[n - 1 - i][1] for i in range(n // 2))

        m = True
        for i in range(n):
            for j in range(i + 1, n):
                is_less = all(a <= b for a, b in zip(self.tt[i][0], self.tt[j][0]))
                if is_less and self.tt[i][1] > self.tt[j][1]:
                    m = False
                    break
            if not m:
                break

        coeffs = self._get_zhegalkin_coeffs()
        l = not any(
            coeff == 1 and bin(i).count("1") > 1 for i, coeff in enumerate(coeffs)
        )

        return {"T0": t0, "T1": t1, "S": s, "M": m, "L": l}

    def _get_zhegalkin_coeffs(self) -> list[int]:
        row = [res for _, res in self.tt]
        coeffs = [row[0]]
        for _ in range(len(row) - 1):
            row = [row[i] ^ row[i + 1] for i in range(len(row) - 1)]
            coeffs.append(row[0])
        return coeffs

    def get_zhegalkin_polynomial(self) -> str:
        coeffs = self._get_zhegalkin_coeffs()
        terms = []
        for i, coeff in enumerate(coeffs):
            if coeff == 1:
                term_vars = [
                    self.variables[j] for j, val in enumerate(self.tt[i][0]) if val == 1
                ]
                terms.append("".join(term_vars) if term_vars else "1")
        return " ^ ".join(terms) if terms else "0"

    def get_fictitious_variables(self) -> list[str]:
        fict_vars = []
        lookup = {combo: res for combo, res in self.tt}
        for i, var in enumerate(self.variables):
            is_fict = True
            for combo, res in self.tt:
                if combo[i] == 0:
                    pair = list(combo)
                    pair[i] = 1
                    if res != lookup[tuple(pair)]:
                        is_fict = False
                        break
            if is_fict:
                fict_vars.append(var)
        return fict_vars

    def get_boolean_derivatives(self) -> dict:
        lookup = {combo: res for combo, res in self.tt}
        results = {}
        max_vars = min(4, len(self.variables))

        for k in range(1, max_vars + 1):
            for diff_vars in itertools.combinations(self.variables, k):
                static_vars = [v for v in self.variables if v not in diff_vars]

                static_idx = [self.variables.index(v) for v in static_vars]
                diff_idx = [self.variables.index(v) for v in diff_vars]

                col = []

                for static_vals in itertools.product([0, 1], repeat=len(static_vars)):
                    xor_sum = 0

                    for diff_vals in itertools.product([0, 1], repeat=k):
                        full_combo = [0] * len(self.variables)
                        for i, val in zip(static_idx, static_vals):
                            full_combo[i] = val
                        for i, val in zip(diff_idx, diff_vals):
                            full_combo[i] = val

                        xor_sum ^= lookup[tuple(full_combo)]

                    col.append(xor_sum)
                results[diff_vars] = col

        return results

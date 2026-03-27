from source.LogicFormatter import LogicFormatter


class LogicMinimizer:
    def __init__(self, target_res, base_terms, num_vars):
        self.target_res = target_res
        self.base_terms = sorted(base_terms, key=str)
        self.is_edge_case = not self.base_terms or len(self.base_terms) == 2**num_vars
        self.is_dnf = target_res == 1

        self.prime_implicants = set()
        self.coverage = {}
        self.essential_pis = set()
        self.additional_pis = []
        self.redundant_pis = set()

        if not self.is_edge_case:
            self._run_quine_mccluskey()

    def _run_quine_mccluskey(self):
        terms = set(self.base_terms)
        while terms:
            new_terms = set()
            used = set()
            t_list = list(terms)
            for i in range(len(t_list)):
                for j in range(i + 1, len(t_list)):
                    t1, t2 = t_list[i], t_list[j]
                    diffs = [k for k in range(len(t1)) if t1[k] != t2[k]]
                    if len(diffs) == 1:
                        used.update([t1, t2])
                        new_term = list(t1)
                        new_term[diffs[0]] = "-"
                        new_terms.add(tuple(new_term))
            self.prime_implicants.update(terms - used)
            terms = new_terms

        for pi in self.prime_implicants:
            self.coverage[pi] = {
                bt
                for bt in self.base_terms
                if all(p == "-" or p == b for p, b in zip(pi, bt))
            }

        uncovered = set(self.base_terms)
        for bt in self.base_terms:
            covering = [pi for pi, cov in self.coverage.items() if bt in cov]
            if len(covering) == 1:
                self.essential_pis.add(covering[0])

        for epi in self.essential_pis:
            uncovered -= self.coverage[epi]

        remaining_pis = set(self.prime_implicants) - self.essential_pis
        while uncovered and remaining_pis:
            best_pi = max(
                remaining_pis, key=lambda pi: len(self.coverage[pi] & uncovered)
            )
            self.additional_pis.append(best_pi)
            uncovered -= self.coverage[best_pi]
            remaining_pis.remove(best_pi)

        self.redundant_pis = (
            self.prime_implicants - self.essential_pis - set(self.additional_pis)
        )

    def get_glued_str(self, vars):
        if self.is_edge_case:
            return "1" if self.is_dnf else "0"
        return LogicFormatter.format_expr(self.prime_implicants, vars, self.is_dnf)

    def get_minimized_str(self, vars):
        if self.is_edge_case:
            return "1" if self.is_dnf else "0"
        final_pis = list(self.essential_pis) + self.additional_pis
        return LogicFormatter.format_expr(final_pis, vars, self.is_dnf)

from source.LogicFormatter import LogicFormatter


class ConsoleRenderer:
    def __init__(self, variables: list[str]) -> None:
        self.variables = variables

    def print_truth_table(self, raw_expr: str, tt: list) -> None:
        print(f"\n--- Таблица истинности для: {raw_expr} ---")
        header = " | ".join(self.variables) + " || F"
        print(header)
        print("-" * len(header))
        for combo, res in tt:
            print(" | ".join(map(str, combo)) + f" || {res}")

    def print_quine_table(self, minimizer) -> None:
        if minimizer.is_edge_case:
            print("  Таблица не требуется (краевой случай).")
            return

        fmt_term = lambda pi: LogicFormatter.format_term(
            pi, self.variables, minimizer.is_dnf
        )
        fmt_base = lambda bt: "".join(
            [
                f"{var}" if val == (1 if minimizer.is_dnf else 0) else f"!{var}"
                for var, val in zip(self.variables, bt)
            ]
        )

        header_cols = [fmt_base(bt) for bt in minimizer.base_terms]
        col_widths = [max(len(col), 3) for col in header_cols]
        pi_strs = [fmt_term(pi) for pi in sorted(minimizer.prime_implicants, key=str)]
        max_pi_len = max([len(s) for s in pi_strs] + [12])

        header = f"  {'Импликанты':<{max_pi_len}} | " + " | ".join(
            [f"{col:^{w}}" for col, w in zip(header_cols, col_widths)]
        )
        print(header)
        print("  " + "-" * (len(header) - 2))

        for pi, pi_str in zip(sorted(minimizer.prime_implicants, key=str), pi_strs):
            cells = [
                "X" if bt in minimizer.coverage[pi] else ""
                for bt in minimizer.base_terms
            ]
            print(
                f"  {pi_str:<{max_pi_len}} | "
                + " | ".join([f"{c:^{w}}" for c, w in zip(cells, col_widths)])
            )

        print("\n  Анализ таблицы:")
        e_strs = [fmt_term(pi) for pi in sorted(minimizer.essential_pis, key=str)]
        print(
            f"  Существенные импликанты:      {', '.join(e_strs) if e_strs else 'отсутствуют'}"
        )

        a_strs = [fmt_term(pi) for pi in sorted(minimizer.additional_pis, key=str)]
        if a_strs:
            print(f"  Дополнительные импликанты:    {', '.join(a_strs)}")

        r_strs = [fmt_term(pi) for pi in sorted(minimizer.redundant_pis, key=str)]
        print(
            f"  Лишние (отброшенные):         {', '.join(r_strs) if r_strs else 'отсутствуют'}"
        )
        print(
            f"  Итоговая форма из таблицы:    {minimizer.get_minimized_str(self.variables)}"
        )

    def print_karnaugh_map(self, tt: list) -> None:
        n = len(self.variables)
        if n < 2 or n > 5:
            print(
                f"  Отрисовка карты Карно поддерживается для 2-5 переменных (у вас {n})."
            )
            return

        r_count, c_count = n // 2, n - (n // 2)
        r_vars, c_vars = self.variables[:r_count], self.variables[r_count:]

        def get_gray(bits):
            if bits == 1:
                return [(0,), (1,)]
            if bits == 2:
                return [(0, 0), (0, 1), (1, 1), (1, 0)]
            if bits == 3:
                return [
                    (0, 0, 0),
                    (0, 0, 1),
                    (0, 1, 1),
                    (0, 1, 0),
                    (1, 1, 0),
                    (1, 1, 1),
                    (1, 0, 1),
                    (1, 0, 0),
                ]
            return []

        row_gray, col_gray = get_gray(r_count), get_gray(c_count)
        lookup = {c: r for c, r in tt}

        corner = f"{''.join(r_vars)}\\{''.join(c_vars)}"
        cw = max(len(corner), 5)

        c_heads = ["".join(map(str, cg)) for cg in col_gray]
        header = f"  {corner:<{cw}} | " + " | ".join(f"{ch:^3}" for ch in c_heads)

        print(header)
        print("  " + "-" * (len(header) - 2))

        for rg in row_gray:
            row_cells = [f"{lookup.get(rg + cg, '-'):^3}" for cg in col_gray]
            print(f"  {''.join(map(str, rg)):<{cw}} | " + " | ".join(row_cells))

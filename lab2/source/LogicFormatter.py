class LogicFormatter:
    @staticmethod
    def format_term(term, variables, is_dnf):
        parts = []
        for var, val in zip(variables, term):
            if val == "-":
                continue
            if is_dnf:
                parts.append(f"{var}" if val == 1 else f"!{var}")
            else:
                parts.append(f"{var}" if val == 0 else f"!{var}")

        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0]
        return "(" + (" & " if is_dnf else " V ").join(parts) + ")"

    @staticmethod
    def format_expr(terms, variables, is_dnf):
        if not terms:
            return None
        strs = [
            LogicFormatter.format_term(t, variables, is_dnf)
            for t in sorted(terms, key=str)
        ]
        return (" V " if is_dnf else " & ").join(strs)

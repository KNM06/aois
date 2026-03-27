import re


class LogicParser:
    PRECEDENCE = {"!": 5, "&": 4, "|": 3, "->": 2, "~": 1, "(": 0, ")": 0}

    @staticmethod
    def is_variable(token):
        return token not in ("!", "&", "|", "->", "~", "(", ")")

    @staticmethod
    def tokenize(expression):
        expr = expression.replace("V", "|")
        expr = re.sub(r"\b[v]\b", "|", expr)
        expr = expr.replace(" ", "")

        token_pattern = r"->|[a-zA-Z0-9_]+|[!&|~()]"
        tokens = re.findall(token_pattern, expr)
        if len("".join(tokens)) != len(expr):
            raise ValueError(
                f"В выражении '{expression}' присутствуют недопустимые символы!"
            )
        return tokens

    @staticmethod
    def validate(tokens):
        if not tokens:
            raise ValueError("Пустое выражение!")
        balance = 0
        for i, token in enumerate(tokens):
            if LogicParser.is_variable(token):
                if token[0].isdigit():
                    raise ValueError(
                        f"Ошибка: имя переменной '{token}' не может начинаться с цифры!"
                    )
                if token[0] == "_":
                    raise ValueError(
                        f"Ошибка: имя переменной '{token}' не может начинаться с нижнего подчеркивания!"
                    )

            if token == "(":
                balance += 1
            elif token == ")":
                balance -= 1
                if balance < 0:
                    raise ValueError(
                        "Синтаксическая ошибка: закрывающая скобка раньше открывающей."
                    )

            if i > 0:
                prev = tokens[i - 1]
                prev_is_var = LogicParser.is_variable(prev)
                token_is_var = LogicParser.is_variable(token)
                prev_is_bin = prev in ("&", "|", "->", "~")
                token_is_bin = token in ("&", "|", "->", "~")

                if prev_is_var and (token == "!" or token == "(" or token_is_var):
                    raise ValueError(
                        f"Ошибка: пропущен бинарный оператор между '{prev}' и '{token}'"
                    )
                if prev == ")" and (token == "!" or token == "(" or token_is_var):
                    raise ValueError(
                        f"Ошибка: пропущен бинарный оператор между '{prev}' и '{token}'"
                    )
                if (prev_is_bin or prev == "!" or prev == "(") and (
                    token_is_bin or token == ")"
                ):
                    raise ValueError(
                        f"Ошибка: некорректное расположение '{token}' после '{prev}'"
                    )

        if balance != 0:
            raise ValueError("Синтаксическая ошибка: не все скобки закрыты.")
        if tokens[0] in ("&", "|", "->", "~"):
            raise ValueError(
                f"Ошибка: выражение не может начинаться с оператора '{tokens[0]}'"
            )
        if tokens[-1] in ("!", "&", "|", "->", "~"):
            raise ValueError(
                f"Ошибка: выражение не может заканчиваться оператором '{tokens[-1]}'"
            )

    @staticmethod
    def to_rpn(tokens):
        output = []
        stack = []
        for token in tokens:
            if LogicParser.is_variable(token):
                output.append(token)
            elif token == "!":
                stack.append(token)
            elif token in ("&", "|", "->", "~"):
                while (
                    stack
                    and stack[-1] != "("
                    and LogicParser.PRECEDENCE[stack[-1]]
                    >= LogicParser.PRECEDENCE[token]
                ):
                    output.append(stack.pop())
                stack.append(token)
            elif token == "(":
                stack.append(token)
            elif token == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                if stack and stack[-1] == "(":
                    stack.pop()
        while stack:
            output.append(stack.pop())
        return output

    @staticmethod
    def evaluate_rpn(rpn, values):
        stack = []
        for token in rpn:
            if LogicParser.is_variable(token):
                stack.append(values[token])
            elif token == "!":
                stack.append(int(not stack.pop()))
            elif token == "&":
                stack.append(stack.pop() & stack.pop())
            elif token == "|":
                stack.append(stack.pop() | stack.pop())
            elif token == "->":
                b = stack.pop()
                a = stack.pop()
                stack.append(int(a <= b))
            elif token == "~":
                stack.append(int(stack.pop() == stack.pop()))

        if len(stack) != 1:
            raise ValueError("Синтаксическая ошибка: пропущен оператор связи.")
        return stack[0]

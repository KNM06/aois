from source.LogicParser import LogicParser
from source.TruthTable import TruthTable
from source.BooleanMath import BooleanMath
from source.LogicMinimizer import LogicMinimizer
from source.ConsoleRenderer import ConsoleRenderer


class BooleanAnalyzer:
    def __init__(self, expression: str) -> None:
        self.raw_expression = expression
        self.is_valid = False
        try:
            tokens = LogicParser.tokenize(expression)
            LogicParser.validate(tokens)
            self.rpn = LogicParser.to_rpn(tokens)
            self.variables = sorted(
                list(set(t for t in tokens if LogicParser.is_variable(t)))
            )

            self.tt_generator = TruthTable(self.rpn, self.variables)
            self.math = BooleanMath(self.tt_generator.table, self.variables)

            self.min_dnf = LogicMinimizer(
                1, self.tt_generator.get_terms(1), len(self.variables)
            )
            self.min_cnf = LogicMinimizer(
                0, self.tt_generator.get_terms(0), len(self.variables)
            )

            self.renderer = ConsoleRenderer(self.variables)
            self.is_valid = True
        except ValueError as e:
            print(f"Ошибка анализа выражения '{expression}':\n> {e}")

    def analyze(self) -> None:
        if not self.is_valid:
            return

        self.renderer.print_truth_table(self.raw_expression, self.tt_generator.table)

        print(f"СДНФ: {self.tt_generator.get_sdnf()}")
        print(f"СКНФ: {self.tt_generator.get_sknf()}")

        num_sdnf, num_sknf = self.tt_generator.get_numeric_forms()
        print(f"Числовая СДНФ: {num_sdnf}")
        print(f"Числовая СКНФ: {num_sknf}")
        print(f"Индексная форма: {self.tt_generator.get_index_form()}")

        classes = self.math.get_post_classes()
        print("\nКлассы Поста:")
        print(f"  T0 (Сохраняет 0):      {'+' if classes['T0'] else '-'}")
        print(f"  T1 (Сохраняет 1):      {'+' if classes['T1'] else '-'}")
        print(f"  S  (Самодвойственная): {'+' if classes['S'] else '-'}")
        print(f"  M  (Монотонная):       {'+' if classes['M'] else '-'}")
        print(f"  L  (Линейная):         {'+' if classes['L'] else '-'}")

        print(f"\nПолином Жегалкина: {self.math.get_zhegalkin_polynomial()}")

        fict = self.math.get_fictitious_variables()
        print(f"Фиктивные переменные: {', '.join(fict) if fict else 'отсутствуют'}")

        derivs = self.math.get_boolean_derivatives()
        if derivs:
            print("\nБулева дифференциация (вектор значений):")
            for diff_vars, col in derivs.items():
                print(
                    f"  dF/d({','.join(diff_vars)}):{'':<10}"[:16]
                    + f" {''.join(map(str, col))}"
                )

        print("\nРасчетный метод минимизации:")
        print(
            f"  [ДНФ] Стадия склеивания: {self.min_dnf.get_glued_str(self.variables)}"
        )
        print(
            f"  [ДНФ] Минимальная форма: {self.min_dnf.get_minimized_str(self.variables)}"
        )
        print(
            f"  [КНФ] Стадия склеивания: {self.min_cnf.get_glued_str(self.variables)}"
        )
        print(
            f"  [КНФ] Минимальная форма: {self.min_cnf.get_minimized_str(self.variables)}"
        )

        print("\nРасчетно-табличный метод (Таблица Квайна):")
        print(">> Таблица для СДНФ:")
        self.renderer.print_quine_table(self.min_dnf)
        print("\n>> Таблица для СКНФ:")
        self.renderer.print_quine_table(self.min_cnf)

        print("\nТабличный метод минимизации (Карта Карно):")
        self.renderer.print_karnaugh_map(self.tt_generator.table)

        if not self.min_dnf.is_edge_case:
            print("\n  Анализ карты Карно:")
            print(
                f"  [ДНФ] Сгруппировав области из единиц (1): {self.min_dnf.get_minimized_str(self.variables)}"
            )
            print(
                f"  [КНФ] Сгруппировав области из нулей (0):  {self.min_cnf.get_minimized_str(self.variables)}"
            )

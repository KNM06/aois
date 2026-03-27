from source.BooleanAnalyzer import BooleanAnalyzer


def main():
    print("=" * 50)
    print("=== Анализатор булевых функций ===")
    print("Поддерживаемые операторы:")
    print("  !        - Отрицание (NOT)")
    print("  &        - Конъюнкция (AND)")
    print("  | или V  - Дизъюнкция (OR)")
    print("  ->       - Импликация")
    print("  ~        - Эквивалентность")
    print("  ()       - Скобки для приоритета")
    print("Пример ввода: (!a & b) -> c")
    print("Для выхода введите '0', 'exit' или 'выход'.")
    print("=" * 50)

    while True:
        expr = input("\nВведите логическое выражение: ").strip()
        if expr.lower() in ("0", "exit", "выход"):
            print("Работа завершена")
            break
        if not expr:
            continue

        analyzer = BooleanAnalyzer(expr)
        analyzer.analyze()
        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()

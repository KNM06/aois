from source.IntegerALU import IntegerALU
from source.FloatALU import FloatALU
from source.BCDALU import BCDALU
from constants import BITS, BCD_MAX_DIGITS


def get_int_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: пожалуйста, введите корректное целое число.")


def get_float_input(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print(
                "Ошибка: пожалуйста, введите корректное вещественное число (например, 12.5)."
            )


def main_menu() -> None:
    int_alu: IntegerALU = IntegerALU()
    float_alu: FloatALU = FloatALU()
    bcd_alu: BCDALU = BCDALU()

    while True:
        print("\n" + "=" * 55)
        print(" Главное меню BinaryALU")
        print("=" * 55)
        print("--- Целочисленная арифметика ---")
        print("1. Перевод целого числа в прямой, обратный и доп. коды")
        print("2. Сложение (дополнительный код)")
        print("3. Вычитание (дополнительный код)")
        print("4. Умножение (прямой код)")
        print("5. Деление (прямой код)")
        print("\n--- Арифметика с плавающей запятой (IEEE-754) ---")
        print(f"6. Перевод float в IEEE-754 ({BITS}-bit)")
        print("7. Сложение IEEE-754")
        print("8. Вычитание IEEE-754")
        print("9. Умножение IEEE-754")
        print("10. Деление IEEE-754")
        print("\n--- Двоично-десятичный код (BCD 8421) ---")
        print("11. Перевод целого числа в BCD 8421")
        print("12. Сложение в коде BCD 8421")
        print("0. Выход")
        print("=" * 55)

        choice: str = input("Выберите операцию (0-12): ").strip()

        if choice == "0":
            print("Работа завершена. До свидания!")
            break

        elif choice == "1":
            n = get_int_input("Введите целое число для перевода: ")
            direct = int_alu.to_direct_code(n)
            inverse = int_alu.to_inverse_code(n)
            twos = int_alu.to_additional_code(n)
            print("\nРезультаты перевода:")
            int_alu.print_result("Прямой код        ", direct, float(n))
            int_alu.print_result("Обратный код      ", inverse, float(n))
            int_alu.print_result("Дополнительный код", twos, float(n))

        elif choice == "2":
            n1 = get_int_input("Введите первое целое число: ")
            n2 = get_int_input("Введите второе целое число: ")
            int_alu.add_additional(n1, n2)

        elif choice == "3":
            n1 = get_int_input("Введите уменьшаемое (целое число): ")
            n2 = get_int_input("Введите вычитаемое (целое число): ")
            int_alu.sub_additional(n1, n2)

        elif choice == "4":
            n1 = get_int_input("Введите первый множитель (целое число): ")
            n2 = get_int_input("Введите второй множитель (целое число): ")
            int_alu.mul_direct(n1, n2)

        elif choice == "5":
            n1 = get_int_input("Введите делимое (целое число): ")
            n2 = get_int_input("Введите делитель (целое число): ")
            try:
                int_alu.div_direct(n1, n2)
            except ZeroDivisionError as e:
                print(f"Ошибка выполнения: {e}")

        elif choice == "6":
            f1 = get_float_input("Введите вещественное число: ")
            float_alu.float_to_ieee754(f1)

        elif choice == "7":
            f1 = get_float_input("Введите первое вещественное число: ")
            f2 = get_float_input("Введите второе вещественное число: ")
            arr1 = float_alu.float_to_ieee754(f1)
            arr2 = float_alu.float_to_ieee754(f2)
            float_alu.add_ieee754(arr1, arr2)

        elif choice == "8":
            f1 = get_float_input("Введите уменьшаемое (вещественное число): ")
            f2 = get_float_input("Введите вычитаемое (вещественное число): ")
            arr1 = float_alu.float_to_ieee754(f1)
            arr2 = float_alu.float_to_ieee754(f2)
            float_alu.sub_ieee754(arr1, arr2)

        elif choice == "9":
            f1 = get_float_input("Введите первый множитель (вещественное): ")
            f2 = get_float_input("Введите второй множитель (вещественное): ")
            arr1 = float_alu.float_to_ieee754(f1)
            arr2 = float_alu.float_to_ieee754(f2)
            float_alu.mul_ieee754_pure(arr1, arr2)

        elif choice == "10":
            f1 = get_float_input("Введите делимое (вещественное): ")
            f2 = get_float_input("Введите делитель (вещественное): ")
            arr1 = float_alu.float_to_ieee754(f1)
            arr2 = float_alu.float_to_ieee754(f2)
            try:
                float_alu.div_ieee754_pure(arr1, arr2)
            except ZeroDivisionError as e:
                print(f"Ошибка выполнения: {e}")

        elif choice == "11":
            n1 = get_int_input(f"Введите целое число (макс. {BCD_MAX_DIGITS} цифр): ")
            try:
                bcd_alu.int_to_bcd_8421(n1)
            except ValueError as e:
                print(f"Ошибка: {e}")

        elif choice == "12":
            n1 = get_int_input("Введите первое слагаемое (целое число): ")
            n2 = get_int_input("Введите второе слагаемое (целое число): ")
            try:
                bcd_alu.add_bcd_8421(n1, n2)
            except ValueError as e:
                print(f"Ошибка: {e}")

        else:
            print("Неверный ввод. Пожалуйста, выберите число от 0 до 12.")


if __name__ == "__main__":
    main_menu()

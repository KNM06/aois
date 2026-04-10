from source.HashTable import HashTable


if __name__ == "__main__":
    while True:
        try:
            user_size = int(input("Введите размер хеш-таблицы (H): "))
            user_start_address = int(input("Введите начальный адрес (B): "))
            if user_size > 0:
                break
            else:
                print("Ошибка: Размер должен быть положительным числом.")
        except ValueError:
            print("Ошибка: Введите целое число.")

    ht = HashTable(size=user_size, start_address=user_start_address)
    print(f"\nХеш-таблица (H={user_size}, B={user_start_address}) успешно создана.")

    while True:
        print("\n--- Меню Хеш-таблицы ---")
        print("1. Добавить новую запись")
        print("2. Найти запись по ключу")
        print("3. Обновить существующую запись")
        print("4. Удалить запись")
        print("5. Вывести хеш-таблицу на экран")
        print("6. Создание тестовых данных")
        print("7. Выход")

        choice = input("\nВыберите действие (1-7): ").strip()

        if choice == "1":
            key = input("Введите ключ (Фамилия): ").strip()
            data = input("Введите данные (Имя): ").strip()
            if key:
                if ht.insert(key, data):
                    print("Запись успешно добавлена.")
            else:
                print("Ошибка: Ключ не может быть пустым.")

        elif choice == "2":
            key = input("Введите ключ для поиска (Фамилия): ").strip()
            index = ht.search(key)
            if index is not None:
                print(f"Запись найдена по индексу {index}: {ht.table[index].pi}")
            else:
                print("Запись с таким ключом не найдена.")

        elif choice == "3":
            key = input("Введите ключ для обновления (Фамилия): ").strip()
            index = ht.search(key)
            if index is not None:
                new_data = input("Введите новые данные (Имя): ").strip()
                ht.table[index].pi = new_data
                print("Запись успешно обновлена.")
            else:
                print("Запись с таким ключом не найдена.")

        elif choice == "4":
            key = input("Введите ключ для удаления (Фамилия): ").strip()
            if ht.delete(key):
                print("Запись успешно удалена.")

        elif choice == "5":
            ht.display()

        elif choice == "6":
            students = [
                ("Иванов", "Иван"),
                ("Иванченко", "Петр"),
                ("Ивантеев", "Сергей"),
                ("Ивашкевич", "Анна"),
                ("Макаров", "Максим"),
                ("Матвеев", "Олег"),
                ("Малышев", "Илья"),
                ("Смирнов", "Алексей"),
                ("Кузнецов", "Дмитрий"),
                ("Попов", "Александр"),
                ("Васильев", "Василий"),
                ("Зайцев", "Николай"),
            ]
            added_count = 0
            for key, data in students:
                if ht.search(key) is None:
                    if ht.insert(key, data):
                        added_count += 1
            print(
                f"Тестовые данные загружены. Успешно добавлено новых записей: {added_count}."
            )

        elif choice == "7":
            print("Работа программы завершена.")
            break

        else:
            print("Ошибка: Неверный ввод. Пожалуйста, выберите пункт от 1 до 7.")

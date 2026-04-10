from source.HashRecord import HashRecord


class HashTable:
    def __init__(self, size=20, start_address=5):
        self.H = size
        self.B = start_address
        self.table = [HashRecord() for _ in range(self.H)]
        self.alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        self.history = []

    def _get_char_value(self, char):
        char = char.upper()
        if char in self.alphabet:
            return self.alphabet.index(char)
        return 0

    def calculate_v(self, key):
        if not key:
            return 0

        val1 = self._get_char_value(key[0])
        val2 = self._get_char_value(key[1]) if len(key) > 1 else 0

        return val1 * 33 + val2

    def calculate_h(self, v):
        return (v % self.H) + self.B

    def insert(self, key, data):
        if self.search(key) is not None:
            print(f"Ошибка: Ключ '{key}' уже существует в таблице.")
            return False

        v = self.calculate_v(key)
        h = self.calculate_h(v)

        start_index = h % self.H

        order_num = len(self.history) + 1
        self.history.append((order_num, key, v, h))

        if self.table[start_index].u == 0 or self.table[start_index].d == 1:
            self.table[start_index].id = key
            self.table[start_index].pi = data
            self.table[start_index].u = 1
            self.table[start_index].d = 0
            self.table[start_index].t = 1
            return True

        self.table[start_index].c = 1
        last_index = start_index
        while self.table[last_index].t == 0 and self.table[last_index].p0 is not None:
            last_index = self.table[last_index].p0

        for step in range(1, self.H + 1):
            q = step * step
            current_index = (h + q) % self.H

            if self.table[current_index].u == 0 or self.table[current_index].d == 1:
                self.table[current_index].id = key
                self.table[current_index].pi = data
                self.table[current_index].u = 1
                self.table[current_index].d = 0
                self.table[current_index].t = 1

                self.table[last_index].t = 0
                self.table[last_index].p0 = current_index
                return True

        print(f"Ошибка: Таблица переполнена.")
        return False

    def search(self, key):
        v = self.calculate_v(key)
        h = self.calculate_h(v)

        for step in range(self.H + 1):
            q = step * step
            current_index = (h + q) % self.H

            if self.table[current_index].u == 0:
                return None

            if self.table[current_index].u == 1 and self.table[current_index].d == 0:
                if self.table[current_index].id == key:
                    return current_index

        return None

    def delete(self, key):
        index = self.search(key)

        if index is None:
            print(f"Ошибка: Запись с ключом '{key}' не найдена.")
            return False

        self.table[index].d = 1

        prev_index = -1
        for i in range(self.H):
            if self.table[i].p0 == index:
                prev_index = i
                break

        if prev_index != -1:
            if self.table[index].t == 1:
                self.table[prev_index].t = 1
                self.table[prev_index].p0 = None
            else:
                self.table[prev_index].p0 = self.table[index].p0
        else:
            if self.table[index].p0 is not None:
                next_index = self.table[index].p0
                self.table[next_index].c = 1

        self.table[index].id = None
        self.table[index].pi = None
        self.table[index].p0 = None
        self.table[index].t = 0
        self.table[index].c = 0

        return True

    def get_load_factor(self):
        occupied = sum(1 for record in self.table if record.u == 1 and record.d == 0)
        return occupied / self.H

    def display(self):
        print("-" * 110)
        print(
            f"{'№':<3} | {'Фамилия':<13} | {'V':<4} | {'h':<3} || {'№ стр':<5} | {'ID':<13} | {'P0':<3} | {'L'} | {'U'} | {'D'} | {'T'} | {'C'} | {'Pi (Данные)'}"
        )
        print("-" * 110)

        for i in range(self.H):
            if i < len(self.history):
                num, hist_key, v, h = self.history[i]
                left_str = f"{num:<3} | {hist_key:<13} | {v:<4} | {h:<3}"
            else:
                left_str = f"{'':<3} | {'':<13} | {'':<4} | {'':<3}"

            record = self.table[i]
            rec_id = str(record.id) if record.id else ""
            rec_p0 = str(record.p0) if record.p0 is not None else ""
            rec_pi = str(record.pi) if record.pi else ""

            right_str = f"{i:<5} | {rec_id:<13} | {rec_p0:<3} | {record.l} | {record.u} | {record.d} | {record.t} | {record.c} | {rec_pi}"

            print(f"{left_str} || {right_str}")

        print("-" * 110)
        print(f"Коэффициент заполнения: {self.get_load_factor():.2f}")
        print("-" * 110)

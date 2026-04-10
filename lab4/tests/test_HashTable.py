import unittest
from unittest.mock import patch
from source.HashTable import HashTable


class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable(size=5, start_address=0)

    def test_initialization(self):
        self.assertEqual(self.ht.H, 5)
        self.assertEqual(self.ht.B, 0)
        self.assertEqual(len(self.ht.table), 5)
        self.assertEqual(len(self.ht.history), 0)

    def test_calculate_v(self):
        self.assertEqual(self.ht.calculate_v("АБ"), 1)
        self.assertEqual(self.ht.calculate_v("В"), 66)
        self.assertEqual(self.ht.calculate_v(""), 0)

    def test_calculate_v_edge_cases(self):
        self.assertEqual(self.ht.calculate_v("Б"), 33)
        self.assertEqual(self.ht.calculate_v("123"), 0)

    def test_calculate_h(self):
        v = 66
        self.assertEqual(self.ht.calculate_h(v), 1)

        ht2 = HashTable(size=5, start_address=10)
        self.assertEqual(ht2.calculate_h(v), 11)

    def test_insert_and_search(self):
        self.assertTrue(self.ht.insert("Иванов", "Иван"))
        index = self.ht.search("Иванов")
        self.assertIsNotNone(index)
        self.assertEqual(self.ht.table[index].pi, "Иван")

    def test_insert_duplicate(self):
        self.assertTrue(self.ht.insert("Иванов", "Иван"))
        self.assertFalse(self.ht.insert("Иванов", "Другой Иван"))

    def test_collision_quadratic_probing(self):
        self.assertTrue(self.ht.insert("А", "Данные 1"))
        self.assertTrue(self.ht.insert("Е", "Данные 2"))
        self.assertTrue(self.ht.insert("Й", "Данные 3"))

        self.assertEqual(self.ht.search("А"), 0)
        self.assertEqual(self.ht.search("Е"), 1)
        self.assertEqual(self.ht.search("Й"), 4)

        self.assertEqual(self.ht.table[0].c, 1)
        self.assertEqual(self.ht.table[0].p0, 1)
        self.assertEqual(self.ht.table[1].p0, 4)

    def test_table_overflow(self):
        ht = HashTable(size=2, start_address=0)
        self.assertTrue(ht.insert("А", "1"))
        self.assertTrue(ht.insert("Б", "2"))
        self.assertFalse(ht.insert("В", "3"))

    def test_delete(self):
        self.ht.insert("Иванов", "Иван")
        self.ht.insert("Петров", "Петр")

        self.assertTrue(self.ht.delete("Иванов"))
        self.assertIsNone(self.ht.search("Иванов"))

        self.assertFalse(self.ht.delete("Иванов"))
        self.assertFalse(self.ht.delete("Сидоров"))

        self.assertTrue(self.ht.insert("Иванов", "Новый Иван"))

    def test_delete_complex_chains(self):
        self.ht.insert("А", "1")
        self.ht.insert("Е", "2")
        self.ht.insert("Й", "3")
        self.assertTrue(self.ht.delete("Е"))  
        self.assertTrue(self.ht.delete("А"))  
        self.assertTrue(self.ht.delete("Й"))  
        
    def test_load_factor(self):
        self.assertEqual(self.ht.get_load_factor(), 0.0)
        self.ht.insert("А", "1")
        self.ht.insert("Б", "2")
        self.assertEqual(self.ht.get_load_factor(), 2 / 5)

        self.ht.delete("А")
        self.assertEqual(self.ht.get_load_factor(), 1 / 5)

    @patch('builtins.print')
    def test_display(self, mock_print):
        self.ht.insert("А", "1")
        self.ht.insert("Б", "2")
        self.ht.display()
        self.assertTrue(mock_print.called)

if __name__ == "__main__":
    unittest.main()

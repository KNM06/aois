import unittest
from source.HashRecord import HashRecord


class TestHashRecord(unittest.TestCase):
    def test_initialization(self):
        record = HashRecord()
        self.assertIsNone(record.id)
        self.assertIsNone(record.pi)
        self.assertEqual(record.u, 0)
        self.assertEqual(record.d, 0)
        self.assertEqual(record.c, 0)
        self.assertEqual(record.t, 0)
        self.assertIsNone(record.p0)
        self.assertEqual(record.l, 0)

    def test_str_representation(self):
        record = HashRecord()
        record.id = "Иванов"
        record.pi = "Иван"
        record.u = 1
        record.t = 1
        record.p0 = 3

        expected_str = f"{'Иванов':12} | {'3':4} | 0 | 1 | 0 | 1 | 0 | Иван"
        self.assertEqual(str(record), expected_str)


if __name__ == "__main__":
    unittest.main()

import unittest
import get_file_list as gfl


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.full_list = ["aaa", "bbb", "ccc"]
        self.short_list = ["aaa", "bbb"]

    def test_get_unique_file(self):
        self.assertEqual(gfl.get_unique_file(self.full_list, self.short_list), ["ccc"],
                         "Списки в прямом порядке не равны")
        self.assertEqual(gfl.get_unique_file(self.short_list, self.full_list), ["ccc"],
                         "Списки в обратном порядке не равны")

    def test_get_unique_file_empty(self):
        self.assertEqual(gfl.get_unique_file(self.full_list, []), self.full_list)

    def test_get_unique_file_equal(self):
        self.assertEqual(gfl.get_unique_file(self.full_list, self.full_list), [])


if __name__ == '__main__':
    unittest.main()

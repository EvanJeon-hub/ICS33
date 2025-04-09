import unittest
from printing import print_values_in_range, print_reversed_list

class Test(unittest.TestCase):
    def test_print_values_in_range(self):
        self.assertEqual(print_values_in_range(1, 6, 2), [1, 3, 5])

    def test_print_reversed_list(self):
        self.assertEqual(print_reversed_list('1234'), ['4321'])


if __name__ == '__main__':
    unittest.main()
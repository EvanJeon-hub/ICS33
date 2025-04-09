import unittest
from printing import print_values_in_range, print_reversed_list
import io
import sys


class TestPrintingFunctions(unittest.TestCase):
    def test_print_values_in_range(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        print_values_in_range(1, 6, 2)
        sys.stdout = sys.__stdout__
        expected_output = "1\n3\n5\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_print_reversed_list_single(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        print_reversed_list(["1234"])
        sys.stdout = sys.__stdout__
        expected_output = "4321\n"
        self.assertEqual(captured_output.getvalue(), expected_output)

    def test_print_reversed_list_multiple(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        print_reversed_list(["1234", "4321"])
        sys.stdout = sys.__stdout__
        expected_output = "4321\n1234\n"
        self.assertEqual(captured_output.getvalue(), expected_output)


if __name__ == '__main__':
    unittest.main()

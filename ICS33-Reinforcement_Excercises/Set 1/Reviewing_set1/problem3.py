# problem3.py
#
# ICS 33 Spring 2025
# Exercise Set 1

from printing import print_reversed_list, print_values_in_range
import io
import contextlib
import unittest

class TestPrinting(unittest.TestCase):
    def test_printing_one_reversed_element_prints_only_the_one_element(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            print_reversed_list(['Boo!'])

        self.assertEqual('!ooB\n', output.getvalue())


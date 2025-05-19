# Evan-Soobin Jeon
# ejeon2@uci.edu

import io
import sys
import unittest
from contextlib import redirect_stdout
from project3 import main

# coverage report -m
# coverage run -m --branch pytest . (branch coverage)

class mainTest(unittest.TestCase):
    """Unit tests for the main function in project3.py."""
    def test_direct_main(self):
        input_code = """\
    LET A 10
    LET B 20
    ADD A B
    PRINT A
    .
    """
        sys.stdin = io.StringIO(input_code)
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        output = f.getvalue().strip()
        self.assertEqual(output, '30')

    def test_direct_main_exception(self):
        input_code = """\
    LET A 10
    LET B 0
    DIV A B
    PRINT A
    .
    """
        sys.stdin = io.StringIO(input_code)
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        output = f.getvalue().strip()
        self.assertIn("Error:", output)

    def test_direct_main_starts_with_dot(self):
        input_code = """\
        .
        """
        sys.stdin = io.StringIO(input_code)
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        output = f.getvalue().strip()
        self.assertEqual(output, "")


if __name__ == "__main__":
    unittest.main()

# Evan-Soobin Jeon
# ejeon2@uci.edu
import unittest
import os
from project4 import main
from contextlib import redirect_stdout
import sys
import io

# coverage report -m
# coverage run -m --branch pytest . (branch coverage)

class TestProject4Main(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_grammar.txt"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write('{\n')
            f.write('Greeting\n')
            f.write('1 Hello [Target]\n')
            f.write('}\n')
            f.write('{\n')
            f.write('Target\n')
            f.write('1 world\n')
            f.write('1 everyone\n')
            f.write('}\n')

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_main_output(self):
        user_input = f"{self.test_file}\n5\nGreeting\n"
        expected_outputs = {"Hello world", "Hello everyone"}

        stdin_backup = sys.stdin
        stdout_capture = io.StringIO()

        try:
            sys.stdin = io.StringIO(user_input)
            with redirect_stdout(stdout_capture):
                main()

            output_lines = stdout_capture.getvalue().strip().split('\n')
            self.assertEqual(len(output_lines), 5)
            for line in output_lines:
                self.assertIn(line, expected_outputs)
        finally:
            sys.stdin = stdin_backup
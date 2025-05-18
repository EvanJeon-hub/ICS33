# test_interpreter.py
# Evan-Soobin Jeon
import unittest
from grin.interpreter import GrinInterpreter
from grin.parsing import GrinParseError

# coverage report -m
# coverage run -m --branch pytest . (branch coverage)
class GrinInterpreterTest(unittest.TestCase):
    """Unit tests for the Grin interpreter."""
    def test_interpret_basic(self):
        lines = [
            "LET A 10",
            "PRINT A"
        ]
        GrinInterpreter.run(lines)
        self.assertEqual(lines, ['LET A 10', 'PRINT A'])

    def test_interpret_empty_program(self):
        lines = []
        GrinInterpreter.run(lines)
        self.assertEqual(lines, [])

    def test_interpret_minimal_end_program(self):
        lines = ['END']
        GrinInterpreter.run(lines)
        self.assertEqual(lines, ['END'])

    def test_interpret_infinite_loop_prevention(self):
        lines = [
            "CHUNK: LET A 3",
        ]
        GrinInterpreter.run(lines)
        self.assertEqual(lines, ['CHUNK: LET A 3'])

    def test_interpret_invalid_statement(self):
        lines = [
            "LET A 10",
            "PRINT A",
            "INVALID STATEMENT"
        ]
        with self.assertRaises(GrinParseError):
            GrinInterpreter.run(lines)

    def test_interpret_valid_statement(self):
        lines = [
            "LET A 10",
            "PRINT A",
            "END"
        ]
        GrinInterpreter.run(lines)
        self.assertEqual(lines, ['LET A 10', 'PRINT A', 'END'])

    def test_interpret_state_running_break(self):
        lines = [
            "LET A 10",
            "GOTO 2",
            "PRINT A",
            "END"
        ]
        GrinInterpreter.run(lines)
        self.assertEqual(lines, ['LET A 10', 'GOTO 2', 'PRINT A', 'END'])


if __name__ == "__main__":
    unittest.main()

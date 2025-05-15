# test_interpreter.py
# Evan-Soobin Jeon
import unittest
from grin.interpreter import GrinInterpreter
from grin.parsing import GrinParseError


class GrinInterpreterTest(unittest.TestCase):

    def test_let_and_print(self):
        lines = [
            "LET A 10",
            "PRINT A"
        ]
        GrinInterpreter.run(lines)



if __name__ == "__main__":
    unittest.main()

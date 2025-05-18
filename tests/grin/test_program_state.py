# Test_program_state.py
# Evan-Soobin Jeon
from grin.program_state import ProgramState
from grin.statement import GrinStatement
import unittest
# coverage report -m
# coverage run -m --branch pytest . (branch coverage)

class TestProgramState(unittest.TestCase):
    """Unit tests for the ProgramState class."""
    def test_initialization(self):
        """Test the initialization of ProgramState."""
        program_state = ProgramState({}, {})
        assert program_state.statements == {}
        assert program_state.labels == {}
        assert program_state.current_line == 0
        assert program_state.variable_stack == {}
        assert program_state.gosub_stack == []
        assert program_state.running is True

    def test_advance(self):
        """Test the advance method."""
        program_state = ProgramState({}, {})
        program_state.current_line = 1
        program_state.advance()
        assert program_state.current_line == 2

    def test_get_current_statement(self):
        """Test getting the current statement."""
        program_state = ProgramState({1: "LET A 10"}, {})
        program_state.current_line = 1
        assert program_state.get_current_statement() == "LET A 10"
        assert program_state.get_current_statement() is not None

    def test_get_label_line(self):
        """Test getting the line number for a label."""
        program_state = ProgramState({}, {"START": 10})
        assert program_state.get_label_line("START") == 10
        assert program_state.get_label_line("END") is None

    def test_set_variable(self):
        """Test setting a variable."""
        program_state = ProgramState({}, {})
        program_state.set_variable("A", 10)
        assert program_state.variable_stack["A"] == 10

    def test_get_variable(self):
        """Test getting a variable."""
        program_state = ProgramState({}, {})
        program_state.set_variable("A", 10)
        assert program_state.get_variable("A") == 10
        assert program_state.get_variable("B") == 0

    def test_push_gosub(self):
        """Test pushing a line number onto the GOSUB stack."""
        program_state = ProgramState({}, {})
        program_state.push_gosub(10)
        assert program_state.gosub_stack == [10]

    def test_pop_gosub(self):
        """Test popping a line number from the GOSUB stack."""
        program_state = ProgramState({}, {})
        program_state.push_gosub(10)
        assert program_state.pop_gosub() == 10
        assert program_state.gosub_stack == []

    def test_pop_gosub_empty_stack(self):
        """Test popping from an empty GOSUB stack."""
        program_state = ProgramState({}, {})
        with self.assertRaises(RuntimeError):
            program_state.pop_gosub()

    def test_evaluate_string_literal(self):
        """Test evaluating a string literal."""
        program_state = ProgramState({}, {})
        result = program_state.evaluate('"Hello"')
        assert result == "Hello"

    def test_evaluate_variable(self):
        """Test evaluating a variable."""
        program_state = ProgramState({}, {})
        program_state.set_variable("A", 10)
        result = program_state.evaluate("A")
        assert result == 10

    def test_evaluate_integer(self):
        """Test evaluating an integer."""
        program_state = ProgramState({}, {})
        result = program_state.evaluate(10)
        assert result == 10

    def test_evaluate_string_literal_quotes(self):
        """string literal detection."""
        program_state = ProgramState({}, {})
        result = program_state.evaluate('"World"')
        assert result == "World"

    def test_evaluate_float(self):
        """Test evaluating a float."""
        program_state = ProgramState({}, {})
        result = program_state.evaluate(10.5)
        assert result == 10.5

    def test_evaluate_invalid_variable(self):
        """Test evaluating an invalid variable."""
        program_state = ProgramState({}, {})
        program_state.set_variable("A", 10)
        result = program_state.evaluate("B")
        assert result == 0

    def test_evaluate_invalid_string(self):
        """Test evaluating an invalid string."""
        program_state = ProgramState({}, {})
        result = program_state.evaluate('"Invalid')
        assert result == 0

    def test_evaluate_invalid_integer(self):
        """Test evaluating an invalid integer."""
        program_state = ProgramState({}, {})
        result = program_state.evaluate("10a")
        assert result == 0

    def test_evaluate_invalid_float(self):
        """Test evaluating an invalid float."""
        program_state = ProgramState({}, {})
        result = program_state.evaluate("10.5a")
        assert result == 0

    def test_evaluate_invalid_expression(self):
        """Test evaluating an invalid expression."""
        program_state = ProgramState({}, {})
        result = program_state.evaluate("10 +")
        assert result == 0

    def test_evaluate_empty_string(self):
        """Test evaluating an empty string."""
        program_state = ProgramState({}, {})
        result = program_state.evaluate("")
        assert result == 0

    def test_evaluate_none(self):
        """Test evaluating None."""
        program_state = ProgramState({}, {})
        result = program_state.evaluate(None)
        assert result == 0

    def test_resolve_target_valid_label(self):
        """Test resolving a valid label."""
        statements = {0: None, 1: None}
        labels = {"start": 1}
        program_state = ProgramState(statements, labels)
        assert program_state.resolve_target('"start"') == 1

    def test_resolve_target_label_not_found(self):
        """Test resolving a label that doesn't exist."""
        program_state = ProgramState({0: None}, {})
        with self.assertRaises(RuntimeError) as e:
            program_state.resolve_target('"missing"')
        assert "Label missing not found" in str(e.exception)

    def test_resolve_target_invalid_label_start_quote_missing(self):
        """Test resolving a label with invalid quote format: missing start quote."""
        program_state = ProgramState({}, {})
        with self.assertRaises(RuntimeError) as e:
            program_state.resolve_target('label"')
        assert "Invalid label format" in str(e.exception)

    def test_resolve_target_invalid_label_end_quote_missing(self):
        """Test resolving a label with invalid quote format: missing end quote."""
        program_state = ProgramState({}, {})
        with self.assertRaises(RuntimeError) as e:
            program_state.resolve_target('"label')
        assert "Invalid label format" in str(e.exception)

    def test_resolve_target_positive_relative_jump(self):
        """Test relative positive jump within bounds."""
        statements = {0: None, 1: None, 2: None}
        program_state = ProgramState(statements, {})
        program_state.current_line = 0
        assert program_state.resolve_target("2") == 2

    def test_resolve_target_negative_relative_jump(self):
        """Test relative negative jump within bounds."""
        statements = {0: None, 1: None, 2: None}
        program_state = ProgramState(statements, {})
        program_state.current_line = 2
        assert program_state.resolve_target("-1") == 1

    def test_resolve_target_negative_jump_invalid_range(self):
        """Test negative jump resulting in line < 0."""
        statements = {0: None, 1: None, 2: None}
        program_state = ProgramState(statements, {})
        program_state.current_line = 0
        with self.assertRaises(RuntimeError) as e:
            program_state.resolve_target("-1")
        assert "Invalid Range" in str(e.exception)

    def test_resolve_target_zero_jump_infinite_loop(self):
        """Test jump with zero (not permitted)."""
        statements = {0: None, 1: None}
        program_state = ProgramState(statements, {})
        program_state.current_line = 1
        with self.assertRaises(RuntimeError) as e:
            program_state.resolve_target("0")
        assert "Infinite Loop is not permitted" in str(e.exception)

    def test_resolve_target_forward_jump_out_of_range(self):
        """Test forward jump that exceeds program length."""
        statements = {0: None, 1: None}
        program_state = ProgramState(statements, {})
        program_state.current_line = 1
        with self.assertRaises(RuntimeError) as e:
            program_state.resolve_target("2")  # 1 + 2 = 3 > len=2
        assert "Out of range" in str(e.exception)

    def test_resolve_target_backward_jump_out_of_range(self):
        """Test backward jump that exceeds program start."""
        statements = {0: None, 1: None, 2: None}
        program_state = ProgramState(statements, {})
        program_state.current_line = 5
        with self.assertRaises(RuntimeError) as e:
            program_state.resolve_target("-1")  # 5 - 1 = 4 > len=3
        assert "Out of range" in str(e.exception)

    def test_resolve_target_invalid_type_returns_none(self):
        """Test resolve_target fallback when given invalid type."""
        statements = {0: None, 1: None}
        program_state = ProgramState(statements, {})
        with self.assertRaises(RuntimeError) as e:
            program_state.resolve_target(object())  # not int or str
        assert "argument must be a string" in str(e.exception)




if __name__ == "__main__":
    unittest.main()
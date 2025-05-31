# test_statement.py
# Evan-Soobin Jeon

from grin.statement import *
from grin.token import GrinToken, GrinTokenKind
from grin.location import GrinLocation
from grin.program_state import ProgramState
from contextlib import redirect_stdout
import io
import unittest

# coverage report -m
# coverage run -m --branch pytest . (branch coverage)


class TestGrinStatement(unittest.TestCase):
    """Test the GrinStatement class and its subclasses."""
    def test_Grinstatement(self):
        statement = GrinStatement()
        with self.assertRaises(NotImplementedError):
            statement.execute(ProgramState([], []))


class TestLetStatement(unittest.TestCase):
    """Test the GrinStatement class and its subclasses."""
    def test_let_statement(self):
        state = ProgramState([], [])
        let_statement = LetStatement("x", "5")
        let_statement.execute(state)
        self.assertEqual(state.get_variable("x"), 5)


class TestPrintStatement(unittest.TestCase):
    """Test the PrintStatement class."""
    def test_print_statement_outputs_variable_value(self):
        state = ProgramState({}, {})
        state.set_variable("A", 10)
        stmt = PrintStatement("A")

        f = io.StringIO()
        with redirect_stdout(f):
            stmt.execute(state)

        output = f.getvalue().strip()
        self.assertEqual(output, "10")

    def test_print_statement_outputs_literal_value(self):
        state = ProgramState({}, {})
        stmt = PrintStatement("42")

        f = io.StringIO()
        with redirect_stdout(f):
            stmt.execute(state)

        output = f.getvalue().strip()
        self.assertEqual(output, "42")


class TestINNUMStatement(unittest.TestCase):
    """Test the INNUMStatement class."""
    def test_INNUM_statement_outputs_numeric_variable(self):
        state = ProgramState({}, {})
        state.set_variable("X", 3.14)
        stmt = INNUMStatement("X")

        f = io.StringIO()
        with redirect_stdout(f):
            stmt.execute(state)

        output = f.getvalue().strip()
        self.assertEqual(output, "3.14")

    def test_INNUM_statement_raises_error_on_non_number(self):
        state = ProgramState({}, {})
        state.set_variable("X", "hello")
        stmt = INNUMStatement("X")

        with self.assertRaises(RuntimeError) as e:
            stmt.execute(state)
        self.assertIn("is not a number", str(e.exception))


class TestINSTRStatement(unittest.TestCase):
    """Test the INNUMStatement class."""
    def test_INSTR_statement_outputs_string_variable(self):
        state = ProgramState({}, {})
        state.set_variable("X", "hello")
        stmt = INSTRStatement("X")

        f = io.StringIO()
        with redirect_stdout(f):
            stmt.execute(state)

        output = f.getvalue().strip()
        self.assertEqual(output, "hello")

    def test_INSTR_statement_raises_error_on_non_string(self):
        state = ProgramState({}, {})
        state.set_variable("X", 42)
        stmt = INSTRStatement("X")

        with self.assertRaises(RuntimeError) as e:
            stmt.execute(state)
        self.assertIn("is not a string", str(e.exception))


class TestArithmeticStatements(unittest.TestCase):
    def test_add_statement(self):
        state = ProgramState({}, {})
        state.set_variable("X", 5)
        add_statement = AddStatement("X", "3")
        add_statement.execute(state)
        self.assertEqual(state.get_variable("X"), 8)

    def test_add_statement_current_value_is_None(self):
        state = ProgramState({}, {})
        state.set_variable("X", None)
        add_statement = AddStatement("X", "3")

        with self.assertRaises(RuntimeError) as e:
            add_statement.execute(state)
        self.assertIn("Variable X not found", str(e.exception))

    def test_add_statement_raises_error_on_invalid_addition(self):
        state = ProgramState({}, {})
        state.set_variable("X", "hello")
        add_statement = AddStatement("X", "3")

        with self.assertRaises(RuntimeError) as e:
            add_statement.execute(state)
        self.assertIn("Invalid addition", str(e.exception))

    def test_subtract_statement(self):
        state = ProgramState({}, {})
        state.set_variable("X", 10)
        subtract_statement = SubtractStatement("X", "3")
        subtract_statement.execute(state)
        self.assertEqual(state.get_variable("X"), 7)

    def test_subtract_statement_current_value_is_None(self):
        state = ProgramState({}, {})
        state.set_variable("X", None)
        subtract_statement = SubtractStatement("X", "3")

        with self.assertRaises(RuntimeError) as e:
            subtract_statement.execute(state)
        self.assertIn("Variable X not found", str(e.exception))

    def test_subtract_statement_raises_error_on_invalid_subtraction(self):
        state = ProgramState({}, {})
        state.set_variable("X", "hello")
        subtract_statement = SubtractStatement("X", "3")

        with self.assertRaises(RuntimeError) as e:
            subtract_statement.execute(state)
        self.assertIn("Invalid subtraction", str(e.exception))

    def test_multiply_statement(self):
        state = ProgramState({}, {})
        state.set_variable("X", 5)
        multiply_statement = MultiplyStatement("X", "3")
        multiply_statement.execute(state)
        self.assertEqual(state.get_variable("X"), 15)

    def test_multiply_statement_current_value_is_None(self):
        state = ProgramState({}, {})
        state.set_variable("X", None)
        multiply_statement = MultiplyStatement("X", "3")

        with self.assertRaises(RuntimeError) as e:
            multiply_statement.execute(state)
        self.assertIn("Variable X not found", str(e.exception))

    def test_multiply_statement_exception(self):
        class Exploding:
            def __mul__(self, other):
                raise ValueError("Boom")

        state = ProgramState({}, {})
        state.set_variable("X", Exploding())
        multiply_statement = MultiplyStatement("X", "3")

        with self.assertRaises(RuntimeError) as e:
            multiply_statement.execute(state)

        assert "Invalid multiplication" in str(e.exception)

    def test_divide_statement(self):
        state = ProgramState({}, {})
        state.set_variable("X", 10)
        divide_statement = DivideStatement("X", "2")
        divide_statement.execute(state)
        self.assertEqual(state.get_variable("X"), 5)

    def test_divide_statement_raises_error_on_invalid_division(self):
        state = ProgramState({}, {})
        state.set_variable("X", "hello")
        divide_statement = DivideStatement("X", "2")

        with self.assertRaises(RuntimeError) as e:
            divide_statement.execute(state)
        self.assertIn("Invalid division", str(e.exception))

    def test_divide_statement_raises_error_on_division_by_zero(self):
        state = ProgramState({}, {})
        state.set_variable("X", 10)
        divide_statement = DivideStatement("X", "0")

        with self.assertRaises(RuntimeError) as e:
            divide_statement.execute(state)
        self.assertIn("Division by zero", str(e.exception))

    def test_divide_statement_raises_error_on_string_division(self):
        state = ProgramState({}, {})
        state.set_variable("X", "hello")
        divide_statement = DivideStatement("X", "2")

        with self.assertRaises(RuntimeError) as e:
            divide_statement.execute(state)
        self.assertIn("Invalid division", str(e.exception))

    def test_divide_statement_raises_error_on_string_division_by_zero(self):
        state = ProgramState({}, {})
        state.set_variable("X", "hello")
        divide_statement = DivideStatement("X", "0")

        with self.assertRaises(RuntimeError) as e:
            divide_statement.execute(state)
        self.assertIn("Division by zero", str(e.exception))

    def test_divide_current_value_is_None(self):
        state = ProgramState({}, {})
        state.set_variable("X", None)
        divide_statement = DivideStatement("X", "2")

        with self.assertRaises(RuntimeError) as e:
            divide_statement.execute(state)
        self.assertIn("Variable X not found", str(e.exception))


class TestGotoStatement(unittest.TestCase):
    """Test the GotoStatement class."""
    def test_goto_unconditional_jump(self):
        state = ProgramState({0: None, 1: None, 2: None}, {})
        state.current_line = 0

        stmt = GotoStatement("2")
        stmt.execute(state)

        self.assertEqual(state.current_line, 2)

    def test_goto_conditional_jump_passes(self):
        state = ProgramState({0: None, 1: None, 2: None}, {})
        state.set_variable("A", 3)
        state.current_line = 0

        stmt = GotoStatement("2", "A", "<", "5")
        stmt.execute(state)

        self.assertEqual(state.current_line, 2)

    def test_goto_conditional_jump_fails(self):
        state = ProgramState({0: None, 1: None, 2: None}, {})
        state.set_variable("A", 7)
        state.current_line = 0

        stmt = GotoStatement("2", "A", "<", "5")
        stmt.execute(state)

        self.assertEqual(state.current_line, 0)

    def test_goto_label_jump(self):
        state = ProgramState({0: None, 1: None, 2: None}, {"start": 2})
        state.current_line = 0

        stmt = GotoStatement('"start"')
        stmt.execute(state)

        self.assertEqual(state.current_line, 2)

    def test_goto_negative_relative_jump(self):
        state = ProgramState({0: None, 1: None, 2: None, 3: None}, {})
        state.current_line = 3

        stmt = GotoStatement("-2")
        stmt.execute(state)

        self.assertEqual(state.current_line, 1)


class TestGosubStatement(unittest.TestCase):
    """Test the GoSubStatement class."""
    def test_gosub_unconditional_jump(self):
        state = ProgramState({0: None, 1: None, 2: None}, {})
        state.current_line = 0

        stmt = GoSubStatement("2")
        stmt.execute(state)

        self.assertEqual(state.current_line, 2)
        self.assertEqual(state.gosub_stack, [1])

    def test_gosub_conditional_jump_passes(self):
        state = ProgramState({0: None, 1: None, 2: None}, {})
        state.set_variable("A", 5)
        state.current_line = 0

        stmt = GoSubStatement("2", "A", "<", "10")
        stmt.execute(state)

        self.assertEqual(state.current_line, 2)
        self.assertEqual(state.gosub_stack, [1])

    def test_gosub_conditional_jump_fails(self):
        state = ProgramState({0: None, 1: None, 2: None}, {})
        state.set_variable("A", 15)
        state.current_line = 0

        stmt = GoSubStatement("2", "A", "<", "10")
        stmt.execute(state)

        self.assertEqual(state.current_line, 0)
        self.assertEqual(state.gosub_stack, [])

    def test_gosub_raises_on_self_jump(self):
        state = ProgramState({0: None, 1: None, 2: None}, {})
        state.current_line = 1

        state.labels = {"self": 1}
        stmt = GoSubStatement('"self"')

        with self.assertRaises(RuntimeError) as e:
            stmt.execute(state)

        self.assertIn("GOSUB cannot jump to the same line", str(e.exception))

    def test_gosub_label_target(self):
        state = ProgramState({0: None, 1: None, 2: None}, {"start": 2})
        state.current_line = 0

        stmt = GoSubStatement('"start"')
        stmt.execute(state)

        self.assertEqual(state.current_line, 2)
        self.assertEqual(state.gosub_stack, [1])


class TestReturnStatement(unittest.TestCase):
    """Test the ReturnStatement class."""
    def test_return_statement_sets_current_line_from_stack(self):
        state = ProgramState({}, {})
        state.push_gosub(5)
        state.current_line = 2

        stmt = ReturnStatement()
        stmt.execute(state)

        self.assertEqual(state.current_line, 5)
        self.assertEqual(state.gosub_stack, [])

    def test_return_statement_raises_error_when_stack_empty(self):
        state = ProgramState({}, {})
        stmt = ReturnStatement()

        with self.assertRaises(RuntimeError) as e:
            stmt.execute(state)

        self.assertIn("No GOSUB stack to return to", str(e.exception))
        self.assertFalse(state.running)


class TestEndStatement(unittest.TestCase):
    """Test the EndStatement class."""
    def test_end_statement_sets_running_false(self):
        state = ProgramState({}, {})
        stmt = EndStatement()

        self.assertTrue(state.running)
        stmt.execute(state)
        self.assertFalse(state.running)


def make_token(kind, text, line=1, column=1):
    return GrinToken(kind=kind, text=text, location=GrinLocation(line, column), value=text)


class TestCreateStatements(unittest.TestCase):
    """Test the create_statements function."""
    def test_create_let_statement(self):
        tokens = [
            [make_token(GrinTokenKind.LET, "LET"),
             make_token(GrinTokenKind.IDENTIFIER, "X"),
             make_token(GrinTokenKind.LITERAL_INTEGER, "5")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, LetStatement)
        self.assertEqual(stmt.variable, "X")
        self.assertEqual(stmt.value, "5")

    def test_create_print_statement(self):
        tokens = [
            [make_token(GrinTokenKind.PRINT, "PRINT"),
             make_token(GrinTokenKind.IDENTIFIER, "X")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, PrintStatement)
        self.assertEqual(stmt.value, "X")

    def test_create_INNUM_statement(self):
        tokens = [
            [make_token(GrinTokenKind.INNUM, "INNUM"),
             make_token(GrinTokenKind.IDENTIFIER, "X")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, INNUMStatement)
        self.assertEqual(stmt.variable, "X")

    def test_create_INSTR_statement(self):
        tokens = [
            [make_token(GrinTokenKind.INSTR, "INSTR"),
             make_token(GrinTokenKind.IDENTIFIER, "X")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, INSTRStatement)
        self.assertEqual(stmt.variable, "X")

    def test_create_add_statement(self):
        tokens = [
            [make_token(GrinTokenKind.ADD, "ADD"),
             make_token(GrinTokenKind.IDENTIFIER, "X"),
             make_token(GrinTokenKind.LITERAL_INTEGER, "5")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, AddStatement)
        self.assertEqual(stmt.variable, "X")
        self.assertEqual(stmt.value, "5")

    def test_create_subtract_statement(self):
        tokens = [
            [make_token(GrinTokenKind.SUB, "SUB"),
             make_token(GrinTokenKind.IDENTIFIER, "X"),
             make_token(GrinTokenKind.LITERAL_INTEGER, "5")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, SubtractStatement)
        self.assertEqual(stmt.variable, "X")
        self.assertEqual(stmt.value, "5")

    def test_create_multiply_statement(self):
        tokens = [
            [make_token(GrinTokenKind.MULT, "MULT"),
             make_token(GrinTokenKind.IDENTIFIER, "X"),
             make_token(GrinTokenKind.LITERAL_INTEGER, "5")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, MultiplyStatement)
        self.assertEqual(stmt.variable, "X")
        self.assertEqual(stmt.value, "5")

    def test_create_divide_statement(self):
        tokens = [
            [make_token(GrinTokenKind.DIV, "DIV"),
             make_token(GrinTokenKind.IDENTIFIER, "X"),
             make_token(GrinTokenKind.LITERAL_INTEGER, "5")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, DivideStatement)
        self.assertEqual(stmt.variable, "X")
        self.assertEqual(stmt.value, "5")

    def test_create_goto_without_condition(self):
        tokens = [
            [make_token(GrinTokenKind.GOTO, "GOTO"),
             make_token(GrinTokenKind.LITERAL_INTEGER, "1")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, GotoStatement)
        self.assertEqual(stmt.target, "1")
        self.assertIsNone(stmt.left_target)
        self.assertIsNone(stmt.relational_operator)
        self.assertIsNone(stmt.right_target)

    def test_create_goto_with_condition(self):
        tokens = [
            [make_token(GrinTokenKind.GOTO, "GOTO"),
             make_token(GrinTokenKind.LITERAL_INTEGER, "1"),
             make_token(GrinTokenKind.IF, "IF"),
             make_token(GrinTokenKind.IDENTIFIER, "X"),
             make_token(GrinTokenKind.LESS_THAN, "<"),
             make_token(GrinTokenKind.LITERAL_INTEGER, "5")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, GotoStatement)
        self.assertEqual(stmt.target, "1")
        self.assertEqual(stmt.left_target, "X")
        self.assertEqual(stmt.relational_operator, "<")
        self.assertEqual(stmt.right_target, "5")

    def test_create_gosub_without_condition(self):
        tokens = [
            [make_token(GrinTokenKind.GOSUB, "GOSUB"),
             make_token(GrinTokenKind.LITERAL_STRING, '"start"')]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, GoSubStatement)
        self.assertEqual(stmt.target, '"start"')
        self.assertIsNone(stmt.left_target)
        self.assertIsNone(stmt.relational_operator)
        self.assertIsNone(stmt.right_target)

    def test_create_gosub_with_condition(self):
        tokens = [
            [make_token(GrinTokenKind.GOSUB, "GOSUB"),
             make_token(GrinTokenKind.LITERAL_STRING, '"start"'),
             make_token(GrinTokenKind.IF, "IF"),
             make_token(GrinTokenKind.IDENTIFIER, "A"),
             make_token(GrinTokenKind.EQUAL, "="),
             make_token(GrinTokenKind.IDENTIFIER, "B")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, GoSubStatement)
        self.assertEqual(stmt.target, '"start"')
        self.assertEqual(stmt.left_target, "A")
        self.assertEqual(stmt.relational_operator, "=")
        self.assertEqual(stmt.right_target, "B")

    def test_create_return_statement(self):
        tokens = [
            [make_token(GrinTokenKind.RETURN, "RETURN")]
        ]

        statements, labels = create_statements(tokens)
        stmt = statements[0]
        self.assertIsInstance(stmt, ReturnStatement)

    def test_raises_on_unknown_token_kind(self):
        class FakeToken:
            @staticmethod
            def kind():
                return "UNKNOWN"

            @staticmethod
            def text():
                return "???"

        tokens = [[FakeToken()]]

        with self.assertRaises(RuntimeError):
            create_statements(tokens)


if __name__ == "__main__":
    unittest.main()

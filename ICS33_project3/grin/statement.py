# Evan-Soobin Jeon
# statement.py
"""
Provides classes to represent statements
in the Grin language. (LET, PRINT, ADD, GOTO, GOSUB, RETURN, END)
each class has a method to execute the statement
"""
from grin.program_state import ProgramState
from grin.token import GrinTokenKind


class GrinStatement:
    def execute(self, state: ProgramState):
        raise NotImplementedError("Subclasses must implement this method.")


class LetStatement(GrinStatement):
    def __init__(self, variable: str, value: str):
        self.variable = variable
        self.value = value

    def execute(self, state: ProgramState):
        value = state.evaluate(self.value)
        state.set_variable(self.variable, value)


class PrintStatement(GrinStatement):
    def __init__(self, value):
        self.value = value

    def execute(self, state: ProgramState):
        value = state.evaluate(self.value)
        print(value)


class INNUMStatement(GrinStatement):
    def __init__(self, variable: str):
        self.variable = variable

    def execute(self, state: ProgramState):
        value = state.get_variable(self.variable)
        if not isinstance(value, (int, float)):
            raise RuntimeError(f"Variable {self.variable} is not a number.")
        print(value)


class INSTRStatement(GrinStatement):
    def __init__(self, variable: str):
        self.variable = variable

    def execute(self, state: ProgramState):
        value = state.get_variable(self.variable)
        if not isinstance(value, str):
            raise RuntimeError(f"Variable {self.variable} is not a string.")
        print(value)


class AddStatement(GrinStatement):
    def __init__(self, variable: str, value: str):
        self.variable = variable
        self.value = value

    def execute(self, state: ProgramState):
        value = state.evaluate(self.value)
        current_value = state.get_variable(self.variable)
        if current_value is None:
            raise RuntimeError(f"Variable {self.variable} not found.")
        try:
            new_value = current_value + value
        except Exception as e:
            raise RuntimeError(f"Invalid addition: {e}")
        state.set_variable(self.variable, new_value)


class SubtractStatement(GrinStatement):
    def __init__(self, variable: str, value: str):
        self.variable = variable
        self.value = value

    def execute(self, state: ProgramState):
        value = state.evaluate(self.value)
        current_value = state.get_variable(self.variable)
        if current_value is None:
            raise RuntimeError(f"Variable {self.variable} not found.")
        try:
            new_value = current_value - value
        except Exception as e:
            raise RuntimeError(f"Invalid subtraction: {e}")
        state.set_variable(self.variable, new_value)


class MultiplyStatement(GrinStatement):
    def __init__(self, variable: str, value: str):
        self.variable = variable
        self.value = value

    def execute(self, state: ProgramState):
        value = state.evaluate(self.value)
        current_value = state.get_variable(self.variable)
        if current_value is None:
            raise RuntimeError(f"Variable {self.variable} not found.")
        try:
            new_value = current_value * value
        except Exception as e:
            raise RuntimeError(f"Invalid multiplication: {e}")
        state.set_variable(self.variable, new_value)


class DivideStatement(GrinStatement):
    def __init__(self, variable: str, value: str):
        self.variable = variable
        self.value = value

    def execute(self, state: ProgramState):
        value = state.evaluate(self.value)
        current_value = state.get_variable(self.variable)
        if current_value is None:
            raise RuntimeError(f"Variable {self.variable} not found.")
        if isinstance(value, (int, float)) and value == 0:
            raise RuntimeError("Division by zero.")
        try:
            if isinstance(current_value, int) and isinstance(value, int):
                new_value = current_value // value
            else:
                new_value = current_value / value
        except Exception as e:
            raise RuntimeError(f"Invalid division: {e}")
        state.set_variable(self.variable, new_value)


class GotoStatement(GrinStatement):
    def __init__(self, target, left_target=None, relational_operator=None, right_target=None):
        self.target = target
        self.left_target = left_target
        self.relational_operator = relational_operator
        self.right_target = right_target

    def execute(self, state: ProgramState):
        if self.left_target is not None:
            left_target = state.evaluate(self.left_target)
            right_target = state.evaluate(self.right_target)
            if not state.evaluate_condition(left_target, right_target, self.relational_operator):
                return
        state.current_line = state.resolve_target(self.target)


class GoSubStatement(GrinStatement):
    def __init__(self, target, left_target=None, relational_operator=None, right_target=None):
        self.target = target
        self.left_target = left_target
        self.relational_operator = relational_operator
        self.right_target = right_target

    def execute(self, state: ProgramState):
        if self.left_target is not None:
            left_target = state.evaluate(self.left_target)
            right_target = state.evaluate(self.right_target)
            if not state.evaluate_condition(left_target, right_target, self.relational_operator):
                return
        resolved_line = state.resolve_target(self.target)
        if resolved_line == state.current_line:
            raise RuntimeError("GOSUB cannot jump to the same line it is on.")
        return_line = state.current_line + 1
        state.push_gosub(return_line)
        state.current_line = resolved_line


class ReturnStatement(GrinStatement):
   def execute(self, state: ProgramState):
        try:
            return_line = state.pop_gosub()
            state.current_line = return_line
        except RuntimeError:
            state.running = False
            raise RuntimeError("No GOSUB stack to return to.")


class EndStatement(GrinStatement):
    def execute(self, state: ProgramState):
        state.running = False


def create_statements(token_lines: list[list]) -> tuple[dict[int, GrinStatement], dict[str, int]]:
    statements = {}
    labels = {}

    for line_number, tokens in enumerate(token_lines):
        index = 0

        if tokens[index].kind() == GrinTokenKind.IDENTIFIER and tokens[index + 1].kind() == GrinTokenKind.COLON:
            label = tokens[index].text()
            labels[label] = line_number
            index += 2

        kind = tokens[index].kind()

        if kind == GrinTokenKind.LET:
            var = tokens[index + 1].text()
            val = tokens[index + 2].text()
            statement = LetStatement(var, val)

        elif kind == GrinTokenKind.PRINT:
            val = tokens[index + 1].text()
            statement = PrintStatement(val)

        elif kind == GrinTokenKind.INNUM:
            var = tokens[index + 1].text()
            statement = INNUMStatement(var)

        elif kind == GrinTokenKind.INSTR:
            var = tokens[index + 1].text()
            statement = INSTRStatement(var)

        elif kind == GrinTokenKind.ADD:
            var = tokens[index + 1].text()
            val = tokens[index + 2].text()
            statement = AddStatement(var, val)

        elif kind == GrinTokenKind.SUB:
            var = tokens[index + 1].text()
            val = tokens[index + 2].text()
            statement = SubtractStatement(var, val)

        elif kind == GrinTokenKind.MULT:
            var = tokens[index + 1].text()
            val = tokens[index + 2].text()
            statement = MultiplyStatement(var, val)

        elif kind == GrinTokenKind.DIV:
            var = tokens[index + 1].text()
            val = tokens[index + 2].text()
            statement = DivideStatement(var, val)

        elif kind == GrinTokenKind.GOTO:
            target = tokens[index + 1].text()
            if len(tokens) > index + 2 and tokens[index + 2].kind() == GrinTokenKind.IF:
                left_target = tokens[index + 3].text()
                relational_operator = tokens[index + 4].text()
                right_target = tokens[index + 5].text()
                statement = GotoStatement(target, left_target, relational_operator, right_target)
            else:
                statement = GotoStatement(target)

        elif kind == GrinTokenKind.GOSUB:
            target = tokens[index + 1].text()
            if len(tokens) > index + 2 and tokens[index + 2].kind() == GrinTokenKind.IF:
                left_target = tokens[index + 3].text()
                relational_operator = tokens[index + 4].text()
                right_target = tokens[index + 5].text()
                statement = GoSubStatement(target, left_target, relational_operator, right_target)
            else:
                statement = GoSubStatement(target)

        elif kind == GrinTokenKind.RETURN:
            statement = ReturnStatement()

        elif kind == GrinTokenKind.END:
            statement = EndStatement()

        else:
            raise RuntimeError

        statements[line_number] = statement
        # Debugging
        # print(statements, labels)

    return statements, labels





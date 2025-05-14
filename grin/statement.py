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
        print(value)


class INSTRStatement(GrinStatement):
    def __init__(self, variable: str):
        self.variable = variable

    def execute(self, state: ProgramState):
        value = state.get_variable(self.variable)
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
        new_value = current_value + value
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
        new_value = current_value - value
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
        new_value = current_value * value
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
        if value == 0:
            raise RuntimeError("Division by zero.")
        if isinstance(current_value, int) and isinstance(value, int):
            new_value = current_value // value
        else:
            new_value = current_value / value
        state.set_variable(self.variable, new_value)


class GotoStatement(GrinStatement):
    def __init__(self, target):
        self.target = target

    def execute(self, state: ProgramState):
        state.current_line = state.resolve_target(self.target)


class GoSubStatement(GrinStatement):
    def __init__(self, target):
        self.target = target

    def execute(self, state: ProgramState):
        return_line = state.current_line + 1
        state.push_gosub(return_line)
        state.current_line = state.resolve_target(self.target)


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
            statement = GotoStatement(target)

        elif kind == GrinTokenKind.GOSUB:
            target = tokens[index + 1].text()
            statement = GoSubStatement(target)

        elif kind == GrinTokenKind.RETURN:
            statement = ReturnStatement()

        elif kind == GrinTokenKind.END:
            statement = EndStatement()

        else:
            raise RuntimeError

        statements[line_number] = statement


    return statements, labels





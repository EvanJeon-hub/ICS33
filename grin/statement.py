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
        # Assuming a value is a number or a variable
        value = state.evaluate(self.value)
        state.set_variable(self.variable, value)


class PrintStatement(GrinStatement):
    def __init__(self, value):
        self.value = value

    def execute(self, state: ProgramState):
        value = state.evaluate(self.value)
        print(value)


class AddStatement(GrinStatement):
    def __init__(self, variable: str, value: str):
        self.variable = variable
        self.value = value

    def execute(self, state: ProgramState):
        pass


class GotoStatement(GrinStatement):
    def __init__(self, target):
        self.target = target

    def execute(self, state: ProgramState):
        pass


class GoSubStatement(GrinStatement):
    def __init__(self, target):
        self.target = target

    def execute(self, state: ProgramState):
        pass


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

        statements[line_number] = statement

    return statements, labels





# Evan-Soobin Jeon
# statement.py
"""
Provides classes to represent statements
in the Grin language. (LET, PRINT, GOTO, GOSUB, RETURN)
each class has a method to execute the statement
"""
class GrinStatement:
    def execute(self, program_state: dict):
        raise NotImplementedError("Subclasses must implement this method.")


class LetStatement(GrinStatement):
    def __init__(self, variable: str, expression: str) -> None:
        self.variable = variable
        self.expression = expression

    def execute(self, context: dict) -> None:
        pass


class PrintStatement(GrinStatement):
    def __init__(self, expression: str) -> None:
        self.expression = expression

    def execute(self, context: dict) -> None:
        pass


class GotoStatement(GrinStatement):
    def __init__(self, line_number: int) -> None:
        self.line_number = line_number

    def execute(self, context: dict) -> None:
        pass


class GoSubStatement(GrinStatement):
    def __init__(self, line_number: int) -> None:
        self.line_number = line_number

    def execute(self, context: dict) -> None:
        pass


class ReturnStatement(GrinStatement):
    def __init__(self) -> None:
        pass

    def execute(self, context: dict) -> None:
        pass








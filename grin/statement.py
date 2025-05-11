# Evan-Soobin Jeon
# statement.py
"""
Provides classes to represent statements
in the Grin language. (LET, PRINT, ADD, GOTO, GOSUB, RETURN, END)
each class has a method to execute the statement
"""
from grin.program_state import ProgramState

class GrinStatement:
    def execute(self, state: ProgramState):
        raise NotImplementedError("Subclasses must implement this method.")


class LetStatement(GrinStatement):
    def __init__(self, variable: str, value: str):
        self.variable = variable
        self.value = value

    def execute(self, state: ProgramState):
        pass


class PrintStatement(GrinStatement):
    def __init__(self, value):
        self.value = value

    def execute(self, state: ProgramState):
        print(self.value)


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
        pass


class EndStatement(GrinStatement):
    def execute(self, state: ProgramState):
        pass






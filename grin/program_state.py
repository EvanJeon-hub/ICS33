# Evan-Soobin Jeon
# program_state.py
"""
Stores stack of variables and GOSUB stack. (last-in-first-out)
Manages the program state
and provides methods to manipulate it.
"""
from grin.statement import GrinStatement


class ProgramState:
    """
    Represents the state of the program.
    Stores the current line number, variable stack, and GOSUB stack.
    """
    def __init__(self, statements: dict[int, GrinStatement], labels: dict[str, int]):
        self.statements = statements
        self.labels = labels
        self.current_line = 0
        self.variable_stack = {}
        self.gosub_stack = []
        self.running = True

    def advance(self):
        """ Advances the current line to the next statement. """
        self.current_line += 1
        if self.current_line not in self.statements:
            self.running = False

    def get_current_statement(self) -> GrinStatement:
        """ Returns the current statement.  """
        return self.statements.get(self.current_line, None)

    def set_variable(self, name: str, value):
        """Sets the value of a variable."""
        self.variable_stack[name] = value

    def get_variable(self, name: str):
        """Gets the value of a variable. """
        return self.variable_stack.get(name, None)

    def push_gosub(self, line_number: int):
        """ Pushes a line number onto the GOSUB stack."""
        self.gosub_stack.append(line_number)

    def pop_gosub(self) -> int:
        """Pops a line number from the GOSUB stack. (last-in-first-out)"""
        return self.gosub_stack.pop() if self.gosub_stack else None

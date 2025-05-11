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
        if not self.gosub_stack:
            raise RuntimeError("No GOSUB stack")
        return self.gosub_stack.pop() if self.gosub_stack else None

    def evaluate(self, value):
        """ Evaluates a token is variable or integer. """
        if isinstance(value, str) and value.isidentifier():
            return self.get_variable(value)
        return value

    # Handles the GOTO and GOSUB statements
    def resolve_target(self, target):
        """ Resolves a target to a line number. """

        # check if a target is a name
        if isinstance(target, str) and target.isidentifier():
            return self.get_variable(target)

        # check if a target is a label
        if isinstance(target, str):
            if target not in self.labels:
                raise RuntimeError(f"Label {target} not found")
            return self.labels[target]

        # check if a target is out of the limit
        if isinstance(target, int):
            dataset = self.current_line + target
            if dataset < 0 or dataset >= len(self.statements) + 1:
                raise RuntimeError(f"Jump to invalid line: {dataset}")
            return dataset

        raise RuntimeError(f"Label {target} not found")

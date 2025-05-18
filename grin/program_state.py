# Evan-Soobin Jeon
# program_state.py
"""
Stores stack of variables and GOSUB stack. (last-in-first-out)
Manages the program state
and provides methods to manipulate it.
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from grin.statement import GrinStatement

class ProgramState:
    """
    Represents the state of the program.
    Stores the current line number, variable stack, and GOSUB stack.
    """
    def __init__(self, statements: dict[int, "GrinStatement"], labels: dict[str, int]):
        self.statements = statements
        self.labels = labels
        self.current_line = 0
        self.variable_stack = {}
        self.gosub_stack = []
        self.running = True

    def advance(self):
        """ Advances the current line to the next statement. """
        self.current_line += 1

    def get_current_statement(self):
        """ Returns the current statement - used for interpreter"""
        return self.statements.get(self.current_line, None)

    def get_label_line(self, label_name: str):
        """Returns the line number for a given label name."""
        return self.labels.get(label_name)

    def set_variable(self, name: str, value):
        """Sets the value of a variable."""
        self.variable_stack[name] = value

    def get_variable(self, name: str):
        """Gets the value of a variable. """
        return self.variable_stack.get(name, 0)

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
        try:
            # Handle String Literal
            if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                return value[1:-1]

            # if a value is string, convert to int or float
            if isinstance(value, str):
                return float(value) if '.' in value else int(value)

            # if a value is already int or float, return it
            if isinstance(value, (int, float)):
                return value

            return self.get_variable(value)

        except ValueError:
            # Handle Variable
            return self.get_variable(value)

    def resolve_target(self, target):
        """ Resolves a target to a line number. """
        try:
            # Handle String Literal (GOTO/GOSUB "label")
            if isinstance(target, str):
                if target.startswith('"') and target.endswith('"'):
                    label = target[1:-1]
                    line = self.get_label_line(label)

                    if line is None:
                        raise ValueError(f"Label {label} not found")

                    return line

                elif not target.lstrip('-').isdigit():
                    raise ValueError("Invalid label format")

            # Handle Integer (GOTO/GOSUB 3)
            var = int(target)

            if var > 0:
                if self.current_line + var > len(self.statements):
                    raise ValueError("Out of range")
                return self.current_line + var

            if var < 0:
                if self.current_line + var > len(self.statements):
                    raise ValueError("Out of range")
                if self.current_line + var < 0:
                    raise ValueError("Invalid Range")
                return self.current_line + var

            if var == 0:
                raise ValueError("Infinite Loop is not permitted")

        except Exception as e:
            raise RuntimeError(e)

        return None

    @staticmethod
    def evaluate_condition(left_target, right_target, relational_operator: str) -> bool:
        """ Evaluates a condition based on the relational operator. """
        allowed = (int, float)

        if isinstance(left_target, allowed) and isinstance(right_target, allowed):
            pass

        elif isinstance(left_target, str) and isinstance(right_target, str):
            pass

        else:
            raise RuntimeError("Invalid types for comparison")

        if relational_operator == "<":
            return left_target < right_target

        elif relational_operator == "<=":
            return left_target <= right_target

        elif relational_operator == ">":
            return left_target > right_target

        elif relational_operator == ">=":
            return left_target >= right_target

        elif relational_operator == "=":
            return left_target == right_target

        elif relational_operator == "<>":
            return left_target != right_target

        else:
            raise RuntimeError(f"Invalid relational operator: {relational_operator}")

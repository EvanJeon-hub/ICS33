# Evan-Soobin Jeon
# interpreter.py
"""
Includes the Grin interpreter, which executes the Grin program.
"""
from typing import Iterable
from grin.program_state import ProgramState
from grin.statement import create_statements
from grin.parsing import parse


class GrinInterpreter(object):
    """The Grin interpreter, which executes the Grin program."""
    @staticmethod
    def run(lines: Iterable[str]):

        token_lines = list(parse(lines))
        statements, labels = create_statements(token_lines)
        state = ProgramState(statements, labels)

        while state.running is True:
            statement = state.get_current_statement()

            if statement is None:
                break

            statement.execute(state)

            if state.get_current_statement() == statement:
                state.advance()

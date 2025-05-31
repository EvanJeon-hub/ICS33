"""A module for defining terminal and variable symbols in a grammar."""
# Evan-Soobin Jeon
# ejeon2@uci.edu

class TerminalSymbol:
    """Represents a terminal symbol in a grammar."""
    def __init__(self, terminal: str):
        self.terminal = terminal

    def find(self, _):
        yield self.terminal


class VariableSymbol:
    def __init__(self, variable: str):
        self.variable = variable

    def find(self, grammar):
        rule = grammar.get_rule(self.variable)
        yield from rule.generate(grammar)


def parse_symbol(symbol: str):
    """
    Parses a string symbol into a TerminalSymbol or VariableSymbol.
    example1: "[A]" -> VariableSymbol("A")
    example2: "a" -> TerminalSymbol("a")
    """
    if symbol.startswith("[") and symbol.endswith("]"):
        return VariableSymbol(symbol[1:-1])
    else:
        return TerminalSymbol(symbol)

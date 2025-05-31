# Evan-Soobin Jeon
# ejeon2@uci.edu
import unittest
from grammar_symbol import TerminalSymbol, VariableSymbol, parse_symbol
from grammar_parser import Grammar, Rule, Option

# coverage report -m
# coverage run -m --branch pytest . (branch coverage)

class TestGrammarSymbol(unittest.TestCase):
    """Unit tests for grammar symbols."""
    def test_terminal_symbol(self):
        terminal = TerminalSymbol("a")
        self.assertEqual(list(terminal.find(None)), ["a"])

    def test_terminal_symbol_fail(self):
        terminal = TerminalSymbol("b")
        self.assertNotEqual(list(terminal.find(None)), ["a"])

    def test_variable_symbol(self):
        # Grammar: A → hello
        rule = Rule("A", [Option(1, ["hello"])])
        grammar = Grammar()
        grammar.add_rule(rule)

        variable_symbol = VariableSymbol("A")
        result = list(variable_symbol.find(grammar))

        self.assertEqual(result, ["hello"])

    def test_variable_symbol_fail(self):
        # Grammar: A → hello
        rule = Rule("A", [Option(1, ["hello"])])
        grammar = Grammar()
        grammar.add_rule(rule)

        variable_symbol = VariableSymbol("A")
        result = list(variable_symbol.find(grammar))

        self.assertNotEqual(result, ["world"])

    def test_parse_terminal_symbol(self):
        terminal = parse_symbol("a")
        self.assertIsInstance(terminal, TerminalSymbol)
        self.assertEqual(terminal.terminal, "a")

    def test_parse_terminal_symbol_fail(self):
        terminal = parse_symbol("b")
        self.assertIsInstance(terminal, TerminalSymbol)
        self.assertNotEqual(terminal.terminal, "a")

    def test_parse_variable_symbol(self):
        variable = parse_symbol("[A]")
        self.assertIsInstance(variable, VariableSymbol)
        self.assertEqual(variable.variable, "A")

    def test_parse_variable_symbol_fail(self):
        variable = parse_symbol("[B]")
        self.assertIsInstance(variable, VariableSymbol)
        self.assertNotEqual(variable.variable, "A")

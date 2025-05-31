# Evan-Soobin Jeon
# ejeon2@uci.edu
import unittest
from grammar_parser import Grammar, Rule, Option
import os

# coverage report -m
# coverage run -m --branch pytest . (branch coverage)

class TestGrammarParser(unittest.TestCase):
    """ Test class for Grammar Parser"""
    def setUp(self):
        self.test_file = "test_grammar.txt"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write('{\n')
            f.write('S\n')
            f.write('1 hello [A]\n')
            f.write('}\n')
            f.write('{\n')
            f.write('A\n')
            f.write('2 world\n')
            f.write('1 everyone\n')
            f.write('}\n')

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_generate_file_parses_correctly(self):
        grammar = Grammar.generate_file(self.test_file)

        self.assertIn('S', grammar._rules)
        self.assertIn('A', grammar._rules)

        rule_s = grammar.get_rule('S')
        rule_a = grammar.get_rule('A')

        self.assertEqual(rule_s.variable, 'S')
        self.assertEqual(len(rule_s.options), 1)
        self.assertEqual(rule_s.options[0].chance, 1)
        self.assertEqual(len(rule_s.options[0].symbols), 2)

        self.assertEqual(rule_a.variable, 'A')
        self.assertEqual(len(rule_a.options), 2)
        self.assertEqual(rule_a.options[0].chance, 2)
        self.assertEqual(rule_a.options[1].chance, 1)

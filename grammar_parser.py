# Evan-Soobin Jeon
# ejeon2@uci.edu
import random
from grammar_symbol import parse_symbol

class Option:
    def __init__(self, chance, symbols):
        self.chance = chance
        self.symbols = [parse_symbol(s) for s in symbols]

    def generate(self, grammar):
        for symbol in self.symbols:
            yield from symbol.find(grammar)


class Rule:
    def __init__(self, variable, options):
        self.variable = variable
        self.options = options

    def generate(self, grammar):
        weights = [option.chance for option in self.options]
        selected_option = random.choices(self.options, weights=weights, k=1)[0]
        return selected_option.generate(grammar)

class Grammar:
    def __init__(self):
        self._rules = {}

    def add_rule(self, rule):
        self._rules[rule.variable] = rule

    def get_rule(self, variable):
        return self._rules[variable]


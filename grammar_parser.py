# Evan-Soobin Jeon
# ejeon2@uci.edu
import random
from grammar_symbol import parse_symbol
"""
Rule: HowIsBoo
{
HowIsBoo - Start Variable
1 Boo is [Adjective] today - Option
}

Rule: Adjective
{
Adjective - Variable
3 happy    - Options
3 perfect
1 relaxing
1 fulfilled
2 excited
}
"""

class Rule:
    def __init__(self, variable, options):
        self.variable = variable
        self.options = options

    def generate(self, grammar):
        weights = [option.chance for option in self.options]
        selected_option = random.choices(self.options, weights=weights, k=1)[0]
        return selected_option.generate(grammar)


class Option:
    def __init__(self, chance, symbols):
        self.chance = chance
        self.symbols = [parse_symbol(s) for s in symbols]

    def generate(self, grammar):
        for symbol in self.symbols:
            yield from symbol.find(grammar)


class Grammar:
    def __init__(self):
        self._rules = {}

    def add_rule(self, rule):
        self._rules[rule.variable] = rule

    def get_rule(self, variable):
        return self._rules[variable]

    @staticmethod
    def generate_file(path):
        grammar = Grammar()
        with open(path, encoding = 'utf-8') as file:
            lines = [line.strip() for line in file if line.strip()]

            i = 0
            while i < len(lines):
                if lines[i] == "{":
                    i += 1
                    variable = lines[i]
                    i += 1
                    options = []
                    while lines[i] != "}":
                        parts = lines[i].split()
                        chance = int(parts[0])
                        symbols = parts[1:]
                        options.append(Option(chance, symbols))
                        i += 1
                    grammar.add_rule(Rule(variable, options))
                i += 1
        return grammar



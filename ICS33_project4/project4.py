# project4.py
#
# ICS 33 Spring 2025
# Project 4: Still Looking for Something
from grammar_parser import Grammar, Rule, Option
from grammar_symbol import VariableSymbol

def main():
    grammar_file = input().strip()
    count = int(input().strip())
    start_variable = input().strip()

    grammar = Grammar.generate_file(grammar_file)
    start_symbol = VariableSymbol(start_variable)

    for _ in range(count):
        generated_text = ' '.join(start_symbol.find(grammar))
        print(generated_text)


if __name__ == '__main__':
    main()

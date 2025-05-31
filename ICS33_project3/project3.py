# project3.py
#
# ICS 33 Spring 2025
# Project 3: Why Not Smile?
#
# The main module that executes your Grin interpreter.
#
# WHAT YOU NEED TO DO: You'll need to implement the outermost shell of your
# program here, but consider how you can keep this part as simple as possible,
# offloading as much of the complexity as you can into additional modules in
# the 'grin' package, isolated in a way that allows you to unit test them.
import sys
from grin.interpreter import GrinInterpreter
from grin.program_state import ProgramState

def main() -> None:
    lines = []

    try:
        for line in sys.stdin:
            line = line.rstrip("\n")
            lines.append(line)

            if line.startswith("."):
                break

        interpreter = GrinInterpreter()
        interpreter.run(lines)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()

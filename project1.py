"""project1.py"""
# Evan-Soobin Jeon
# ejeon2@uci.edu

from pathlib import Path
from inputs import input_command
from alerts import Alert
from cancellations import Cancellation


def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input().strip())

def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()

    if not input_file_path.exists():
        print("FILE NOT FOUND")
        return

    devices, events, simulation_time = input_command(input_file_path)
    queue = []

    pass

if __name__ == '__main__':
    main()

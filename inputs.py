"""inputs.py"""
# Evan-Soobin Jeon
# ejeon2@uci.edu
import shlex
from alerts import Alert
from cancellations import Cancellation
from devices import Device


def input_command(file_path):
    """Reads the input file and processes commands."""
    devices = {}
    events = []
    simulation_time = None

    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            tokens = shlex.split(file_path)
            command = tokens[0]

        if command == "LENGTH":
            """characteristic 1"""

        elif command == "DEVICE":
            """characteristic 2"""

        elif command == "PROPAGATE":
            """characteristic 3"""

        elif command == "ALERT":
            """characteristic 4"""

        elif command == "CANCEL":
            """characteristic 5"""

        return devices, events, simulation_time








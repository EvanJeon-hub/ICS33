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
    simulation_time = int

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            tokens = shlex.split(line)
            command = tokens[0]

            if command == "LENGTH":
                simulation_time = int(tokens[1])

            elif command == "DEVICE":
                device_id = int(tokens[1])
                devices[device_id] = Device(device_id)

            elif command == "PROPAGATE":
                sender_id = int(tokens[1])
                receiver_id = int(tokens[2])
                delay = tokens[3]
                events.append(("PROPAGATE", sender_id, receiver_id, delay))

            elif command == "ALERT":
                device_id = int(tokens[1])
                description = tokens[2]
                time = int(tokens[3])
                alert = Alert(device_id, description, time)
                events.append(("ALERT", alert))

            elif command == "CANCEL":
                device_id = int(tokens[1])
                description = tokens[2]
                time = int(tokens[3])
                cancellation = Cancellation(device_id, description, time)
                events.append(("CANCEL", cancellation))

    return devices, events, simulation_time

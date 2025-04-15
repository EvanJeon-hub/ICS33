"""project1.py"""
# Evan-Soobin Jeon
# ejeon2@uci.edu

from pathlib import Path
from inputs import input_command
from alerts import Alert


def _read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input().strip())

def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = _read_input_file_path()

    if not input_file_path.exists():
        print("FILE NOT FOUND")
        return

    devices, events, simulation_time = input_command(str(input_file_path))
    queue = []

    for event in events:
        if event[0] == "PROPAGATE":
            pass

        elif event[0] == "ALERT":
            pass

        elif event[0] == "CANCEL":
            pass

        queue.sort(key=lambda x: x[0])

    # Run Simulation
    while queue:
        current_time, event_type, device, event = queue.pop(0)

        if current_time >= simulation_time:
            break

        if event_type == "alert":
            device.receive_alert(event, current_time, queue)

        elif event_type == "cancellation":
            device.receive_cancellation(event, current_time, queue)

        queue.sort(key=lambda x: x[0])

    print(Alert.create_end_message(simulation_time))

if __name__ == '__main__':
    main()

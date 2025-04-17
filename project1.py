"""project1.py"""
# Evan-Soobin Jeon
# ejeon2@uci.edu

from pathlib import Path
from inputs import input_command
from alerts import Alert


def read_input_file_path() -> Path:
    """Reads the input file path from the standard input"""
    return Path(input().strip())


def main() -> None:
    """Runs the simulation program in its entirety"""
    input_file_path = read_input_file_path()

    if not input_file_path.exists():
        print("FILE NOT FOUND")
        return

    devices, events, simulation_time = input_command(str(input_file_path))
    queue = []

    for event in events:
        if event[0] == "PROPAGATE":
            _, sender_id, receiver_id, delay = event
            sender = devices[sender_id]
            receiver = devices[receiver_id]
            sender.add_propagation_set(receiver, int(delay))

        if event[0] == "ALERT":
            _, alert = event
            device = devices[alert.device_id]
            queue.append((alert.time, "alert", device, alert))

        if event[0] == "CANCEL":
            _, cancellation = event
            device = devices[cancellation.device_id]
            queue.append(
                (cancellation.time, "cancellation", device, cancellation)
            )

        queue.sort(key=lambda x: (x[0], 0 if x[1] == "alert" else 1))

    # Run Simulation
    while queue:
        current_time, event_type, device, event = queue.pop(0)

        if event_type == "alert":
            device.receive_alert(event, current_time, queue)

        if event_type == "cancellation":
            device.receive_cancellation(event, current_time, queue)

        queue.sort(key=lambda x: (x[0], 0 if x[1] == "alert" else 1))

    print(Alert.create_end_message(simulation_time))


if __name__ == '__main__':
    main()

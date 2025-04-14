# devices.py
# Evan-Soobin Jeon
# ejeon2@uci.edu

from alerts import Alert
from cancellations import Cancellation
from inputs import input_command

class Device:
    def __init__(self, device_id):
        if device_id < 0:
            raise ValueError("device_id must be a non-negative integer.")
        self.device_id = device_id
        self.notified_alerts = set()
        self.canceled_alerts = set()

    def __enter__(self):
        print(f"Device {self.device_id} is leaving simulation.")
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        print(f"Device {self.ID} is leaving simulation.")

    def send_message(self, message):
        pass

    def receive_message(self, message):
        pass



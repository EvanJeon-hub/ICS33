# devices.py
# Evan-Soobin Jeon
# ejeon2@uci.edu

from alerts import Alert
from cancellations import Cancellation


class Device:
    def __init__(self, device_id):
        if device_id < 0:
            raise ValueError("device_id must be a non-negative integer.")
        self.device_id = device_id
        self.notified_alerts = set()
        self.canceled_alerts = set()
        self.propagation_set = {}

    def add_propagation_set(self, target_device, delay):
        if target_device < 0 or delay < 0:
            raise ValueError("target_device and delay must be non-negative integers.")
        self.propagation_set[target_device] = delay

    def receive_alert(self, alert: Alert, current_time: int, queue: list):
        pass

    def receive_cancellation(self, cancel: Cancellation, current_time: int, queue: list):
        pass

    # After raising an alert, the device should be ready to receive another alert
    def raise_alert(self, description, time, queue):
        alert = Alert(self.device_id, description, time)
        self.receive_alert(alert, time, queue)

    # After cancel an alert, the device should be ready to cancel another alert
    def cancel_alert(self, description, time, queue):
        cancellation = Cancellation(self.device_id, description, time)
        self.receive_cancellation(cancellation, time, queue)




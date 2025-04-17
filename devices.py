"""devices.py"""
# Evan-Soobin Jeon
# ejeon2@uci.edu

from alerts import Alert
from cancellations import Cancellation


class Device:
    """Device class that represents a device in the system."""
    def __init__(self, device_id):
        """__init__ method to initialize the device with a device_id."""
        if device_id < 0:
            raise ValueError("device_id must be a non-negative integer.")
        self.device_id = device_id
        self.notified_alerts = set()
        self.canceled_alerts = set()
        self.propagation_set = {}

    def __eq__(self, other):
        """Equality check for devices based on device_id."""
        return isinstance(other, Device) and self.device_id == other.device_id

    def __hash__(self):
        """Hash function for devices based on device_id."""
        return hash(self.device_id)

    def add_propagation_set(self, target_device, delay):
        """Add a target device and its delay to the propagation set."""
        if not isinstance(target_device, Device):
            raise TypeError("target_device must be a Device instance.")
        if target_device.device_id < 0 or delay < 0:
            raise ValueError("must be non-negative integers.")
        self.propagation_set[target_device] = delay

    def receive_alert(self, alert: Alert, current_time: int, queue: list):
        """""Receive an alert and propagate it to other devices."""
        # Check if the alert has already been notified
        if (alert.description, alert.device_id, self.device_id, alert.time) in self.notified_alerts:
            return

        # Check if the alert is from a different device
        if self.device_id != alert.device_id:
            print(alert.create_receive_alert_message(
                self.device_id, alert.device_id, current_time
            ))

        # Check if the alert is already canceled
        for desc, canceled_id, receiver_id, cancel_time in self.canceled_alerts:
            if desc == alert.description and cancel_time < current_time:
                return

        # Add the alert to the notified alerts
        self.notified_alerts.add((alert.description, alert.device_id, self.device_id, alert.time))

        # Propagate the alert to other devices
        for target_device, delay in self.propagation_set.items():
            propagation_time = current_time + delay
            new_cancel = Alert(self.device_id, alert.description, propagation_time)
            print(alert.create_send_alert_message(
                self.device_id, target_device.device_id, current_time
            ))
            queue.append((propagation_time, "alert", target_device, new_cancel))

    def receive_cancellation(
            self, cancel: Cancellation, current_time: int, queue: list):
        """Receive a cancellation and propagate it to other devices."""
        # Check if the cancellation has already been notified
        if (cancel.description, cancel.device_id, self.device_id, cancel.time) in self.canceled_alerts:
            return

        # Check if the cancellation is from a different device
        if self.device_id != cancel.device_id:
            print(cancel.create_receive_cancel_message(
                self.device_id, cancel.device_id, current_time
            ))

        # Check if the cancellation is already notified
        for desc, canceled_id, receiver_id, cancel_time in self.canceled_alerts:
            if desc == cancel.description and cancel_time < current_time:
                return

        # Add the cancellation to the notified cancellations
        self.canceled_alerts.add((cancel.description, cancel.device_id, self.device_id, cancel.time))

        # Propagate the cancellation to other devices
        for target_device, delay in self.propagation_set.items():
            propagation_time = current_time + delay
            new_cancel = Cancellation(self.device_id, cancel.description, propagation_time)
            print(cancel.create_send_cancel_message(
                self.device_id, target_device.device_id, current_time
            ))
            queue.append((propagation_time, "cancellation", target_device, new_cancel))

    def raise_alert(self, description, time, queue):
        """Raise an alert and propagate it to other devices."""
        alert = Alert(self.device_id, description, time)
        self.receive_alert(alert, time, queue)

    def cancel_alert(self, description, time, queue):
        """Cancel an alert and propagate it to other devices."""
        cancellation = Cancellation(self.device_id, description, time)
        self.receive_cancellation(cancellation, time, queue)

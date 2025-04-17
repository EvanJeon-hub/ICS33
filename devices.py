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
        # Adds the device and delay time to the propagation_set dictionary
        self.propagation_set[target_device] = delay

    def receive_alert(self, alert: Alert, current_time: int, queue: list):
        """""Receive an alert and propagate it to other devices."""

        # If this alert has been canceled BEFORE this current_time, do not propagate
        for desc, canceled_id, receiver_id, cancel_time in self.canceled_alerts:
            if desc == alert.description and cancel_time < current_time:
                return

        # Check if the alert is already recorded
        if (alert.description, alert.device_id, self.device_id, alert.time) in self.notified_alerts:
            return

        # record the alert status
        self.notified_alerts.add((alert.description, alert.device_id, self.device_id, alert.time))

        if self.device_id == alert.device_id:
            for target_device, delay in self.propagation_set.items():
                propagation_time = current_time + delay
                new_alert = Alert(
                    self.device_id, alert.description, propagation_time
                )
                print(alert.create_send_alert_message(
                    self.device_id, target_device.device_id, current_time
                ))
                queue.append((propagation_time, "alert", target_device, new_alert))

        else:
            print(alert.create_receive_alert_message(
                self.device_id, alert.device_id, current_time
            ))
            for target_device, delay in self.propagation_set.items():
                propagation_time = current_time + delay
                new_alert = Alert(
                    self.device_id, alert.description, propagation_time
                )
                print(alert.create_send_alert_message(
                    self.device_id, target_device.device_id, current_time
                ))
                queue.append((propagation_time, "alert", target_device, new_alert))


    def receive_cancellation(
            self, cancel: Cancellation, current_time: int, queue: list):
        """Receive a cancellation and propagate it to other devices."""
        # If this cancellation has been canceled BEFORE this current_time, do not propagate
        for desc, canceled_id, receiver_id, cancel_time in self.canceled_alerts:
            if desc == cancel.description and cancel_time < current_time:
                return

        # Check if the cancellation is already recorded
        if (cancel.description, cancel.device_id, self.device_id, cancel.time) in self.canceled_alerts:
            return

        # Add the cancellation to the set of canceled alerts
        self.canceled_alerts.add((cancel.description, cancel.device_id, self.device_id, cancel.time))

        if self.device_id == cancel.device_id:
            for target_device, delay in self.propagation_set.items():
                propagation_time = current_time + delay
                new_cancellation = Cancellation(
                    self.device_id, cancel.description, propagation_time
                )
                print(cancel.create_send_cancel_message(
                    self.device_id, target_device.device_id, current_time
                ))
                queue.append(
                    (propagation_time, "cancellation", target_device, new_cancellation)
                )

        else:
            print(cancel.create_receive_cancel_message(
                self.device_id, cancel.device_id, current_time
            ))
            for target_device, delay in self.propagation_set.items():
                propagation_time = current_time + delay
                new_cancellation = Cancellation(
                    self.device_id, cancel.description, propagation_time
                )
                print(cancel.create_send_cancel_message(
                    self.device_id, target_device.device_id, current_time
                ))
                queue.append(
                    (propagation_time, "cancellation", target_device, new_cancellation)
                )

    def raise_alert(self, description, time, queue):
        """Raise an alert and propagate it to other devices."""
        alert = Alert(self.device_id, description, time)
        # scheduling propagation to other devices
        self.receive_alert(alert, time, queue)

    def cancel_alert(self, description, time, queue):
        """Cancel an alert and propagate it to other devices."""
        cancellation = Cancellation(self.device_id, description, time)
        # scheduling propagation to other devices
        self.receive_cancellation(cancellation, time, queue)

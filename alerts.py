"""alerts.py"""
# Evan-Soobin Jeon
# ejeon2@uci.edu


class Alert:
    """Alert class represents an alert from a device."""
    def __init__(self, device_id: int, description: str, time: int):
        """__init_ method initializes the Alert object."""
        if device_id < 0:
            raise ValueError("device_id must be a non-negative integer.")
        self.device_id = device_id
        self.description = description
        self.time = time

    def __str__(self):
        """__str__ method returns a str representation of the Alert object."""
        return (f"Alert[{self.description}] from "
                f"Device {self.device_id} at {self.time}ms")

    def create_send_alert_message(
            self, sender_id: int, receiver_id: int, time: int
                                  ):
        """creates a formatted message for sending"""
        return (f"@{time}: #{sender_id} SENT ALERT TO "
                f"#{receiver_id}: {self.description}")

    def create_receive_alert_message(
            self, sender_id: int, receiver_id: int, time: int
                                     ):
        """creates a formatted message for receiving"""
        return (f"@{time}: #{sender_id} RECEIVED ALERT FROM "
                f"#{receiver_id}: {self.description}")

    @staticmethod
    def create_end_message(time: int):
        """creates a formatted message for ending"""
        return f"@{time}: END"

# alert = Alert(1, "Fire", 10)
# print(alert.create_send_alert_message(1, 2, 10))
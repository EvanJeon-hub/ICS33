"""cancellation.py"""
# Evan-Soobin Jeon
# ejeon2@uci.edu


class Cancellation:
    """Cancellation class for handling cancellation messages."""
    def __init__(self, device_id: int, description: str, time: int):
        if device_id < 0:
            raise ValueError("device_id must be a non-negative integer.")
        self.device_id = device_id
        self.description = description
        self.time = time

    def __str__(self):
        """__str__ method for printing the cancellation."""
        return (f"Cancellation[{self.description}] from "
                f"Device {self.device_id} at {self.time}ms")

    def create_send_cancel_message(
            self, sender_id: int, receiver_id: int, time: int
    ):
        """creates a send cancellation message"""
        return (f"@{time}: #{sender_id} SENT CANCELLATION TO "
                f"#{receiver_id}: {self.description}")

    def create_receive_cancel_message(
            self, sender_id: int, receiver_id: int, time: int
    ):
        """creates a receive cancellation message"""
        return (f"@{time}: #{sender_id} RECEIVED CANCELLATION FROM "
                f"#{receiver_id}: {self.description}")

    @staticmethod
    def create_end_message(time: int):
        """creates an end message"""
        return f"@{time}: END"

# cancel = Cancellation(1, "Fire", 10)
# print(cancel.create_send_cancel_message(1, 2, 10))
# cancellations.py
# Evan-Soobin Jeon
# ejeon2@uci.edu

class Cancellation:
    def __init__(self, device_id: int, description: str, timestamp: int):
        self.device_id = device_id
        self.description = description
        self.timestamp = timestamp

    def __str__(self):
        return f"Cancellation[{self.description}] from Device {self.device_id} at {self.timestamp}ms"

    def create_send_cancel_message(self, device_id: int, description: str, timestamp: int):
        pass

    def create_receive_cancel_message(self, device_id: int, description: str, timestamp: int):
        pass


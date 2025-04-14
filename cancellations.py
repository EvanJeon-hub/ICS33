# cancellations.py
# Evan-Soobin Jeon
# ejeon2@uci.edu

class Cancellation:
    def __init__(self, device_id: int, description: str, time: int):
        self.device_id = device_id
        self.description = description
        self.time = time

    def __str__(self):
        return f"Cancellation[{self.description}] from Device {self.device_id} at {self.time}ms"

    def create_send_cancel_message(self, sender_id: int, receiver_id: int, time: int):
        return f"@{time}: #{sender_id} SENT CANCELLATION TO #{receiver_id}: {self.description}"

    def create_receive_cancel_message(self, sender_id: int, receiver_id: int, time: int):
        return f"@{time}: #{sender_id} RECEIVED CANCELLATION ALERT TO #{receiver_id}: {self.description}"

    @staticmethod
    def create_end_message(time: int):
        return f"@{time}: END"


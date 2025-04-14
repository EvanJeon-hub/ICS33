# cancellations.py
# Evan-Soobin Jeon
# ejeon2@uci.edu

class Cancellation:
    def __init__(self, device_id: int, description: str, time: int):
        if device_id < 0:
            raise ValueError("device_id must be a non-negative integer.")
        self.device_id = device_id
        self.description = description
        self.time = time

    def __str__(self):
        return f"Cancellation[{self.description}] from Device {self.device_id} at {self.time}ms"

    def create_send_cancel_message(self, sender_id: int, receiver_id: int, time: int):
        return f"@{time}: #{sender_id} SENT CANCELLATION TO #{receiver_id}: {self.description}"

    def create_receive_cancel_message(self, sender_id: int, receiver_id: int, time: int):
        return f"@{time}: #{sender_id} RECEIVED CANCELLATION FROM #{receiver_id}: {self.description}"

    @staticmethod
    def create_end_message(time: int):
        return f"@{time}: END"

cancellation = Cancellation(1, "OhNo", 1000)
print(cancellation.create_receive_cancel_message(sender_id=1, receiver_id=2, time=200))
print(cancellation.create_send_cancel_message(sender_id=2, receiver_id=1, time=150))
print(cancellation.create_end_message(time=600))

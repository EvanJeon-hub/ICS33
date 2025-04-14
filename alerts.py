# alerts.py
# Evan-Soobin Jeon
# ejeon2@uci.edu

class Alert:
    def __init__(self, device_id: int, description: str, time: int):
        self.device_id = device_id
        self.description = description
        self.time = time

    def __str__(self):
        return f"Alert[{self.description}] from Device {self.device_id} at {self.time}ms"

    def create_send_alert_message(self, sender_id: int, receiver_id: int, time: int):
        return f"@{time}: #{sender_id} SENT ALERT TO #{receiver_id}: {self.description}"

    def creat_receive_alert_message(self, sender_id: int, receiver_id: str, time: int):
        return f"@{time}: #{sender_id} RECEIVED ALERT FROM #{receiver_id}: {self.description}"

    @ staticmethod
    def create_end_message(time: int):
        return f"@{time}: END"

print(Alert(1, "Test Alert", 1000))
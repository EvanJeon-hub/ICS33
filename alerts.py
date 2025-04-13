# Evan-Soobin Jeon
# ejeon2@uci.edu

class Alert:
    def __init__(self, device_id: int, description: str, timestamp: int):
        self.device_id = device_id
        self.description = description
        self.timestamp = timestamp

    def __str__(self):
        return f"Alert[{self.description}] from Device {self.device_id} at {self.timestamp}ms"

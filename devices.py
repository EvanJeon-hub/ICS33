# Evan-Soobin Jeon
# ejeon2@uci.edu

from alerts import *
from cancellations import *

class devices:
    def __init__(self, device_id):
        if device_id < 0:
            raise ValueError("device_id must be a non-negative integer.")
        self.ID = device_id

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_traceback):
        return False



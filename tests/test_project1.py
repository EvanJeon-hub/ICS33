# test_project1.py
# Evan-Soobin Jeon
# ejeon2@uci.edu

import unittest
from alerts import Alert
from cancellations import Cancellation
from devices import Device
from inputs import input_command
from project1 import *


class Test_Alerts(unittest.TestCase):
    def test_alert_initialization(self):
        alert = Alert(device_id=1, description="power_outage", time=100)
        self.assertEqual(alert.device_id, 1)
        self.assertEqual(alert.description, "power_outage")
        self.assertEqual(alert.time, 100)

    def test_alert_str(self):
        alert = Alert(2, "network_error", 250)
        expected_str = "Alert[network_error] from Device 2 at 250ms"
        self.assertEqual(str(alert), expected_str)

    def test_create_send_alert_message_success(self):
        alert = Alert(1, "OhNo", 300)
        message = alert.create_send_alert_message(sender_id=2, receiver_id=1, time=50)
        expected_message = "@50: #2 SENT ALERT TO #1: OhNo"
        self.assertEqual(message, expected_message)

    def test_create_send_alert_message_failure(self):
        alert = Alert(1, "OhNo", 300)
        message = alert.create_send_alert_message(sender_id=2, receiver_id=1, time=50)
        expected_message = "@100: #2 SENT ALERT TO #1: OhNo"
        self.assertNotEqual(message, expected_message)

    def test_create_receive_alert_message_success(self):
        alert = Alert(1, "OhNo", 300)
        message = alert.create_receive_alert_message(sender_id=1, receiver_id=2, time=100)
        expected_message = "@100: #1 RECEIVED ALERT FROM #2: OhNo"
        self.assertEqual(message, expected_message)

    def test_create_receive_alert_message_failure(self):
        alert = Alert(1, "OhNo", 300)
        message = alert.create_receive_alert_message(sender_id=1, receiver_id=2, time=100)
        expected_message = "@200: #1 RECEIVED ALERT FROM #3: OhNo"
        self.assertNotEqual(message, expected_message)

    def test_create_end_message_success(self):
        alert = Alert(1, "OhNo", 300)
        message = alert.create_end_message(time=500)
        expected_message = "@500: END"
        self.assertEqual(message, expected_message)

    def test_create_end_message_failure(self):
        alert = Alert(1, "OhNo", 300)
        message = alert.create_end_message(time=500)
        expected_message = "@600: END"
        self.assertNotEqual(message, expected_message)


class Test_cancellations(unittest.TestCase):
    def test_cancellation_initialization(self):
        cancellation = Cancellation(device_id=1, description="OhNo", time=1000)
        self.assertEqual(cancellation.device_id, 1)
        self.assertEqual(cancellation.description, "OhNo")
        self.assertEqual(cancellation.time, 1000)

    def test_cancellation_str(self):
        cancellation = Cancellation(2, "network_error", 250)
        expected_str = "Cancellation[network_error] from Device 2 at 250ms"
        self.assertEqual(str(cancellation), expected_str)

    def test_create_send_cancel_message_success(self):
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_send_cancel_message(sender_id=2, receiver_id=1, time=150)
        expected_message = "@150: #2 SENT CANCELLATION TO #1: OhNo"
        self.assertEqual(message, expected_message)

    def test_create_send_cancel_message_failure(self):
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_send_cancel_message(sender_id=2, receiver_id=1, time=150)
        expected_message = "@200: #2 SENT CANCELLATION TO #1: OhNo"
        self.assertNotEqual(message, expected_message)

    def test_create_receive_cancel_message_success(self):
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_receive_cancel_message(sender_id=1, receiver_id=2, time=200)
        expected_message = "@200: #1 RECEIVED CANCELLATION FROM #2: OhNo"
        self.assertEqual(message, expected_message)

    def test_create_receive_cancel_message_failure(self):
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_receive_cancel_message(sender_id=1, receiver_id=2, time=200)
        expected_message = "@150: #1 RECEIVED CANCELLATION FROM #2: OhNo"
        self.assertNotEqual(message, expected_message)

    def test_create_end_message(self):
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_end_message(time=600)
        expected_message = "@600: END"
        self.assertEqual(message, expected_message)

    def test_create_end_message_failure(self):
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_end_message(time=600)
        expected_message = "@700: END"
        self.assertNotEqual(message, expected_message)


class Test_devices(unittest.TestCase):
    pass


class Test_inputs(unittest.TestCase):
    pass


class Test_project1(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()

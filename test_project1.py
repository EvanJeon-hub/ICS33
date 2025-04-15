"""Test cases for project1"""
# Evan-Soobin Jeon
# ejeon2@uci.edu

import unittest
from io import StringIO
from contextlib import redirect_stdout
import tempfile
from alerts import Alert
from cancellations import Cancellation
from devices import Device
from inputs import input_command
from project1 import _read_input_file_path, main

# coverage report -m (shows report with percent)
# coverage run -m --branch pytest . (branch coverage)


class TestAlerts(unittest.TestCase):
    """Test cases for the Alert class"""
    def test_alert_initialization_success(self):
        """test the initialization of the Alert class"""
        alert = Alert(device_id=1, description="power_outage", time=100)
        self.assertEqual(alert.device_id, 1)
        self.assertEqual(alert.description, "power_outage")
        self.assertEqual(alert.time, 100)

    def test_alert_initialization_failure(self):
        """test the initialization of the Alert class"""
        with self.assertRaises(ValueError):
            Alert(device_id=-1, description="power_outage", time=100)

    def test_alert_str_success(self):
        """test the string representation of the Alert class"""
        alert = Alert(2, "network_error", 250)
        expected_str = "Alert[network_error] from Device 2 at 250ms"
        self.assertEqual(str(alert), expected_str)

    def test_alert_str_failure(self):
        """test the string representation of the Alert class"""
        alert = Alert(2, "network_error", 250)
        expected_str = "Alert[network_error] from Device 3 at 250ms"
        self.assertNotEqual(str(alert), expected_str)

    def test_create_send_alert_message_success(self):
        """test the creation of the send alert message"""
        alert = Alert(1, "OhNo", 300)
        message = alert.create_send_alert_message(
            sender_id=2, receiver_id=1, time=50
        )
        expected_message = "@50: #2 SENT ALERT TO #1: OhNo"
        self.assertEqual(message, expected_message)

    def test_create_send_alert_message_failure(self):
        """test the creation of the send alert message"""
        alert = Alert(1, "OhNo", 300)
        message = alert.create_send_alert_message(
            sender_id=2, receiver_id=1, time=50
        )
        expected_message = "@100: #2 SENT ALERT TO #1: OhNo"
        self.assertNotEqual(message, expected_message)

    def test_create_receive_alert_message_success(self):
        """test the creation of the receiving alert message"""
        alert = Alert(1, "OhNo", 300)
        message = alert.create_receive_alert_message(
            sender_id=1, receiver_id=2, time=100
        )
        expected_message = "@100: #1 RECEIVED ALERT FROM #2: OhNo"
        self.assertEqual(message, expected_message)

    def test_create_receive_alert_message_failure(self):
        """test the creation of the receiving alert message"""
        alert = Alert(1, "OhNo", 300)
        message = alert.create_receive_alert_message(
            sender_id=1, receiver_id=2, time=100
        )
        expected_message = "@200: #1 RECEIVED ALERT FROM #3: OhNo"
        self.assertNotEqual(message, expected_message)

    def test_create_end_message_success(self):
        """test the creation of the end message"""
        alert = Alert(1, "OhNo", 300)
        message = alert.create_end_message(time=500)
        expected_message = "@500: END"
        self.assertEqual(message, expected_message)

    def test_create_end_message_failure(self):
        """test the creation of the end message"""
        alert = Alert(1, "OhNo", 300)
        message = alert.create_end_message(time=500)
        expected_message = "@600: END"
        self.assertNotEqual(message, expected_message)


class TestCancellations(unittest.TestCase):
    """Test cases for the Cancellation class"""
    def test_cancellation_initialization_success(self):
        """test the initialization of the Cancellation class"""
        cancellation = Cancellation(device_id=1, description="OhNo", time=1000)
        self.assertEqual(cancellation.device_id, 1)
        self.assertEqual(cancellation.description, "OhNo")
        self.assertEqual(cancellation.time, 1000)

    def test_cancellation_initialization_failure(self):
        """test the initialization of the Cancellation class"""
        with self.assertRaises(ValueError):
            Cancellation(device_id=-1, description="OhNo", time=1000)

    def test_cancellation_str(self):
        """test the string representation of the Cancellation class"""
        cancellation = Cancellation(2, "network_error", 250)
        expected_str = "Cancellation[network_error] from Device 2 at 250ms"
        self.assertEqual(str(cancellation), expected_str)

    def test_cancellation_str_success(self):
        """test the string representation of the Cancellation class"""
        cancellation = Cancellation(2, "network_error", 250)
        expected_str = "Cancellation[network_error] from Device 2 at 250ms"
        self.assertEqual(str(cancellation), expected_str)

    def test_create_send_cancel_message_success(self):
        """test the creation of the send cancel message"""
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_send_cancel_message(
            sender_id=2, receiver_id=1, time=150
        )
        expected_message = "@150: #2 SENT CANCELLATION TO #1: OhNo"
        self.assertEqual(message, expected_message)

    def test_create_send_cancel_message_failure(self):
        """test the creation of the send cancel message"""
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_send_cancel_message(
            sender_id=2, receiver_id=1, time=150
        )
        expected_message = "@200: #2 SENT CANCELLATION TO #1: OhNo"
        self.assertNotEqual(message, expected_message)

    def test_create_receive_cancel_message_success(self):
        """test the creation of the receiving cancel message"""
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_receive_cancel_message(
            sender_id=1, receiver_id=2, time=200
        )
        expected_message = "@200: #1 RECEIVED CANCELLATION FROM #2: OhNo"
        self.assertEqual(message, expected_message)

    def test_create_receive_cancel_message_failure(self):
        """test the creation of the receiving cancel message"""
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_receive_cancel_message(
            sender_id=1, receiver_id=2, time=200
        )
        expected_message = "@150: #1 RECEIVED CANCELLATION FROM #2: OhNo"
        self.assertNotEqual(message, expected_message)

    def test_create_end_message(self):
        """test the creation of the end message"""
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_end_message(time=600)
        expected_message = "@600: END"
        self.assertEqual(message, expected_message)

    def test_create_end_message_failure(self):
        """test the creation of the end message"""
        cancellation = Cancellation(1, "OhNo", 1000)
        message = cancellation.create_end_message(time=600)
        expected_message = "@700: END"
        self.assertNotEqual(message, expected_message)


class TestDevices(unittest.TestCase):
    """Test cases for the Device class"""
    def test_device_initialization_success(self):
        """test the initialization of the Device class"""
        device = Device(device_id=1)
        self.assertEqual(device.device_id, 1)
        self.assertEqual(device.notified_alerts, set())
        self.assertEqual(device.canceled_alerts, set())
        self.assertEqual(device.propagation_set, {})

    def test_device_initialization_failure(self):
        """test the initialization of the Device class"""
        with self.assertRaises(ValueError):
            Device(device_id=-1)

    def test_device_eq_success(self):
        """Test equality check (__eq__) for two devices with same ID"""
        d1 = Device(device_id=5)
        d2 = Device(device_id=5)
        self.assertEqual(d1, d2)

    def test_device_eq_failure(self):
        """Test inequality check (__eq__) for two devices with different IDs"""
        d1 = Device(device_id=5)
        d2 = Device(device_id=7)
        self.assertNotEqual(d1, d2)

    def test_device_hash_equal(self):
        """Test hash function (__hash__) for two devices with same ID"""
        d1 = Device(device_id=10)
        d2 = Device(device_id=10)
        self.assertEqual(hash(d1), hash(d2))

    def test_device_hash_not_equal(self):
        """Test hash function (__hash__) for two devices with different IDs"""
        d1 = Device(device_id=10)
        d2 = Device(device_id=20)
        self.assertNotEqual(hash(d1), hash(d2))

    def test_device_add_propagation_set_success(self):
        """test the add_propagation_set method"""
        device = Device(device_id=1)
        target_device = Device(device_id=2)
        device.add_propagation_set(target_device=target_device, delay=100)
        self.assertEqual(device.propagation_set, {target_device: 100})

    def test_device_add_propagation_set_failure_type_error(self):
        """test the add_propagation_set method"""
        device = Device(device_id=1)
        with self.assertRaises(TypeError):
            device.add_propagation_set(target_device="not_a_device", delay=100)

    def test_device_add_propagation_set_failure_value_error(self):
        """test that ValueError is raised for invalid device_id or delay"""
        device = Device(device_id=1)

        with self.assertRaises(ValueError) as context1:
            device.add_propagation_set(
                target_device=Device(device_id=-1), delay=100
            )
        self.assertIn(
            "device_id must be a non-negative", str(context1.exception)
        )

        with self.assertRaises(ValueError) as context2:
            device.add_propagation_set(
                target_device=Device(device_id=2), delay=-50
            )
        self.assertIn("must be non-negative", str(context2.exception))

    def test_receive_alert_description_already_notified(self):
        """test the receive_alert method"""
        device = Device(device_id=1)
        alert = Alert(device_id=2, description="power_outage", time=100)
        device.notified_alerts.add("power_outage")
        queue = []
        device.receive_alert(alert, 50, queue)
        self.assertEqual(queue, [])

    def test_receive_alert_create_receive_alert_message_success(self):
        """test the receive_alert method"""
        device = Device(device_id=1)
        alert = Alert(device_id=2, description="power", time=100)
        queue = []

        output = StringIO()
        with redirect_stdout(output):
            device.receive_alert(alert, 50, queue)

        output_lines = output.getvalue().strip().split("\n")
        expected_message = "@50: #1 RECEIVED ALERT FROM #2: power"
        self.assertIn(expected_message, output_lines)

    def test_receive_alert_create_receive_alert_message_failure(self):
        """test the receive_alert method"""
        device = Device(device_id=1)
        alert = Alert(device_id=2, description="power", time=100)
        queue = []

        output = StringIO()
        with redirect_stdout(output):
            device.receive_alert(alert, 50, queue)

        output_lines = output.getvalue().strip().split("\n")
        expected_message = "@100: #1 RECEIVED ALERT FROM #2: power"
        self.assertNotIn(expected_message, output_lines)

    # TODO: Line 47 - 54
    def test_receive_alert_create_send_alert_message_success(self):
        """test the receive_alert method"""

    def test_receive_alert_create_send_alert_message_failure(self):
        """test the receive_alert method"""

    def test_receive_cancellation_description_already_canceled(self):
        """test the receive_cancellation method"""
        device = Device(device_id=1)
        cancel = Cancellation(
            device_id=2, description="power", time=100
        )
        device.canceled_alerts.add("power")
        queue = []
        device.receive_cancellation(cancel, 50, queue)
        self.assertEqual(queue, [])

    def test_receive_cancellation_create_receive_cancel_message_success(self):
        """test the receive_cancellation method"""
        device = Device(device_id=1)
        cancel = Cancellation(
            device_id=2, description="power", time=100
        )
        queue = []

        output = StringIO()
        with redirect_stdout(output):
            device.receive_cancellation(cancel, 50, queue)

        output_lines = output.getvalue().strip().split("\n")
        expected_message = "@50: #1 RECEIVED CANCELLATION FROM #2: power"
        self.assertIn(expected_message, output_lines)

    def test_receive_cancellation_create_receive_cancel_message_failure(self):
        """test the receive_cancellation method"""
        device = Device(device_id=1)
        cancel = Cancellation(device_id=2, description="power", time=100)
        queue = []

        output = StringIO()
        with redirect_stdout(output):
            device.receive_cancellation(cancel, 50, queue)

        output_lines = output.getvalue().strip().split("\n")
        expected_message = "@100: #1 RECEIVED CANCELLATION FROM #2: power"
        self.assertNotIn(expected_message, output_lines)

    # TODO: Line 68 - 76
    def test_receive_cancellation_create_send_cancel_message_success(self):
        """test the receive_cancellation method"""

    def test_receive_cancellation_create_send_cancel_message_failure(self):
        """test the receive_cancellation method"""

    # TODO: raise_alert()
    def test_raise_alert_success(self):
        """test the raise_alert method"""

    def test_raise_alert_failure(self):
        """test the raise_alert method"""

    # TODO: cancel_alert()
    def test_cancel_alert_success(self):
        """test the cancel_alert method"""

    def test_cancel_alert_failure(self):
        """test the cancel_alert method"""


class TestInputs(unittest.TestCase):
    """Test cases for the input_command function"""
    def test_basic_input_parsing_success(self):
        """test the input_command function"""
        test_input = StringIO(
            "LENGTH 600000\n"
            "DEVICE 1\n"
            "PROPAGATE 1 2 100\n"
            "ALERT 1 OhNo 5000\n"
            "CANCEL 1 OhNo 6000\n"
        )
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(test_input.getvalue().encode())
            temp_file.flush()
            devices, events, simulation_time = input_command(temp_file.name)

        self.assertEqual(simulation_time, 600000)
        self.assertEqual(len(devices), 1)
        self.assertEqual(len(events), 3)
        self.assertEqual(events[0], ("PROPAGATE", 1, 2, "100"))
        self.assertEqual(events[1][0], "ALERT")
        self.assertEqual(events[2][0], "CANCEL")
        self.assertEqual(events[1][1].description, "OhNo")
        self.assertEqual(events[2][1].description, "OhNo")
        self.assertEqual(events[1][1].device_id, 1)
        self.assertEqual(events[2][1].device_id, 1)
        self.assertEqual(events[1][1].time, 5000)
        self.assertEqual(events[2][1].time, 6000)

    def test_basic_input_parsing_failure(self):
        """test the input_command function"""
        test_input = StringIO(
            "LENGTH 600000\n"
            "DEVICE 1\n"
            "PROPAGATE 1 2 100\n"
            "ALERT 1 OhNo 5000\n"
            "CANCEL 1 OhNo 6000\n"
        )
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(test_input.getvalue().encode())
            temp_file.flush()
            devices, events, simulation_time = input_command(temp_file.name)

        self.assertNotEqual(simulation_time, 700000)
        self.assertNotEqual(len(devices), 2)
        self.assertNotEqual(len(events), 4)
        self.assertNotEqual(events[0], ("PROPAGATE", 1, 3, "100"))
        self.assertNotEqual(events[0][0], "ALERT")
        self.assertNotEqual(events[1][0], "CANCEL")
        self.assertNotEqual(events[2][0], "ALERT")
        self.assertNotEqual(events[1][1].description, "Ohno")
        self.assertNotEqual(events[2][1].description, "Ohno")
        self.assertNotEqual(events[1][1].device_id, 2)
        self.assertNotEqual(events[2][1].device_id, 2)
        self.assertNotEqual(events[1][1].time, 6000)
        self.assertNotEqual(events[2][1].time, 7000)

    def test_input_startswith_hash_success(self):
        """test the input_command function"""
        test_input = StringIO(
            "# This is a comment\n"
            "LENGTH 600000\n"
            "# Another comment\n"
            "DEVICE 1\n"
            "PROPAGATE 1 2 100\n"
            "ALERT 1 OhNo 5000\n"
            "CANCEL 1 OhNo 6000\n"
        )
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(test_input.getvalue().encode())
            temp_file.flush()
            devices, events, simulation_time = input_command(temp_file.name)

        self.assertEqual(simulation_time, 600000)
        self.assertEqual(len(devices), 1)
        self.assertEqual(len(events), 3)
        self.assertEqual(events[0], ("PROPAGATE", 1, 2, "100"))
        self.assertEqual(events[0][0], "PROPAGATE")
        self.assertEqual(events[1][0], "ALERT")
        self.assertEqual(events[2][0], "CANCEL")
        self.assertEqual(events[1][1].description, "OhNo")
        self.assertEqual(events[2][1].description, "OhNo")
        self.assertEqual(events[1][1].device_id, 1)
        self.assertEqual(events[2][1].device_id, 1)
        self.assertEqual(events[1][1].time, 5000)
        self.assertEqual(events[2][1].time, 6000)

    def test_input_startswith_hash_failure(self):
        """test the input_command function"""
        test_input = StringIO(
            "# This is a comment\n"
            "LENGTH 600000\n"
            "# Another comment\n"
            "DEVICE 1\n"
            "PROPAGATE 1 2 100\n"
            "ALERT 1 OhNo 5000\n"
            "CANCEL 1 OhNo 6000\n"
        )
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(test_input.getvalue().encode())
            temp_file.flush()
            devices, events, simulation_time = input_command(temp_file.name)

        self.assertNotEqual(simulation_time, 700000)
        self.assertNotEqual(len(devices), 2)
        self.assertNotEqual(len(events), 4)
        self.assertNotEqual(events[0], ("PROPAGATE", 1, 3, "100"))
        self.assertNotEqual(events[0][0], "ALERT")
        self.assertNotEqual(events[1][0], "CANCEL")
        self.assertNotEqual(events[2][0], "ALERT")
        self.assertNotEqual(events[1][1].description, "Ohno")
        self.assertNotEqual(events[2][1].description, "Ohno")
        self.assertNotEqual(events[1][1].device_id, 2)
        self.assertNotEqual(events[2][1].device_id, 2)
        self.assertNotEqual(events[1][1].time, 6000)
        self.assertNotEqual(events[2][1].time, 7000)


class TestProject1(unittest.TestCase):
    """Test cases for the project1 module"""


if __name__ == '__main__':
    unittest.main()

"""Test cases for project1"""
# Evan-Soobin Jeon
# ejeon2@uci.edu

import unittest
from contextlib import redirect_stdout, contextmanager
import tempfile
import os
import sys
from pathlib import Path
from io import StringIO
from alerts import Alert
from cancellations import Cancellation
from devices import Device
from inputs import input_command
from project1 import read_input_file_path, main

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

    def test_receive_alert_prevent_duplicate_success(self):
        """test the receive_alert method"""
        device = Device(1)
        queue = []

        alert = Alert(0, "Power Failure", 100)
        device.notified_alerts.add((
            alert.description, alert.device_id, device.device_id, alert.time
        ))

        device.receive_alert(alert, 100, queue)
        self.assertEqual(len(queue), 0)

    def test_receive_alert_prevent_duplicate_failure(self):
        """test the receive_alert method"""
        device = Device(1)
        queue = []

        alert = Alert(0, "Power Failure", 100)
        device.notified_alerts.add((
            alert.description, alert.device_id, device.device_id, alert.time
        ))

        device.receive_alert(alert, 100, queue)
        self.assertNotEqual(len(queue), 1)

    def test_receive_cancellation_prevent_duplicate_success(self):
        """test the receive_cancellation method"""
        device = Device(1)
        queue = []

        cancel = Cancellation(0, "Power Failure", 100)
        device.canceled_alerts.add((
            cancel.description, cancel.device_id, device.device_id, cancel.time
        ))

        device.receive_cancellation(cancel, 100, queue)
        self.assertEqual(len(queue), 0)

    def test_receive_cancellation_prevent_duplicate_failure(self):
        """test the receive_cancellation method"""
        device = Device(1)
        queue = []

        cancel = Cancellation(0, "Power Failure", 100)
        device.canceled_alerts.add((
            cancel.description, cancel.device_id, device.device_id, cancel.time
        ))

        device.receive_cancellation(cancel, 100, queue)
        self.assertNotEqual(len(queue), 1)

    def test_raise_alert_success(self):
        """test the raise_alert method"""
        device1 = Device(1)
        device2 = Device(2)
        device1.add_propagation_set(device2, delay=2)

        queue = []
        device1.raise_alert("Ohno", 10, queue)

        self.assertEqual(len(queue), 1)
        event_time, event_type, target_device, alert_obj = queue[0]
        self.assertEqual(event_time, 12)  # 10 + delay(2)
        self.assertEqual(event_type, "alert")
        self.assertEqual(target_device, device2)
        self.assertIsInstance(alert_obj, Alert)
        self.assertEqual(alert_obj.description, "Ohno")

    def test_raise_alert_failure(self):
        """test the raise_alert method"""
        device1 = Device(1)
        device2 = Device(2)
        device1.add_propagation_set(device2, delay=2)

        queue = []
        device1.raise_alert("Ohno", 10, queue)

        self.assertNotEqual(len(queue), 2)
        event_time, _, _, _ = queue[0]
        self.assertNotEqual(event_time, 15)

    def test_cancel_alert_success(self):
        """test the cancel_alert method"""
        device1 = Device(1)
        device2 = Device(2)
        device1.add_propagation_set(device2, delay=3)

        queue = []
        device1.cancel_alert("Ohno", 20, queue)

        self.assertEqual(len(queue), 1)
        event_time, event_type, target_device, cancel_obj = queue[0]
        self.assertEqual(event_time, 23)  # 20 + delay(3)
        self.assertEqual(event_type, "cancellation")
        self.assertEqual(target_device, device2)
        self.assertIsInstance(cancel_obj, Cancellation)
        self.assertEqual(cancel_obj.description, "Ohno")

    def test_cancel_alert_failure(self):
        """test the cancel_alert method"""
        device1 = Device(1)
        device2 = Device(2)
        device1.add_propagation_set(device2, delay=3)

        queue = []
        device1.cancel_alert("Ohno", 20, queue)

        self.assertNotEqual(len(queue), 2)
        event_time, _, _, _ = queue[0]
        self.assertNotEqual(event_time, 25)

    def test_alert_blocked_due_to_older_cancellation(self):
        """test the alert_blocked_due_to_older_cancellation method"""

    def test_cancel_blocked_due_to_older_alert(self):
        """test the cancel_blocked_due_to_older_alert method"""


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

        self.assertIsInstance(devices, dict)
        self.assertIsInstance(events, list)
        self.assertIsInstance(simulation_time, int)
        self.assertIsInstance(devices[1], Device)
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

        self.assertNotIsInstance(simulation_time, str)
        self.assertNotIsInstance(devices, list)
        self.assertNotIsInstance(events, dict)
        self.assertNotIsInstance(devices[1], str)
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

    def test_invalid_command_ignored_success(self):
        """Test that invalid commands are ignored by input_command"""
        with tempfile.NamedTemporaryFile(
                mode='w+', delete=False, encoding='utf-8') as temp_file:
            temp_file.write("""
            LENGTH 100
            DEVICE 1
            UNKNOWN_COMMAND foo bar baz
            DEVICE 2
            """)
            temp_file_path = temp_file.name

        devices, events, simulation_time = input_command(temp_file_path)

        os.remove(temp_file_path)

        self.assertEqual(simulation_time, 100)
        self.assertEqual(len(devices), 2)
        self.assertEqual(len(events), 0)
        self.assertIn(1, devices)
        self.assertIn(2, devices)
        self.assertIsInstance(devices[1], Device)
        self.assertIsInstance(devices[2], Device)

    def test_invalid_command_ignored_failure(self):
        """Test that invalid commands are ignored by input_command"""
        with tempfile.NamedTemporaryFile(
                mode='w+', delete=False, encoding='utf-8') as temp_file:
            temp_file.write("""
            LENGTH 100
            DEVICE 1
            UNKNOWN_COMMAND foo bar baz
            DEVICE 2
            """)
            temp_file_path = temp_file.name

        devices, events, simulation_time = input_command(temp_file_path)

        os.remove(temp_file_path)

        self.assertNotEqual(simulation_time, 200)
        self.assertNotEqual(len(devices), 3)
        self.assertNotEqual(len(events), 1)
        self.assertNotIn(3, devices)
        self.assertNotIsInstance(devices[1], str)
        self.assertNotIsInstance(devices[2], str)


@contextmanager
def redirect_stdin(new_stdin):
    """Context manager to redirect stdin to a new StringIO object"""
    original_stdin = sys.stdin
    sys.stdin = new_stdin
    try:
        yield
    finally:
        sys.stdin = original_stdin


class TestProject1(unittest.TestCase):
    """
    Test cases for the project1 module.
    This module also covers devices.py
    """
    def test_project1_read_input_file_path_success(self):
        """Test the read_input_file_path function without mock"""
        test_input = StringIO("  /home/user/data.txt  \n")
        expected_path = Path("/home/user/data.txt")

        with redirect_stdin(test_input):
            result = read_input_file_path()

        self.assertEqual(result, expected_path)
        self.assertIsInstance(result, Path)

    def test_project1_read_input_file_path_failure(self):
        """Test the read_input_file_path function without mock"""
        test_input = StringIO("  /home/user/data.txt  \n")
        _ = Path("/home/user/data.txt")

        with redirect_stdin(test_input):
            result = read_input_file_path()

        self.assertNotEqual(result, Path("/home/user/other.txt"))
        self.assertNotIsInstance(result, str)

    def test_main_file_not_found_success(self):
        """Test the main function with a non-existent file"""
        test_input = StringIO("non_existent_file.txt\n")

        with redirect_stdin(test_input), redirect_stdout(StringIO()) as output:
            main()
            output_value = output.getvalue().strip()

        self.assertEqual(output_value, "FILE NOT FOUND")

    def test_main_file_not_found_failure(self):
        """Test the main function with a non-existent file"""
        test_input = StringIO("non_existent_file.txt\n")

        with redirect_stdin(test_input), redirect_stdout(StringIO()) as output:
            main()
            output_value = output.getvalue().strip()

        self.assertNotEqual(output_value, "FILE FOUND")
        self.assertNotIn("FILE FOUND", output_value)

    def test_project1_main_success(self):
        """Test the main function with a valid input file"""
        test_input = (
            "LENGTH 900\n"
            "DEVICE 1\n"
            "DEVICE 2\n"
            "PROPAGATE 1 2 100\n"
            "PROPAGATE 2 1 100\n"
            "ALERT 1 Badness 200\n"
            "CANCEL 1 Badness 450\n"
        )

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(test_input)
            temp_file_path = temp_file.name

        try:
            with redirect_stdin(StringIO(f"{temp_file_path}\n")), \
                    redirect_stdout(StringIO()) as output:
                main()
                output_value = output.getvalue().strip().replace("\r\n", "\n")

            expected_output = (
                "@200: #1 SENT ALERT TO #2: Badness\n"
                "@300: #2 RECEIVED ALERT FROM #1: Badness\n"
                "@300: #2 SENT ALERT TO #1: Badness\n"
                "@400: #1 RECEIVED ALERT FROM #2: Badness\n"
                "@400: #1 SENT ALERT TO #2: Badness\n"
                "@450: #1 SENT CANCELLATION TO #2: Badness\n"
                "@500: #2 RECEIVED ALERT FROM #1: Badness\n"
                "@500: #2 SENT ALERT TO #1: Badness\n"
                "@550: #2 RECEIVED CANCELLATION FROM #1: Badness\n"
                "@550: #2 SENT CANCELLATION TO #1: Badness\n"
                "@600: #1 RECEIVED ALERT FROM #2: Badness\n"
                "@650: #1 RECEIVED CANCELLATION FROM #2: Badness\n"
                "@900: END"
            )

            self.assertEqual(output_value, expected_output)

        finally:
            os.remove(temp_file_path)

    def test_project1_main_failure(self):
        """Test the main function with an invalid output (failure)"""
        test_input = (
            "LENGTH 900\n"
            "DEVICE 1\n"
            "DEVICE 2\n"
            "PROPAGATE 1 2 100\n"
            "PROPAGATE 2 1 100\n"
            "ALERT 1 Badness 200\n"
            "CANCEL 1 Badness 450\n"
        )

        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(test_input)
            temp_file_path = temp_file.name

        try:
            with redirect_stdin(StringIO(f"{temp_file_path}\n")), \
                    redirect_stdout(StringIO()) as output:
                main()
                output_value = output.getvalue().strip().replace("\r\n", "\n")

            expected_output = output_value.replace("@900: END", "@9000 END")

            self.assertNotEqual(output_value, expected_output)

        finally:
            os.remove(temp_file_path)


if __name__ == '__main__':
    unittest.main()

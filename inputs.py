# Evan-Soobin Jeon
# ejeon2@uci.edu
import shlex

def _input(command):
    command_input = shlex.split(command)
    command = command_input[0]

    if command == "LENGTH" and int(command_input[1]) > 0:
        """characteristic 1"""

    if command == "DEVICE" and int(command_input[1]) > 0:
        """characteristic 2"""

    if command == "PROPAGATE" and int(command_input[1]) > 0 and int(command_input[2]) > 0 and int(command_input[3]) > 0:
        """characteristic 3"""

    if command == "ALERT" and int(command_input[1]) > 0 and command_input[2] == str and int(command_input[3]) > 0:
        """characteristic 4"""

    if command == "CANCEL" and int(command_input[1]) > 0 and command_input[2] == str and int(command_input[3]) > 0:
        """characteristic 5"""

    if command == "":
        """characteristic 6"""

    if command == "#":
        """characteristic 7"""







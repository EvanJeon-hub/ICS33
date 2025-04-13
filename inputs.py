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

    if command == "PROPAGATE":
        """characteristic 3"""

    if command == "ALERT":
        """characteristic 4"""

    if command == "CANCEL":
        """characteristic 5"""

    if command == "":
        """characteristic 6"""

    if command == "#":
        """characteristic 7"""







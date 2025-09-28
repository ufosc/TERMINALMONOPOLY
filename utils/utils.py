# Loading animation function
import itertools
import sys
import time
loading = True
def loading_animation(text: str="Loading...", flag: bool = True) -> None:
    for frame in itertools.cycle(['|', '/', '-', '\\']):
        if not flag:
            break
        sys.stdout.write(f'\r{text} {frame}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f'\r{text} complete!     \n')

import socket
import modules_directory.inventory as inv
class Client:
    def __init__(self, socket: socket.socket, id: int, name: str, inventory_object: inv.Inventory):
        self.socket = socket
        self.id = id
        self.name = name
        self.inventory = inventory_object
        self.can_roll = True
        self.num_rolls = 0
        self.terminal_statuses = ["ACTIVE", "ACTIVE", "ACTIVE", "ACTIVE"]
        self.trades = [{"name":"", "properties":[]}, {"name":"", "properties":[]}, {"name":"", "properties":[]}] # List of trades for this player
        self.PlayerObject = None # Player object for this client


# Written by @https://github.com/SerpentBTW

"""
All functions here CAN use print() because they are not to be called during
gameplay. They are only to be called during the setup of the game, where 
printing directly using print() is not an issue. Do not use in any main()
functions or modules that are called during gameplay.
"""


def validate_name(name) -> bool:
    """
    names cannot be greater than 8 characters
    alphnumeric, spaces, and apostrophes are allowed
    """
    if len(name) > 8:
        return False

    for char in name:
        if not (char.isalnum() or char == " " or char == "'"):
            return False

    return True


import subprocess


def is_port_unused(port: int) -> bool:
    """
    Check if port is being used in any capacity. If the port inputted is, the program will return False.
    """
    result = subprocess.run(["netstat", "-an"], capture_output=True, text=True)
    if f":{port}" in result.stdout:
        print(f"Port {port} is already in use.")
        return False
    return True


def validate_port(port: str):
    """
    Validate a port. The port must be a number between 1024 and 65535.
    """

    if not port.isdigit():
        print(f"Port {port} is not a number.")
        return False

    port = int(port)
    if port < 1024 or port > 65535:
        print(f"Port {port} is not in the valid range of 1024-65535.")
        return False

    return True


def validate_address(address: str) -> bool:
    """
    Validate an IP address. The address must be in the form of 4 numbers separated by dots.
    Each number must be between 0 and 255.
    """
    if address.count(".") != 3:
        return False

    parts = address.split(".")
    for part in parts:
        if not part.isdigit():
            return False

        part = int(part)
        if part < 0 or part > 255:
            return False

    return True
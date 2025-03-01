from screenspace import Terminal
from socket import socket
import networking as net

class GenericModule:
    def __init__(self, name):
        self.name = name
        self.command = "generic"

    def module(self, pid: int = None, server_socket: socket = None, active_terminal: Terminal = None):
        """
        This method is a placeholder for the module's main functionality.
        It is intended to be overridden by subclasses to provide specific behavior.
        """

        if active_terminal is not None:
            active_terminal.update("I am a generic module, I do nothing." + f"\nYou're player ID is {pid}.\n")
        
        if server_socket is not None:
            net.send_message(server_socket, f"{pid}generic")

    def get_name(self):
        return self.name

    
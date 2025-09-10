from utils.utils import screenspace as ss
from socket import socket
import networking as net

name = "Deed Viewer"
author = "https://github.com/adamgulde"
description = "View property deed details."
version = "1.3" # Moved to its own file
command = "deed"
module_type = "player"
help_text = "Type DEED to view property deeds."
persistent = True # Keep the terminal open after use
oof_params = {"player_id": None, "server": None, "index": None} # Global parameters for out of focus function
    
def run(player_id:int, server: socket, active_terminal: ss.Terminal):
    global oof_params
    active_terminal.persistent = persistent
    index = ss.get_valid_int("Enter a property ID (or ENTER to skip): ", 1, 39, disallowed=[0,2,4,7,10,17,20,22,30,33,36,38], allowed=[" "])
    if not index == "":
        active_terminal.persistent = persistent
        active_terminal.oof_callable = oof # Set the out of focus callable function
        oof_params = net.set_oof_params(player_id, server, index=index) # Set the parameters for the out of focus function
        active_terminal.clear()

        # Send the deed request to the server, which will return the deed data.
        net.send_message(server, f'{player_id}deed {index}')

        # Wait for server to send back the deed, then display it on the active terminal.
        deed = net.receive_message(server)
        active_terminal.update(deed, padding=False)

def oof() -> str:
    """
    Update function for when the terminal is out of focus. Does NOT need active_terminal, and returns the string to be displayed.
    """
    server = oof_params["server"]
    player_id = oof_params["player_id"]
    index = oof_params["index"]

    # Send the deed request to the server, which will return the deed data.
    net.send_message(server, f'{player_id}deed {index}')

    # Wait for server to send back the deed, then display it on the active terminal.
    deed = net.receive_message(server)
    return deed
    

def handle(data, client_socket, mply):
    """
    Handles the deed command for the banker.
    """
    if data.startswith("deed"):
        # Extract the location from the command
        cmds = data.split(' ') 
        location = int(cmds[1])
        # Get the property data from the Monopoly game instance
        property_data = mply.get_deed(location)
        # Get the deed string representation
        deed_str = property_data.get_deed_str(0) 

        # Send the deed string to the client
        net.send_message(client_socket, deed_str)
import screenspace as ss
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
    active_terminal.persistent = persistent
    index = ss.get_valid_int("Enter a property ID (or ENTER to skip): ", 1, 39, disallowed=[0,2,4,7,10,17,20,22,30,33,36,38], allowed=[" "])
    if not index == "":
        active_terminal.persistent = persistent
        active_terminal.oof_callable = oof # Set the out of focus callable function
        set_oof_params(player_id, server, index) # Set the parameters for the out of focus function
        active_terminal.clear()

        # Send the deed request to the server, which will return the deed data.
        net.send_message(server, f'{player_id}deed {index}')

        # Wait for server to send back the deed, then display it on the active terminal.
        net.player_mtrw = True
        deed = net.receive_message(server)
        net.player_mtrw = False
        active_terminal.update(deed, padding=False)

def set_oof_params(player_id:int, server: socket, index: int) -> None: 
    """
    Sets the parameters for the out of focus function.
    """
    oof_params["player_id"] = player_id
    oof_params["server"] = server
    oof_params["index"] = index

def oof() -> str:
    """
    Update function for when the terminal is out of focus. Does NOT need active_terminal, and returns the string to be displayed.
    """
    server = oof_params["server"]
    player_id = oof_params["player_id"]
    index = oof_params["index"]

    # Send the deed request to the server, which will return the deed data.
    net.send_oof_message(server, f'{player_id}deed {index}')

    # Wait for OOF response
    deed = ""
    while not net.has_oof_messages():
        from time import sleep
        sleep(0.01)  # Small delay to avoid busy waiting
    deed = net.receive_oof_message()
    return deed
    

def handle(data, client_socket, mply, is_oof_request=False):
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

        # Send the deed string to the client with OOF tagging if needed
        if is_oof_request:
            net.send_message(client_socket, f"OOF:{deed_str}")
        else:
            net.send_message(client_socket, deed_str)
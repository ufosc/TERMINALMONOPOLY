import screenspace as ss
from socket import socket
import networking as net

name = "Deed Viewer"
author = "https://github.com/adamgulde"
description = "View property deed details."
version = "1.3" # Moved to its own file
command = "deed"
help_text = "Type DEED to view property deeds."
    
def run(player_id:int, server: socket, active_terminal: ss.Terminal):
    index = ss.get_valid_int("Enter a property ID: ", 1, 39, disallowed=[0,2,4,7,10,17,20,22,30,33,36,38], allowed=[" "])
    if not index == "":
        active_terminal.clear()
        # active_terminal.set_persistent(True) # Always allow players to use deeds when they navigate to the deed terminal.
        active_terminal.persistent_command = "deed"

        # Send the deed request to the server, which will return the deed data.
        net.send_message(server, f'{player_id}deed {index}')

        # Wait for server to send back the deed, then display it on the active terminal.
        active_terminal.update(net.receive_message(server), padding=False)
    else: 
        active_terminal.is_retrieved = False # Allow player to use deeds again.
        stdIn = ""
        active_terminal.update("Return to this Terminal to use deeds.", padding=True)
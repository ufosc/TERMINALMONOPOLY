import screenspace as ss
from socket import socket
import networking as net

name = "Player List"
author = "https://github.com/adamgulde"
version = "1.0" # Moved to its own file
command = "plist"
help_text = "Type PLIST to view other players' information."
persistent = True # Keep the terminal open after use
oof_params = {"player_id": None, "server": None, "index": None} # Global parameters for out of focus function
    
def run(player_id:int, server: socket, active_terminal: ss.Terminal):
    active_terminal.persistent = persistent
    active_terminal.oof_callable = oof # Set the out of focus callable function
    set_oof_params(player_id, server) # Set the parameters for the out of focus function
    active_terminal.update("Loading player list...", padding=True)

    # Send the deed request to the server, which will return the deed data.
    net.send_message(server, f'{player_id}plist')

    # Wait for server to send back the deed, then display it on the active terminal.
    net.player_mtrw = True
    message = net.receive_message(server)
    net.player_mtrw = False
    active_terminal.update(message, padding=True)

def set_oof_params(player_id:int, server: socket) -> None: 
    """
    Sets the parameters for the out of focus function.
    """
    oof_params["player_id"] = player_id
    oof_params["server"] = server

def oof() -> str:
    """
    Update function for when the terminal is out of focus. Does NOT need active_terminal, and returns the string to be displayed.
    """
    server = oof_params["server"]
    player_id = oof_params["player_id"]

    # Send the deed request to the server, which will return the deed data.
    net.send_message(server, f'{player_id}plist')

    # Wait for server to send back the deed, then display it on the active terminal.
    plist = net.receive_message(server)
    return plist
    

def handle(client_socket, clients):
    """
    Builds and sends a player list message to the client.
    Parameters:
        client (socket): The socket of the client to send the message to.
        clients (list): List of all connected clients.
    """
    # Build the player list message
    message = "Player List:\n\n"
    for c in clients:
        message += "│" + f"{c.name}".center(14)
        message += "│" + f"ID: {c.id}".center(14)
        message += "│" + f"Cash: {c.money}".center(14) + "│\n" 

    # Send the deed string to the client
    net.send_message(client_socket, message)
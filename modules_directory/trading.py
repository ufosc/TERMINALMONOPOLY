import screenspace as ss
from socket import socket
import networking as net
from style import graphics as g, set_cursor_str
from random import randint
import textwrap

name = "Trading Module"
author = "https://github.com/adamgulde"
description = "Trade assets with other players."
version = "1.0" 
command = "trade"
help_text = "Type TRADE to trade assets with other players."
persistent = False
oof_params = {"player_id": None, "server": None} # Global parameters for out of focus function

def run(player_id:int, server: socket, active_terminal: ss.Terminal):
    """
    Trading Module

    Allows players to trade assets with each other. 
    Players can offer cash, properties, and stocks in exchange for other assets.
    Version 1.0 will only allow cash and property trades, but future versions will allow all inventory items as well.

    Args:
        player_id (int): The ID of the player.
        server (socket): The server socket to communicate with.
        active_terminal (ss.Terminal): The terminal to display the information.
        
    Returns:
        None
    """
    img = g.get("trading_network")
    active_terminal.update(img, True) # Print the image, with padding to clear old text.
    active_terminal.persistent = persistent
    active_terminal.oof_callable = oof # Set the out of focus callable function
    set_oof_params(player_id, server) # Set the parameters for the out of focus function
    
    net.send_message(server, f'{player_id}trade,open')
    net.player_mtrw = True
    info = net.receive_message(server)
    net.player_mtrw = False

    if "``__f" in info: 
        info = info.replace("``__f", "") 
        img += (set_cursor_str(62, 7) + "." + set_cursor_str(65, 7) + "." + set_cursor_str(62, 9) + "----")

    if "__players:" in info: # If the players are in the network, add them to the string.
        players = info.split("__players:")[1].split("__;")[0].split(",")
        for player in players:
            if player != "":
                img += set_cursor_str(33, 15 + players.index(player)) + f"{player}" # Offset the players.

    if "__ads:" in info: # If there is an ad, position them in the string.
        ad = info.split("__ads:")[1].split("__;")[0] # Get the ad from the string.
        text_list = textwrap.wrap(ad, 22)
        for i, line in enumerate(text_list):
            if i == 3: break # Limit to 3 lines of ads.
            img += set_cursor_str(52, 16 + i) + line # Offset the ads.

    message = info.split("__msg:")[1].split("__;")[0] # Get the message from the string.
    
    if "\n" in message:  # Check if there are newlines in the message
        lines = message.split("\n")
        n = 0
        for line in lines:
            wrapped_lines = textwrap.wrap(line, 49)  # Wrap each line to 49 characters
            for i, wrapped_line in enumerate(wrapped_lines):
                if i == 7: break  # Limit to 7 lines of messages
                img += set_cursor_str(1, n + 1 + i) + wrapped_line  # Adjust cursor for each wrapped line
            n += 1
    else:
        img += set_cursor_str(1, 1) + message  # Single-line message

    ret_val = img # Add the image to the return value.

    active_terminal.update(ret_val, False) # Update the terminal with the information, without overwriting the entire image.

def set_oof_params(player_id:int, server: socket) -> None: 
    """
    Sets the parameters for the out of focus function.
    """
    oof_params["player_id"] = player_id
    oof_params["server"] = server

def oof() -> str:
    """
    Update function for when the terminal is out of focus. Does NOT need active_terminal, and returns the string to be displayed.
    Of course, do NOT update player_mtrw here because this is not called in the main thread.
    """
    server = oof_params["server"]
    player_id = oof_params["player_id"]

    header = f"World Wide Web Trading Menu".center(75)
    
    ret_val = header

    return ret_val
    
def handle(data, client_socket, clients, mply, money, properties):
    """
    Handles the trade command for the banker.
    """
    ret_val = ""

    # Any data that needs to be parsed by the client will be of form "__key:", and will be separated by commas. It will end with __;.
    # Anything that the player directly prints will be of form "__msg:message__;".
    # The player will need to parse the message, and display it in the correct location.

    if "open" in data:
        """
        Opens the trading network, and displays the welcome message.
        This will also send to the client the list of players in the network, which needs to be parsed.
        """
        ret_val += f"__msg:TMTN: Welcome to the Trading Network\nYou can trade assets with other players.__;" # Welcome message.
        ret_val += "__players:" # List all players in the network, except the one who opened the network.
        for player in clients:
            ret_val += f"{player.name},"
        ret_val += "__;"

        ads = ["Safe, online trading since '25", "Trade with confidence!", "The best TM trading network in the world!", 
                "Trade with your friends!", "Trade with your enemies!", "Trade with your plants!", "Trade using your computer!", 
                "Trade using your microwave!", "Make money, trade with us!", "Trade with the best!", "Trade to get a gazillion dollars!",
                "Trade now, or be a loser!", "Trade now, or be a loser forever!", "Trading is what we do best!", 
                "Trading on TMTN has never been easier. It changed my life!", "You should trade Boardwalk, it's the best property!",
                "Don't sleep on Mediterranean Avenue, it's an interesting property!", "The Utilities are great for trading!"]
        ret_val += f"__ads:{ads[randint(0, len(ads)-1)]}__;" # Random ad from the list.

    if randint(0, 14400) == 3100: ret_val += "``__f"
    net.send_message(client_socket, ret_val)
import screenspace as ss
from socket import socket
import networking as net
from style import graphics as g, set_cursor_str

name = "Balance Module"
author = "https://github.com/adamgulde"
description = "View balance, net worth, stocks, and property deeds."
version = "1.0" # Moved to its own file
command = "bal"
help_text = "Type BAL to view your cash and assets."
persistent = False
oof_params = {}

def run(player_id:int, server: socket, active_terminal: ss.Terminal):
    """
    Balance Module
    
    Displays the player's cash and assets.
    
    Args:
        player_id (int): The ID of the player.
        server (socket): The server socket to communicate with.
        active_terminal (ss.Terminal): The terminal to display the information.
        
    Returns:
        None
    """
    global oof_params
    active_terminal.clear()
    active_terminal.persistent = persistent
    active_terminal.oof_callable = oof # Set the out of focus callable function
    oof_params = net.set_oof_params(player_id, server) # Set the parameters for the out of focus function
    
    header = f"Consolidated Cash and Assets".center(75)
    # Get the player's cash on hand
    net.send_message(server, f'{player_id}bal,get_assets,get_net_worth')
    info = header + "\n" + net.receive_message(server)

    # Get moneybag image and create the lists of lines
    image = str(g.get("moneybag"))
    image = image.splitlines()
    info_lines = info.splitlines() 

    ret_val = ""

    for i in range(len(image)):
        ret_val += " " * 35 + image[i] + "\n"
    active_terminal.update(ret_val, False) # print just the moneybags 

    ret_val = ""
    for i in range(ss.rows):
        if i < len(info_lines): # Check if there is a line in info
            ret_val += info_lines[i] + "\n" # Only info line
        else:
            ret_val += "\n"

    active_terminal.update(ret_val, False) # print the rest of the info, False to print over the moneybags, but not clear the screen

def oof() -> str:
    """
    Update function for when the terminal is out of focus. Does NOT need active_terminal, and returns the string to be displayed.
    """
    server = oof_params["server"]
    player_id = oof_params["player_id"]

    header = f"Consolidated Cash and Assets".center(75)
    # Get the player's cash on hand
    net.send_message(server, f'{player_id}bal,get_assets,get_net_worth')
    info = header + "\n" + net.receive_message(server)

    # Get moneybag image and create the lists of lines
    image = str(g.get("moneybag"))
    image = image.splitlines()
    info_lines = info.splitlines() 
    
    ret_val = ""

    for j in range(len(image)):
        ret_val += " " * 35 + image[j] + "\n" # Print the moneybags image 35 spaces from the left side of the screen.

    for i in range(ss.rows):
        if i < len(info_lines): # Check if there is a line in info
            ret_val += set_cursor_str(0,i) + info_lines[i] # Only info line, set cursor to the beginning of the line.a

    return ret_val
    

def handle(data, client_socket, mply, money, properties):
    """
    Handles the balance command for the banker.
    """
    ret_val = ""
    if "bal" in data:
        """
        Simply return the client's balance.
        """
        ret_val += f"Cash on hand: {str(money)}\n"
        if data == "bal": 
            net.send_message(client_socket, str(money))
            return

    if "get_assets" in data:
        """
        Build the string list of client's assets.
        """
        assets = ""
        i = 0
        for prop in properties:
            deed = mply.get_deed(prop.location)
            name = deed.name.split()[0][:3] + " " + deed.name.split()[1][:3] # Get first 3 letters of each word
            if i % 2 == 0:
                assets += f"{name} - ${deed.getPrice() + deed.housePrice * deed.houses}".ljust(15)
            else:
                assets += f" | {name} - ${deed.getPrice() + deed.housePrice * deed.houses}\n"
            i += 1
        if properties == []:
            assets += "You have no properties.\n"

        # for stock in current_client.stocks:
        #     assets += stock.get_value()

        # for fish in current_client.inventory.fish..... <- something like this

        ret_val += assets
        
    if "get_net_worth" in data:
        """
        Calculate net worth of client based on money, properties, and stocks.
        """
        net_worth = money
        for prop in properties:
            deed = mply.get_deed(prop.location)
            deed_value = deed.getPrice() if deed.mortgaged == False else deed.mortgage
            deed_value += deed.housePrice * deed.houses 
            net_worth += deed_value

        # for stock in current_client.stocks:
        #     net_worth += stock.get_value()

        ret_val += f"You have a net worth of ${net_worth}.\n"
    net.send_message(client_socket, ret_val)
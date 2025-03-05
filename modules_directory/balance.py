import screenspace as ss
from socket import socket
import networking as net
from style import graphics as g, COLORS

name = "Balance Module"
author = "https://github.com/adamgulde"
description = "View balance, net worth, stocks, and property deeds."
version = "1.0" # Moved to its own file
command = "bal"
help_text = "Type BAL to view your cash and assets."
persistent = False
    
def run(player_id:int, server: socket, active_terminal: ss.Terminal):
    active_terminal.clear()

    # Get moneybag image and create the list of lines, where the middle 14 lines are the moneybag image
    # image = g.get("moneybag")
    # lines = [""] * 3 + [image] * 14 + [""] * 3
    
    header = f"Consolidated Cash and Assets".center(75)
    # Get the player's cash on hand
    net.send_message(server, f'{player_id}bal,get_assets,get_net_worth')
    info = header + "\n" + net.receive_message(server)
    

    active_terminal.update(info, False)

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
        for prop in properties:
            deed = mply.get_deed(prop)
            name = deed.name.split()[0][:3] + " " + deed.name.split()[1][:3] # Get first 3 letters of each word
            assets += f"{name} - ${deed.getPrice() + deed.housePrice * deed.houses}\n"
        if properties == []:
            assets += "You have no properties.\n"

        # for stock in current_client.stocks:
        #     assets += stock.get_value()

        ret_val += assets
        
    if "get_net_worth" in data:
        """
        Calculate net worth of client based on money, properties, and stocks.
        """
        net_worth = money
        for prop in properties:
            deed = mply.get_deed(prop)
            deed_value = deed.getPrice() if deed.mortgaged == False else deed.mortgage
            deed_value += deed.housePrice * deed.houses 
            net_worth += deed_value

        # for stock in current_client.stocks:
        #     net_worth += stock.get_value()

        ret_val += f"You have a net worth of ${net_worth}.\n"
    net.send_message(client_socket, ret_val)
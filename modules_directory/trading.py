import textwrap
# import keyboard | Redacted
import readchar
import time
import utils.networking as net
from socket import socket
from utils.screenspace import g, set_cursor_str, MYCOLORS as COLORS, Terminal
from utils.utils import Client
from random import randint

name = "Trading Module"
author = "https://github.com/adamgulde"
version = "1.0" 
command = "trade"
help_text = "Type TRADE to trade assets with other players."
persistent = False
oof_params = {"player_id": None, "server": None} # Global parameters for out of focus function

# The auctions are a list of dictionaries, where each dictionary is an auction.
# Each auction has a name, an object (the item being auctioned), a price, and a bidder, and a time remaining.
class Temp:
    def __init__(self, l, n):
        self.location = l
        self.name = n

o1 = Temp(3, "Player")
o2 = Temp(4, "four")
o3 = Temp(5, "five")
o4 = Temp(39, "yeah")


auctions = [{"name": o1.name, "obj": o1, "price": 0, "bidder": "", "remaining": 0}, 
            {"name": o2.name, "obj": o2, "price": 0, "bidder": "", "remaining": 0},
            {"name": o3.name, "obj": o3, "price": 0, "bidder": "", "remaining": 0},
            {"name": o4.name, "obj": o4, "price": 0, "bidder": "", "remaining": 0},] 

def run(player_id:int, server: socket, active_terminal: Terminal):
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
    global oof_params
    img = g.get("trading_network")
    active_terminal.update(img, True) # Print the image, with padding to clear old text.
    active_terminal.persistent = persistent
    active_terminal.oof_callable = oof # Set the out of focus callable function
    oof_params = net.set_oof_params(player_id, server) # Set the parameters for the out of focus function
    net.send_message(server, f'{player_id}trade,open')
    info = net.receive_message(server)

    # Get initial trading menu. 
    img += client_parse_menu(info) # Parse the data from the client, add to the image.
    ret_val = img # Add the image to the return value.
    active_terminal.update(ret_val, False) # Update the terminal with the information, without overwriting the entire image.

    # Navigate the trading menu.
    while True:
        choice = navigate([(2, 11), (2, 12), (2, 13), (2, 16), (2, 17), (2, 18), (48, 11), (48, 12), (58, 11), (58, 12)], active_terminal, ret_val) # Get the coordinates of the options in the menu.

        net.send_message(server, f"{player_id}trade,eval,{choice}") # Send the choice to the server.
        server_choice = net.receive_message(server) # Receive the choice from the server.
        
        if server_choice == "invalid": # If the choice is invalid, update the terminal with the error message.
            ret_val += COLORS.RED + set_cursor_str(22, 10) + "Invalid choice." + COLORS.ORANGE + set_cursor_str(22, 11) + "Please try again." + COLORS.RESET
        elif server_choice == "-1": # Player pressed "q" to quit the menu.
            ret_val += set_cursor_str(22, 10) + " " * 22 + set_cursor_str(22, 11) + " " * 22
            ret_val += COLORS.BLUE + set_cursor_str(22, 10) + "Come again soon!" + COLORS.GREEN + set_cursor_str(22, 11) + "Come again soon!" + COLORS.RESET
            active_terminal.update(ret_val, False) # Paste exit message onto terminal
            break
        else:
            ret_val += set_cursor_str(22, 10) + " " * 22 + set_cursor_str(22, 11) + " " * 22
            if server_choice.startswith("trading_screen") and server_choice.startswith("trading_auctions"):
                ret_val = img + client_parse_menu(server_choice)
            else: 
                img_name = server_choice.split(",")[0] # Get the image name from the server choice.
                trade_auction_data = server_choice.split(",", 1)[1:] # Get the trade or auction data from the server choice.
                img = g.get(img_name) # get either the trading screen or the trading auctions.
                active_terminal.update(img, True) # Update the terminal with the image. 
                break # Exit the loop if the choice is valid. 
            # data = net.receive_message(server) 
            # active_terminal.update(data, False) # Update the terminal with the specific data from the server.
    
    # trade_auction_data
    # Navigate the new trade menu
    # while True:
        # choice = navigate([(0,2), (0,3), (24, 2), (24, 3)]) # This will be dependent on what's received from Banker

    
    active_terminal.indicate_keyboard_hook(off=True) # Stop the keyboard hook.


def navigate(option_coords: list, active_terminal: Terminal, static_menu: str) -> int:

    """
    Navigates the trading menu.

    Args:
        options (int): The number of options in the menu to navigate through.
        option_coords (list): The coordinates of the options in the menu to move the cursor to.
        
    Returns:
        int: The selected option index.
    """
    active_terminal.indicate_keyboard_hook()
    selecting = True
    selected_option = 0 # The option that is currently selected.
    time.sleep(0.25) # Sleep to prevent an accidental purchase from pressing "enter" too fast.
     # Wait for the user to release the enter key before proceeding.

    old_x = option_coords[selected_option][0] # Get the x coordinate of the selected option.
    old_y = option_coords[selected_option][1] # Get the y coordinate of the selected option.
    active_terminal.update(static_menu + COLORS.BLUE + set_cursor_str(old_x, old_y) + ">>", False) # Update the terminal with the default option.

    while selecting:
        key = readchar.readkey()
        keyLower = key.lower() if len(key) == 1 else key
        
        if keyLower == 'w' or key == readchar.key.UP:  # Move up in the menu
            old_x = option_coords[selected_option][0] # Get the x coordinate of the selected option.
            old_y = option_coords[selected_option][1] # Get the y coordinate of the selected option.
            selected_option -= 1 # Move up in the menu.
            if selected_option < 0: # If the selected option is less than 0, wrap around to the last option.
                selected_option = len(option_coords) - 1 # Wrap around to the last option.
            # Wait for the user to release the up key before proceeding.
            time.sleep(0.25)

        elif keyLower == 's' or key == readchar.key.DOWN:  # Move down in the menu
            old_x = option_coords[selected_option][0] # Get the x coordinate of the selected option.
            old_y = option_coords[selected_option][1] # Get the y coordinate of the selected option.
            selected_option += 1 # Move down in the menu.
            if selected_option >= len(option_coords): # If the selected option is greater than the number of options, wrap around to the first option.
                selected_option = 0 # Wrap around to the first option.
            # Wait for the user to release the down key before proceeding.
            time.sleep(0.25)
        
        elif key == readchar.key.ENTER:  # Select item
            selecting = False  # Exit the loop 

        elif keyLower == 'q':  # Quit menu
            selecting = False  # Exit the loop
            selected_option = -1 # Set the selected option to -1 to indicate quitting.
        
        x = option_coords[selected_option][0] # Get the x coordinate of the selected option.
        y = option_coords[selected_option][1] # Get the y coordinate of the selected option.

        if old_x != x or old_y != y:  # If the cursor has moved, update the terminal.
            active_terminal.update(static_menu + COLORS.BLUE + set_cursor_str(x, y) + ">>", False) # Update the terminal with the selected option.
            old_x = x # Update the old x coordinate.
            old_y = y 
    
    return selected_option # Return the selected option.

def client_parse_menu(info: str) -> str:
    """
    Parses the data from the client and returns the string to be displayed.
    The data will be of form "__key:", and will be separated by commas. It will end with __;.
    """
    ret_val = ""

    if "``__f" in info: 
        info = info.replace("``__f", "") 
        ret_val += (set_cursor_str(62, 7) + "." + set_cursor_str(65, 7) + "." + set_cursor_str(62, 9) + "----")

    if "__players:" in info: # If the players are in the network, add them to the string.
        players = info.split("__players:")[1].split("__;")[0].split(",")
        for player in players:
            if player != "":
                ret_val += set_cursor_str(28, 15 + players.index(player)) + f"{player}" # Offset the players.

    if "__ads:" in info: # If there is an ad, position them in the string.
        ad = info.split("__ads:")[1].split("__;")[0] # Get the ad from the string.
        text_list = textwrap.wrap(ad, 22)
        for i, line in enumerate(text_list):
            if i == 3: break # Limit to 3 lines of ads.
            ret_val += set_cursor_str(48, 16 + i) + line # Offset the ads.

    if "__pending:" in info: # If there are pending trades, add them to the string.
        pending = info.split("__pending:")[1].split("__;")[0].split(",")
        for trade in pending:
            if trade != "":
                ret_val += set_cursor_str(8, 15 + pending.index(trade)) + f"{trade}"
    
    if "__requests:" in info: # If there are requested trades, add them to the string.
        requests = info.split("__requests:")[1].split("__;")[0].split(",")
        for trade in requests:
            if trade != "":
                ret_val += set_cursor_str(8, 20 + requests.index(trade)) + f"{trade}"
    
    if "__auctions:" in info: # If there are open auctions, add them to the string.
        auctions = info.split("__auctions:")[1].split("__;")[0].split(",")
        i = 0
        coords = [(50, 11), (50, 12), (60, 11), (60, 12)] # Auction locations are not linear =(
        for auction in auctions:
            if auction != "":
                ret_val += set_cursor_str(coords[i][0], coords[i][1]) + f"{auction}" 
            i += 1
                    


    message = info.split("__msg:")[1].split("__;")[0] # Get the message from the string.
    
    if "\n" in message:  # Check if there are newlines in the message
        lines = message.split("\n")
        n = 0
        for line in lines:
            wrapped_lines = textwrap.wrap(line, 49)  # Wrap each line to 49 characters
            for i, wrapped_line in enumerate(wrapped_lines):
                if i == 7: break  # Limit to 7 lines of messages
                ret_val += set_cursor_str(1, n + 1 + i) + wrapped_line  # Adjust cursor for each wrapped line
            n += 1
    else:
        ret_val += set_cursor_str(1, 1) + message  # Single-line message

    return ret_val

def client_trade():
    """
    The player trade function. This will be called when the player wants to trade with another player.
    The player will be able to choose the player they want to trade.
    They only can initiate one trade per player. They will need to close the trade before they can initiate another one with the same player.
    """
    pass # TODO: Implement the client trade function.

def oof() -> str:
    """
    Update function for when the terminal is out of focus. Does NOT need active_terminal, and returns the string to be displayed.
    """
    server = oof_params["server"]
    player_id = oof_params["player_id"]

    header = f"World Wide Web Trading Menu".center(75)
    
    ret_val = header

    return ret_val

def handle(data, player_id: int, client_socket: socket, clients: list[Client], add_to_output_area: callable):
    """
    Handles the trade command for the banker.
    """
    ret_val = ""

    client_obj = clients[player_id] # Get the client object from the list of clients.

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

        ret_val += "__pending:" # List all your pending trades in the network.
        for trade in client_obj.trades:
            if trade["name"] != "":
                ret_val += f"{trade['name']},"
        ret_val += "__;"

        ret_val += "__requests:" # List all requested trades of you in the network.
        for each_player in clients:
            if each_player.id != client_obj.id:
                for trade in each_player.trades:
                    if trade["name"] == client_obj.name:
                        ret_val += f"{each_player.name},"
        ret_val += "__;"

        ret_val += "__auctions:" # List all open auctions in the network.
        for auction in auctions:
            if auction["name"] != "":
                ret_val += f"Lot {auction.get('obj').location}," # Get the location index of the property. 
        ret_val += "__;"
        if randint(0, 14400) == 3100: ret_val += "``__f"
    
    elif "eval" in data:
        """
        Evaluates the choice made by the player.
        This will be of form "trade,eval,choice", where choice (int) is the index of the option in the menu.
        Index 0 - 2 means open a pending trade according to trades dictionary.
            This requires checking if the trade is already open. If not, ask the player to open a trade with another player.
        Index 3 - 5 means open a requested trade with player 0 - 3 excluding you.
        Index 6 - 8 means check the open auctions, excluding your own. (Each player can only have one auction open at a time.)
        """
        choice = int(data.split(",")[2])
        if choice == -1: # Player quit
            ret_val += "-1"

        elif 0 <= choice <= 2: # Open a pending trade with another player.
            if client_obj.trades[choice]["name"] == "":
                ret_val += "__msg:You have no pending trade.\n" # No pending trades.
                ret_val += "Press enter again if you like to open a trade with another player." # Ask the player if they want to open a trade.
                ret_val += "__;"
            elif client_obj.trades[choice]["name"] != "":
                pass

        elif 3 <= choice <= 5:
                for each_player in clients:
                    if each_player.id != client_obj.id:
                        for trade in each_player.trades:
                            if trade["name"] == client_obj.name:
                                ret_val += f"__msg:Trade request found with {each_player.name}.__;"
                            break
                ret_val += "invalid" # Invalid choice.
            
        elif 6 <= choice <= 9: # Open an auction.
                if choice - 6 == player_id:
                    if auctions[player_id]["name"] == client_obj.name:
                        ret_val += "__msg:You already have an open auction.\n"
                        ret_val += "Time remaining: " + str(auctions[choice - 6]["remaining"]) + " seconds.\n"
                        ret_val += "__;"
                    elif auctions[player_id]["name"] != client_obj.name:
                        ret_val += "__msg:You have no open auction.\n"
                        ret_val += "Press enter again if you like to open an auction."
                        ret_val += "__;"
                else:
                    if auctions[choice - 6]["name"] == "":
                        ret_val += "invalid" # Invalid choice because the auction (another player's auction) is not open.
                    else:
                        ret_val += "trading_auctions," # Valid choice, return the name of the auction screen. 

                        # Add auction details to the ret_val for client to parse.
                        ret_val += "__msg:Auction found with " + auctions[choice - 6]["name"] + ".\n"
                        ret_val += "Time remaining: " + str(auctions[choice - 6]["remaining"]) + " seconds.\n"
                        ret_val += "__;"
                    
            

    elif "next" in data:
        """
        Next page of the trading menu.
        This will be of form "trade,next,choice", where choice (int) is the index of the option in the menu.
        """
        choice = int(data.split(",")[2])
        if 0 <= choice <= 2:
            pass
        
            
    net.send_message(client_socket, ret_val)
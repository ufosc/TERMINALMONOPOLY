import textwrap

class Inventory():
    def __init__(self):
        """
        Initializes the inventory of the player.
        The inventory is a dictionary of items and their quantities.
        All items are stored here, to be extracted by the shop module.
        """
        self.items = {
            "fish": {"Carp": 10, "Bass": 0, "Salmon": 0},
            "module_modifiers": {},
            "board_upgrades": {},
            "defensive_items": {}
        }  # Initialize with empty inventory.
    
    def getinventory(self) -> dict:
        """
        Returns the inventory of the player.
        """
        return self.items
    
    def add_item(self, item: str, quantity: int) -> None:
        """
        Adds an item to the inventory.
        If the item already exists, it adds the quantity to the existing item.
        This could be a fish, or a Terminal upgrade, or an attack Module. 
        """
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
    
    def remove_item(self, item: str, quantity: int) -> None:
        """
        Removes an item from the inventory.
        If the item does not exist, it does nothing.
        If the quantity is greater than the quantity of the item, it removes all of the item.
        """
        for category in self.items:
            if item in self.items[category]:
                if self.items[category][item] > quantity:
                    self.items[category][item] -= quantity
                else:
                    del self.items[category][item]

    def get_inventory_str(self) -> str:
        """
        Returns a string representation of the inventory.
        """
        ret_val = ""
        for item in self.items:
            ret_val += f"{item.upper()}: " # Add the item name.
            items_unsplit = ""
            for item_name in self.items[item]:
                items_unsplit += f"{item_name}: {self.items[item][item_name]} " # Wrap the text to 75 characters, with the subsequent lines indented.
            lines = textwrap.wrap(items_unsplit, 75 - (len(item) + 1), subsequent_indent=" ")
            for line in lines:
                ret_val += line + "\n" if line != lines[-1] else line # Add a newline if there are multiple lines
            ret_val += "\n"
        return ret_val

from socket import socket
from screenspace import Terminal
import networking as net

name = "Inventory Module"
command = "inv"
author = "https://github.com/adamgulde"
description = "View all inventory items."
version = "1.3 - Integrating with banker and more robust object handling" 
help_text = "Type INV to view your inventory."
persistent = False # No need to run additional commands after switching
oof_params = {"player_id": None, "server": None} # Global parameters for out of focus function

def run(player_id:int, server: socket, active_terminal: Terminal):
    set_oof_params(player_id, server) # Set the parameters for the out of focus function
    active_terminal.persistent = persistent
    active_terminal.oof_callable = oof # Set the out of focus callable function

    net.send_message(server, f"{player_id}get_inventory_str") # Request inventory from banker
    inv_str = net.receive_message(server) # Receive inventory from banker
    active_terminal.update("Inventory".center(75, "═") + f"\n\n{inv_str}", padding=True)

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

    net.send_message(server, f"{player_id}get_inventory_str") # Request inventory from banker
    inv_str = net.receive_message(server) # Receive inventory from banker
    return "Inventory".center(75, "═") + f"\n\n{inv_str}"
    
def handle(data: str, client_socket: socket, client_inventory: Inventory) -> None:
    """
    Handles the deed command for the banker.
    """
    if data == "get_inventory_str":  # If the client is requesting the inventory string.
        net.send_message(client_socket, client_inventory.get_inventory_str()) # Send the inventory string to the client.